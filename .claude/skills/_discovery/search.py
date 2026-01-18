#!/usr/bin/env python3
"""
Semantic search for skills and agents.

Usage:
    python search.py "optimize SQL queries"
    python search.py "build REST API" --limit 5
    python search.py "security audit" --type skill
"""

import json
import math
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

INDEX_PATH = Path(__file__).parent / "index.json"


class SkillDiscovery:
    """Semantic search for skills and agents using TF-IDF."""

    def __init__(self, index_path: Path = None):
        self.index_path = index_path or INDEX_PATH
        self.index: Dict = {}
        self.stopwords = self._get_stopwords()
        self._load_index()

    def _get_stopwords(self) -> set:
        """Common stopwords."""
        return {
            "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
            "be", "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "must", "shall", "can", "need",
            "this", "that", "these", "those", "i", "you", "he", "she", "it",
            "we", "they", "what", "which", "who", "when", "where", "why", "how",
            "all", "each", "every", "both", "few", "more", "most", "other",
            "some", "such", "no", "nor", "not", "only", "own", "same", "so",
            "than", "too", "very", "just", "also", "now", "use", "using", "used"
        }

    def _load_index(self):
        """Load the search index."""
        if not self.index_path.exists():
            print(f"Index not found at {self.index_path}")
            print("Run: python indexer.py to build the index")
            self.index = {"documents": {}, "idf": {}, "vectors": {}}
            return

        with open(self.index_path, "r", encoding="utf-8") as f:
            self.index = json.load(f)

    def tokenize(self, text: str) -> List[str]:
        """Tokenize query text."""
        tokens = re.findall(r'[a-z0-9]+', text.lower())
        tokens = [t for t in tokens if t not in self.stopwords and len(t) > 2]
        return tokens

    def search(
        self,
        query: str,
        limit: int = 10,
        doc_type: Optional[str] = None,
        min_score: float = 0.1
    ) -> List[Dict]:
        """
        Search for skills and agents matching the query.

        Args:
            query: Natural language query
            limit: Maximum results to return
            doc_type: Filter by type ("skill" or "agent")
            min_score: Minimum similarity score (0-1)

        Returns:
            List of matching documents with scores
        """
        query_tokens = self.tokenize(query)
        if not query_tokens:
            return []

        # Build query vector
        query_tf = defaultdict(int)
        for token in query_tokens:
            query_tf[token] += 1

        max_tf = max(query_tf.values())
        query_vector = {}
        for term, count in query_tf.items():
            normalized_tf = count / max_tf
            idf = self.index["idf"].get(term, 0)
            query_vector[term] = normalized_tf * idf

        # Calculate similarities
        results = []
        for doc_id, doc_vector in self.index["vectors"].items():
            doc_info = self.index["documents"].get(doc_id, {})

            # Filter by type if specified
            if doc_type and doc_info.get("type") != doc_type:
                continue

            score = self._cosine_similarity(query_vector, doc_vector)
            if score >= min_score:
                results.append({
                    "doc_id": doc_id,
                    "type": doc_info.get("type", "unknown"),
                    "name": doc_info.get("name", ""),
                    "description": doc_info.get("description", ""),
                    "category": doc_info.get("category", ""),
                    "tags": doc_info.get("tags", []),
                    "score": round(score, 3)
                })

        # Sort by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def _cosine_similarity(self, vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two vectors."""
        # Dot product
        dot_product = sum(vec1.get(term, 0) * vec2.get(term, 0)
                         for term in set(vec1.keys()) | set(vec2.keys()))

        # Magnitudes
        mag1 = math.sqrt(sum(v ** 2 for v in vec1.values()))
        mag2 = math.sqrt(sum(v ** 2 for v in vec2.values()))

        if mag1 == 0 or mag2 == 0:
            return 0

        return dot_product / (mag1 * mag2)

    def suggest_for_task(self, task_description: str) -> List[Dict]:
        """
        Get skill suggestions for a task description.

        This is a convenience method that returns formatted suggestions.
        """
        results = self.search(task_description, limit=5)

        suggestions = []
        for r in results:
            suggestion = {
                "recommendation": r["name"],
                "type": r["type"],
                "relevance": f"{r['score'] * 100:.0f}%",
                "reason": r["description"][:100] + "..." if len(r["description"]) > 100 else r["description"]
            }
            suggestions.append(suggestion)

        return suggestions

    def find_related(self, skill_or_agent: str, limit: int = 5) -> List[Dict]:
        """Find related skills/agents based on the given one."""
        # Get the document
        doc_id = None
        for did in self.index["documents"]:
            if did.endswith(f":{skill_or_agent}"):
                doc_id = did
                break

        if not doc_id:
            return []

        doc_vector = self.index["vectors"].get(doc_id, {})
        if not doc_vector:
            return []

        # Find similar documents
        results = []
        for other_id, other_vector in self.index["vectors"].items():
            if other_id == doc_id:
                continue

            score = self._cosine_similarity(doc_vector, other_vector)
            if score > 0.1:
                doc_info = self.index["documents"].get(other_id, {})
                results.append({
                    "name": doc_info.get("name", ""),
                    "type": doc_info.get("type", ""),
                    "score": round(score, 3)
                })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]


def main():
    parser = argparse.ArgumentParser(description="Search for skills and agents")
    parser.add_argument("query", type=str, help="Search query")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Max results")
    parser.add_argument("--type", "-t", choices=["skill", "agent"], help="Filter by type")
    parser.add_argument("--min-score", type=float, default=0.1, help="Minimum score")
    parser.add_argument("--related", "-r", type=str, help="Find related to this skill/agent")
    args = parser.parse_args()

    discovery = SkillDiscovery()

    if args.related:
        print(f"\nSkills/Agents related to '{args.related}':\n")
        results = discovery.find_related(args.related, limit=args.limit)
    else:
        print(f"\nSearching for: '{args.query}'\n")
        results = discovery.search(
            args.query,
            limit=args.limit,
            doc_type=args.type,
            min_score=args.min_score
        )

    if not results:
        print("No results found.")
        return

    # Display results
    print("-" * 60)
    for i, r in enumerate(results, 1):
        score_bar = "█" * int(r.get("score", 0) * 20)
        print(f"{i}. [{r.get('type', 'unknown').upper():6}] {r['name']}")
        print(f"   Score: {r.get('score', 0):.2f} {score_bar}")
        if r.get("description"):
            desc = r["description"][:80] + "..." if len(r.get("description", "")) > 80 else r.get("description", "")
            print(f"   {desc}")
        if r.get("tags"):
            print(f"   Tags: {', '.join(r['tags'][:5])}")
        print()

    print("-" * 60)
    print(f"Found {len(results)} results")


if __name__ == "__main__":
    main()
