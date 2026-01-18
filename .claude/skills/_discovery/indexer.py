"""
TF-IDF Indexer for semantic skill discovery.

Builds a search index from skill and agent metadata for natural language queries.
"""

import json
import math
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

# Paths
SKILLS_DIR = Path(__file__).parent.parent
AGENTS_DIR = SKILLS_DIR.parent / "agents"
MANIFEST_PATH = SKILLS_DIR / "MANIFEST.json"
INDEX_PATH = Path(__file__).parent / "index.json"


class TFIDFIndexer:
    """Build and manage TF-IDF index for skills and agents."""

    def __init__(self):
        self.documents: Dict[str, Dict] = {}  # doc_id -> {type, name, text, tokens}
        self.idf: Dict[str, float] = {}  # term -> IDF score
        self.doc_vectors: Dict[str, Dict[str, float]] = {}  # doc_id -> {term: tf-idf}
        self.stopwords = self._get_stopwords()

    def _get_stopwords(self) -> Set[str]:
        """Common stopwords to filter out."""
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

    def tokenize(self, text: str) -> List[str]:
        """Tokenize and normalize text."""
        # Lowercase and split on non-alphanumeric
        tokens = re.findall(r'[a-z0-9]+', text.lower())
        # Filter stopwords and short tokens
        tokens = [t for t in tokens if t not in self.stopwords and len(t) > 2]
        return tokens

    def build_index(self):
        """Build the complete search index."""
        print("Building search index...")

        # Load manifest
        manifest = self._load_manifest()

        # Index skills
        for skill_name, skill_data in manifest.get("skills", {}).items():
            self._index_skill(skill_name, skill_data)

        # Index agents
        self._index_agents()

        # Calculate IDF
        self._calculate_idf()

        # Calculate TF-IDF vectors
        self._calculate_vectors()

        # Save index
        self._save_index()

        print(f"Indexed {len(self.documents)} documents")

    def _load_manifest(self) -> Dict:
        """Load skills manifest."""
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def _index_skill(self, skill_name: str, skill_data: Dict):
        """Index a single skill."""
        # Build searchable text
        text_parts = [
            skill_name.replace("-", " "),
            skill_data.get("description", ""),
            " ".join(skill_data.get("tags", [])),
            skill_data.get("category", ""),
        ]

        # Add related skills
        for related in skill_data.get("related_skills", []):
            text_parts.append(related.replace("-", " "))

        text = " ".join(text_parts)
        tokens = self.tokenize(text)

        self.documents[f"skill:{skill_name}"] = {
            "type": "skill",
            "name": skill_name,
            "description": skill_data.get("description", ""),
            "category": skill_data.get("category", ""),
            "tags": skill_data.get("tags", []),
            "text": text,
            "tokens": tokens
        }

    def _index_agents(self):
        """Index all agents."""
        for agent_file in AGENTS_DIR.glob("*.md"):
            if agent_file.name in ["INVOCATION_MANIFEST.md", "README.md"]:
                continue

            agent_name = agent_file.stem
            content = agent_file.read_text(encoding="utf-8")

            # Extract description from frontmatter
            description = ""
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    for line in parts[1].split("\n"):
                        if line.startswith("description:"):
                            description = line.replace("description:", "").strip().strip('"')
                            break

            # Build searchable text
            text_parts = [
                agent_name.replace("-", " "),
                description,
                # Extract first 500 chars of content for additional context
                content[:500]
            ]

            text = " ".join(text_parts)
            tokens = self.tokenize(text)

            self.documents[f"agent:{agent_name}"] = {
                "type": "agent",
                "name": agent_name,
                "description": description,
                "text": text,
                "tokens": tokens
            }

    def _calculate_idf(self):
        """Calculate IDF scores for all terms."""
        # Count document frequency for each term
        df = defaultdict(int)
        for doc in self.documents.values():
            seen = set()
            for token in doc["tokens"]:
                if token not in seen:
                    df[token] += 1
                    seen.add(token)

        # Calculate IDF
        n_docs = len(self.documents)
        for term, count in df.items():
            self.idf[term] = math.log(n_docs / (count + 1)) + 1

    def _calculate_vectors(self):
        """Calculate TF-IDF vectors for all documents."""
        for doc_id, doc in self.documents.items():
            # Calculate term frequencies
            tf = defaultdict(int)
            for token in doc["tokens"]:
                tf[token] += 1

            # Normalize TF and multiply by IDF
            max_tf = max(tf.values()) if tf else 1
            vector = {}
            for term, count in tf.items():
                normalized_tf = count / max_tf
                vector[term] = normalized_tf * self.idf.get(term, 0)

            self.doc_vectors[doc_id] = vector

    def _save_index(self):
        """Save index to file."""
        index_data = {
            "version": "1.0.0",
            "documents": {
                doc_id: {
                    "type": doc["type"],
                    "name": doc["name"],
                    "description": doc["description"],
                    "category": doc.get("category", ""),
                    "tags": doc.get("tags", [])
                }
                for doc_id, doc in self.documents.items()
            },
            "idf": self.idf,
            "vectors": self.doc_vectors
        }

        with open(INDEX_PATH, "w", encoding="utf-8") as f:
            json.dump(index_data, f, indent=2)

        print(f"Index saved to {INDEX_PATH}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Build skill search index")
    parser.add_argument("--rebuild", action="store_true", help="Force rebuild")
    args = parser.parse_args()

    indexer = TFIDFIndexer()
    indexer.build_index()


if __name__ == "__main__":
    main()
