"""
Semantic Skill Discovery.

Natural language search for finding the right skills and agents.

Usage:
    from discovery import SkillDiscovery

    discovery = SkillDiscovery()
    results = discovery.search("optimize database performance")
"""

from .search import SkillDiscovery
from .indexer import TFIDFIndexer

__all__ = ["SkillDiscovery", "TFIDFIndexer"]
__version__ = "1.0.0"
