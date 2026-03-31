import os
from contextlib import contextmanager
from langfuse import Langfuse
from langfuse.api.resources.commons.types.observation import Observation

class TraceWrapper:
    """Wrapper to provide backward compatibility with old Langfuse trace API"""
    def __init__(self, span):
        self.span = span
        self.id = span.id  # Provide access to span ID

    def observation(self, name: str, input=None, output=None, parent_observation_id=None):
        # Create an observation using the new API
        return self.span.start_observation(
            name=name,
            as_type='event',
            input=input,
            output=output
        )

class LangFuseWrapper:
    def __init__(self):
        self.langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "http://localhost:3000")
        )

    @contextmanager
    def create_trace(self, name: str, user_id: str = None, session_id: str = None):
        # Create a span using the new API and wrap it for backward compatibility
        with self.langfuse.start_as_current_span(
            name=name,
            metadata={"user_id": user_id, "session_id": session_id}
        ) as span:
            yield TraceWrapper(span)

    def create_observation(self, trace, name: str, input: dict = None, output: dict = None, parent_observation_id: str = None):
        return trace.observation(name=name, input=input, output=output, parent_observation_id=parent_observation_id)

    def log_metrics(self, observation: Observation, latency: float, reasoning_quality: float, tool_use_accuracy: float):
        observation.score(name="latency", value=latency)
        observation.score(name="reasoning_quality", value=reasoning_quality)
        observation.score(name="tool_use_accuracy", value=tool_use_accuracy)

# Singleton instance
langfuse_wrapper = LangFuseWrapper()