"""
SQLite storage layer for framework metrics.

Provides persistent storage for usage analytics with efficient querying.
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from contextlib import contextmanager

# Database path
DB_PATH = Path(__file__).parent / "metrics.db"


class MetricsStorage:
    """SQLite storage for framework metrics."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DB_PATH
        self._init_db()

    def _init_db(self):
        """Initialize database with schema."""
        with self._get_connection() as conn:
            conn.executescript("""
                -- Skill invocations
                CREATE TABLE IF NOT EXISTS skill_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    duration_ms INTEGER,
                    metadata TEXT,
                    session_id TEXT
                );

                -- Agent invocations
                CREATE TABLE IF NOT EXISTS agent_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    duration_ms INTEGER,
                    metadata TEXT,
                    session_id TEXT,
                    feature_name TEXT
                );

                -- Workflow events
                CREATE TABLE IF NOT EXISTS flow_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flow_name TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    phase TEXT,
                    timestamp TEXT NOT NULL,
                    duration_ms INTEGER,
                    metadata TEXT,
                    session_id TEXT,
                    feature_name TEXT
                );

                -- Session tracking
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    started_at TEXT NOT NULL,
                    ended_at TEXT,
                    project_path TEXT,
                    metadata TEXT
                );

                -- Indexes for common queries
                CREATE INDEX IF NOT EXISTS idx_skill_name ON skill_events(skill_name);
                CREATE INDEX IF NOT EXISTS idx_skill_timestamp ON skill_events(timestamp);
                CREATE INDEX IF NOT EXISTS idx_agent_name ON agent_events(agent_name);
                CREATE INDEX IF NOT EXISTS idx_agent_timestamp ON agent_events(timestamp);
                CREATE INDEX IF NOT EXISTS idx_flow_name ON flow_events(flow_name);
                CREATE INDEX IF NOT EXISTS idx_flow_timestamp ON flow_events(timestamp);
            """)

    @contextmanager
    def _get_connection(self):
        """Get database connection with context manager."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # =========================================================================
    # INSERT OPERATIONS
    # =========================================================================

    def record_skill_event(
        self,
        skill_name: str,
        event_type: str,
        duration_ms: Optional[int] = None,
        metadata: Optional[Dict] = None,
        session_id: Optional[str] = None
    ) -> int:
        """Record a skill event."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO skill_events
                (skill_name, event_type, timestamp, duration_ms, metadata, session_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    skill_name,
                    event_type,
                    datetime.utcnow().isoformat(),
                    duration_ms,
                    json.dumps(metadata) if metadata else None,
                    session_id
                )
            )
            return cursor.lastrowid

    def record_agent_event(
        self,
        agent_name: str,
        event_type: str,
        duration_ms: Optional[int] = None,
        metadata: Optional[Dict] = None,
        session_id: Optional[str] = None,
        feature_name: Optional[str] = None
    ) -> int:
        """Record an agent event."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO agent_events
                (agent_name, event_type, timestamp, duration_ms, metadata, session_id, feature_name)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    agent_name,
                    event_type,
                    datetime.utcnow().isoformat(),
                    duration_ms,
                    json.dumps(metadata) if metadata else None,
                    session_id,
                    feature_name
                )
            )
            return cursor.lastrowid

    def record_flow_event(
        self,
        flow_name: str,
        event_type: str,
        phase: Optional[str] = None,
        duration_ms: Optional[int] = None,
        metadata: Optional[Dict] = None,
        session_id: Optional[str] = None,
        feature_name: Optional[str] = None
    ) -> int:
        """Record a flow event."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO flow_events
                (flow_name, event_type, phase, timestamp, duration_ms, metadata, session_id, feature_name)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    flow_name,
                    event_type,
                    phase,
                    datetime.utcnow().isoformat(),
                    duration_ms,
                    json.dumps(metadata) if metadata else None,
                    session_id,
                    feature_name
                )
            )
            return cursor.lastrowid

    def start_session(
        self,
        session_id: str,
        project_path: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Start a new session."""
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO sessions
                (id, started_at, project_path, metadata)
                VALUES (?, ?, ?, ?)
                """,
                (
                    session_id,
                    datetime.utcnow().isoformat(),
                    project_path,
                    json.dumps(metadata) if metadata else None
                )
            )

    def end_session(self, session_id: str):
        """End a session."""
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE sessions SET ended_at = ? WHERE id = ?",
                (datetime.utcnow().isoformat(), session_id)
            )

    # =========================================================================
    # QUERY OPERATIONS
    # =========================================================================

    def get_top_skills(self, limit: int = 10, days: int = 30) -> List[Dict]:
        """Get top skills by invocation count."""
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    skill_name,
                    COUNT(*) as invocations,
                    SUM(CASE WHEN event_type = 'completed' THEN 1 ELSE 0 END) as completions,
                    SUM(CASE WHEN event_type = 'failed' THEN 1 ELSE 0 END) as failures,
                    AVG(duration_ms) as avg_duration_ms
                FROM skill_events
                WHERE timestamp >= ?
                GROUP BY skill_name
                ORDER BY invocations DESC
                LIMIT ?
                """,
                (since, limit)
            ).fetchall()
            return [dict(row) for row in rows]

    def get_top_agents(self, limit: int = 10, days: int = 30) -> List[Dict]:
        """Get top agents by invocation count."""
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    agent_name,
                    COUNT(*) as invocations,
                    SUM(CASE WHEN event_type = 'completed' THEN 1 ELSE 0 END) as completions,
                    SUM(CASE WHEN event_type = 'blocked' THEN 1 ELSE 0 END) as blocked,
                    SUM(CASE WHEN event_type = 'failed' THEN 1 ELSE 0 END) as failures,
                    AVG(duration_ms) as avg_duration_ms
                FROM agent_events
                WHERE timestamp >= ?
                GROUP BY agent_name
                ORDER BY invocations DESC
                LIMIT ?
                """,
                (since, limit)
            ).fetchall()
            return [dict(row) for row in rows]

    def get_flow_stats(self, days: int = 30) -> List[Dict]:
        """Get flow command statistics."""
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    flow_name,
                    COUNT(*) as invocations,
                    SUM(CASE WHEN event_type = 'completed' THEN 1 ELSE 0 END) as completions,
                    SUM(CASE WHEN event_type = 'failed' THEN 1 ELSE 0 END) as failures,
                    AVG(duration_ms) as avg_duration_ms
                FROM flow_events
                WHERE timestamp >= ? AND event_type IN ('started', 'completed', 'failed')
                GROUP BY flow_name
                ORDER BY invocations DESC
                """,
                (since,)
            ).fetchall()
            return [dict(row) for row in rows]

    def get_daily_trends(self, days: int = 7) -> List[Dict]:
        """Get daily usage trends."""
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    date(timestamp) as date,
                    COUNT(*) as total_events,
                    SUM(CASE WHEN event_type = 'invoked' THEN 1 ELSE 0 END) as invocations,
                    SUM(CASE WHEN event_type = 'completed' THEN 1 ELSE 0 END) as completions,
                    SUM(CASE WHEN event_type = 'failed' THEN 1 ELSE 0 END) as failures
                FROM (
                    SELECT timestamp, event_type FROM skill_events WHERE timestamp >= ?
                    UNION ALL
                    SELECT timestamp, event_type FROM agent_events WHERE timestamp >= ?
                )
                GROUP BY date(timestamp)
                ORDER BY date DESC
                """,
                (since, since)
            ).fetchall()
            return [dict(row) for row in rows]

    def get_skill_details(self, skill_name: str, days: int = 30) -> Dict:
        """Get detailed stats for a specific skill."""
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        with self._get_connection() as conn:
            # Overall stats
            row = conn.execute(
                """
                SELECT
                    COUNT(*) as total_events,
                    SUM(CASE WHEN event_type = 'invoked' THEN 1 ELSE 0 END) as invocations,
                    SUM(CASE WHEN event_type = 'completed' THEN 1 ELSE 0 END) as completions,
                    SUM(CASE WHEN event_type = 'failed' THEN 1 ELSE 0 END) as failures,
                    AVG(duration_ms) as avg_duration_ms,
                    MIN(duration_ms) as min_duration_ms,
                    MAX(duration_ms) as max_duration_ms
                FROM skill_events
                WHERE skill_name = ? AND timestamp >= ?
                """,
                (skill_name, since)
            ).fetchone()

            # Recent events
            recent = conn.execute(
                """
                SELECT event_type, timestamp, duration_ms, metadata
                FROM skill_events
                WHERE skill_name = ? AND timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT 10
                """,
                (skill_name, since)
            ).fetchall()

            return {
                "skill_name": skill_name,
                "stats": dict(row) if row else {},
                "recent_events": [dict(r) for r in recent]
            }

    def get_bottlenecks(self, threshold_ms: int = 5000, days: int = 7) -> List[Dict]:
        """Identify slow components (potential bottlenecks)."""
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    'skill' as type,
                    skill_name as name,
                    AVG(duration_ms) as avg_duration_ms,
                    MAX(duration_ms) as max_duration_ms,
                    COUNT(*) as occurrences
                FROM skill_events
                WHERE timestamp >= ? AND duration_ms IS NOT NULL
                GROUP BY skill_name
                HAVING avg_duration_ms > ?

                UNION ALL

                SELECT
                    'agent' as type,
                    agent_name as name,
                    AVG(duration_ms) as avg_duration_ms,
                    MAX(duration_ms) as max_duration_ms,
                    COUNT(*) as occurrences
                FROM agent_events
                WHERE timestamp >= ? AND duration_ms IS NOT NULL
                GROUP BY agent_name
                HAVING avg_duration_ms > ?

                ORDER BY avg_duration_ms DESC
                """,
                (since, threshold_ms, since, threshold_ms)
            ).fetchall()
            return [dict(row) for row in rows]

    def get_failure_rates(self, days: int = 7) -> List[Dict]:
        """Get failure rates for skills and agents."""
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()
        with self._get_connection() as conn:
            rows = conn.execute(
                """
                SELECT
                    'skill' as type,
                    skill_name as name,
                    COUNT(*) as total,
                    SUM(CASE WHEN event_type = 'failed' THEN 1 ELSE 0 END) as failures,
                    ROUND(100.0 * SUM(CASE WHEN event_type = 'failed' THEN 1 ELSE 0 END) / COUNT(*), 2) as failure_rate
                FROM skill_events
                WHERE timestamp >= ?
                GROUP BY skill_name
                HAVING failures > 0

                UNION ALL

                SELECT
                    'agent' as type,
                    agent_name as name,
                    COUNT(*) as total,
                    SUM(CASE WHEN event_type = 'failed' THEN 1 ELSE 0 END) as failures,
                    ROUND(100.0 * SUM(CASE WHEN event_type = 'failed' THEN 1 ELSE 0 END) / COUNT(*), 2) as failure_rate
                FROM agent_events
                WHERE timestamp >= ?
                GROUP BY agent_name
                HAVING failures > 0

                ORDER BY failure_rate DESC
                """,
                (since, since)
            ).fetchall()
            return [dict(row) for row in rows]

    # =========================================================================
    # MAINTENANCE OPERATIONS
    # =========================================================================

    def cleanup(self, days: int = 30):
        """Remove events older than specified days."""
        cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()
        with self._get_connection() as conn:
            conn.execute("DELETE FROM skill_events WHERE timestamp < ?", (cutoff,))
            conn.execute("DELETE FROM agent_events WHERE timestamp < ?", (cutoff,))
            conn.execute("DELETE FROM flow_events WHERE timestamp < ?", (cutoff,))
            conn.execute("DELETE FROM sessions WHERE ended_at < ?", (cutoff,))

    def get_database_stats(self) -> Dict:
        """Get database statistics."""
        with self._get_connection() as conn:
            stats = {}
            for table in ['skill_events', 'agent_events', 'flow_events', 'sessions']:
                row = conn.execute(f"SELECT COUNT(*) as count FROM {table}").fetchone()
                stats[table] = row['count']

            # Database file size
            if self.db_path.exists():
                stats['db_size_bytes'] = self.db_path.stat().st_size

            return stats


# CLI interface
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Metrics storage management")
    parser.add_argument("--cleanup", action="store_true", help="Clean up old events")
    parser.add_argument("--days", type=int, default=30, help="Days to keep (for cleanup)")
    parser.add_argument("--stats", action="store_true", help="Show database stats")
    args = parser.parse_args()

    storage = MetricsStorage()

    if args.cleanup:
        storage.cleanup(days=args.days)
        print(f"Cleaned up events older than {args.days} days")

    if args.stats:
        stats = storage.get_database_stats()
        print("Database Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
