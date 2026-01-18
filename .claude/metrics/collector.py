"""
Metrics collector for framework usage analytics.

Provides a simple API for recording skill, agent, and flow events.
"""

import time
import uuid
from datetime import datetime
from typing import Dict, Optional, Any
from contextlib import contextmanager
from pathlib import Path

from .storage import MetricsStorage


class MetricsCollector:
    """
    Collects and records framework usage metrics.

    Usage:
        collector = MetricsCollector()

        # Simple event recording
        collector.record_skill_invocation("senior-backend")

        # With context manager for automatic duration
        with collector.track_skill("senior-backend") as tracker:
            # ... skill execution ...
            tracker.set_metadata({"trigger": "user_request"})
        # Duration automatically recorded on exit
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern for global collector."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, storage: Optional[MetricsStorage] = None):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.storage = storage or MetricsStorage()
        self._session_id = None
        self._enabled = True

    @property
    def session_id(self) -> str:
        """Get or create session ID."""
        if self._session_id is None:
            self._session_id = str(uuid.uuid4())[:8]
        return self._session_id

    def start_session(self, project_path: Optional[str] = None):
        """Start a new metrics session."""
        self._session_id = str(uuid.uuid4())[:8]
        self.storage.start_session(
            self.session_id,
            project_path=project_path,
            metadata={"started_at": datetime.utcnow().isoformat()}
        )

    def end_session(self):
        """End the current session."""
        if self._session_id:
            self.storage.end_session(self._session_id)
            self._session_id = None

    def enable(self):
        """Enable metrics collection."""
        self._enabled = True

    def disable(self):
        """Disable metrics collection."""
        self._enabled = False

    # =========================================================================
    # SKILL METRICS
    # =========================================================================

    def record_skill_invocation(
        self,
        skill_name: str,
        metadata: Optional[Dict] = None
    ):
        """Record a skill invocation event."""
        if not self._enabled:
            return
        self.storage.record_skill_event(
            skill_name=skill_name,
            event_type="invoked",
            metadata=metadata,
            session_id=self.session_id
        )

    def record_skill_completion(
        self,
        skill_name: str,
        duration_ms: Optional[int] = None,
        metadata: Optional[Dict] = None
    ):
        """Record a skill completion event."""
        if not self._enabled:
            return
        self.storage.record_skill_event(
            skill_name=skill_name,
            event_type="completed",
            duration_ms=duration_ms,
            metadata=metadata,
            session_id=self.session_id
        )

    def record_skill_failure(
        self,
        skill_name: str,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None
    ):
        """Record a skill failure event."""
        if not self._enabled:
            return
        self.storage.record_skill_event(
            skill_name=skill_name,
            event_type="failed",
            duration_ms=duration_ms,
            metadata={"error": error} if error else None,
            session_id=self.session_id
        )

    @contextmanager
    def track_skill(self, skill_name: str):
        """
        Context manager for tracking skill execution.

        Usage:
            with collector.track_skill("senior-backend") as tracker:
                # ... skill execution ...
                tracker.set_metadata({"key": "value"})
        """
        tracker = _ExecutionTracker(skill_name, "skill", self)
        self.record_skill_invocation(skill_name)
        try:
            yield tracker
            self.record_skill_completion(
                skill_name,
                duration_ms=tracker.duration_ms,
                metadata=tracker.metadata
            )
        except Exception as e:
            self.record_skill_failure(
                skill_name,
                error=str(e),
                duration_ms=tracker.duration_ms
            )
            raise

    # =========================================================================
    # AGENT METRICS
    # =========================================================================

    def record_agent_invocation(
        self,
        agent_name: str,
        feature_name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Record an agent invocation event."""
        if not self._enabled:
            return
        self.storage.record_agent_event(
            agent_name=agent_name,
            event_type="invoked",
            metadata=metadata,
            session_id=self.session_id,
            feature_name=feature_name
        )

    def record_agent_completion(
        self,
        agent_name: str,
        duration_ms: Optional[int] = None,
        feature_name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Record an agent completion event."""
        if not self._enabled:
            return
        self.storage.record_agent_event(
            agent_name=agent_name,
            event_type="completed",
            duration_ms=duration_ms,
            metadata=metadata,
            session_id=self.session_id,
            feature_name=feature_name
        )

    def record_agent_blocked(
        self,
        agent_name: str,
        blocked_by: str,
        feature_name: Optional[str] = None
    ):
        """Record an agent blocked event."""
        if not self._enabled:
            return
        self.storage.record_agent_event(
            agent_name=agent_name,
            event_type="blocked",
            metadata={"blocked_by": blocked_by},
            session_id=self.session_id,
            feature_name=feature_name
        )

    def record_agent_failure(
        self,
        agent_name: str,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None,
        feature_name: Optional[str] = None
    ):
        """Record an agent failure event."""
        if not self._enabled:
            return
        self.storage.record_agent_event(
            agent_name=agent_name,
            event_type="failed",
            duration_ms=duration_ms,
            metadata={"error": error} if error else None,
            session_id=self.session_id,
            feature_name=feature_name
        )

    @contextmanager
    def track_agent(self, agent_name: str, feature_name: Optional[str] = None):
        """Context manager for tracking agent execution."""
        tracker = _ExecutionTracker(agent_name, "agent", self)
        self.record_agent_invocation(agent_name, feature_name)
        try:
            yield tracker
            self.record_agent_completion(
                agent_name,
                duration_ms=tracker.duration_ms,
                feature_name=feature_name,
                metadata=tracker.metadata
            )
        except Exception as e:
            self.record_agent_failure(
                agent_name,
                error=str(e),
                duration_ms=tracker.duration_ms,
                feature_name=feature_name
            )
            raise

    # =========================================================================
    # FLOW METRICS
    # =========================================================================

    def record_flow_start(
        self,
        flow_name: str,
        feature_name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Record a flow start event."""
        if not self._enabled:
            return
        self.storage.record_flow_event(
            flow_name=flow_name,
            event_type="started",
            metadata=metadata,
            session_id=self.session_id,
            feature_name=feature_name
        )

    def record_flow_phase(
        self,
        flow_name: str,
        phase: str,
        duration_ms: Optional[int] = None,
        feature_name: Optional[str] = None
    ):
        """Record a flow phase completion."""
        if not self._enabled:
            return
        self.storage.record_flow_event(
            flow_name=flow_name,
            event_type="phase_completed",
            phase=phase,
            duration_ms=duration_ms,
            session_id=self.session_id,
            feature_name=feature_name
        )

    def record_flow_completion(
        self,
        flow_name: str,
        duration_ms: Optional[int] = None,
        feature_name: Optional[str] = None,
        metadata: Optional[Dict] = None
    ):
        """Record a flow completion event."""
        if not self._enabled:
            return
        self.storage.record_flow_event(
            flow_name=flow_name,
            event_type="completed",
            duration_ms=duration_ms,
            metadata=metadata,
            session_id=self.session_id,
            feature_name=feature_name
        )

    def record_flow_failure(
        self,
        flow_name: str,
        phase: Optional[str] = None,
        error: Optional[str] = None,
        duration_ms: Optional[int] = None,
        feature_name: Optional[str] = None
    ):
        """Record a flow failure event."""
        if not self._enabled:
            return
        self.storage.record_flow_event(
            flow_name=flow_name,
            event_type="failed",
            phase=phase,
            duration_ms=duration_ms,
            metadata={"error": error} if error else None,
            session_id=self.session_id,
            feature_name=feature_name
        )

    @contextmanager
    def track_flow(self, flow_name: str, feature_name: Optional[str] = None):
        """Context manager for tracking flow execution."""
        tracker = _ExecutionTracker(flow_name, "flow", self)
        self.record_flow_start(flow_name, feature_name)
        try:
            yield tracker
            self.record_flow_completion(
                flow_name,
                duration_ms=tracker.duration_ms,
                feature_name=feature_name,
                metadata=tracker.metadata
            )
        except Exception as e:
            self.record_flow_failure(
                flow_name,
                error=str(e),
                duration_ms=tracker.duration_ms,
                feature_name=feature_name
            )
            raise


class _ExecutionTracker:
    """Helper class for tracking execution duration and metadata."""

    def __init__(self, name: str, type_: str, collector: MetricsCollector):
        self.name = name
        self.type = type_
        self.collector = collector
        self.start_time = time.time()
        self.metadata: Dict[str, Any] = {}

    @property
    def duration_ms(self) -> int:
        """Get elapsed time in milliseconds."""
        return int((time.time() - self.start_time) * 1000)

    def set_metadata(self, metadata: Dict[str, Any]):
        """Set metadata for this execution."""
        self.metadata.update(metadata)


# Global collector instance
def get_collector() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return MetricsCollector()
