import os
from langfuse import Langfuse
from langfuse.api.resources.commons.types.observation import Observation

class LangFuseWrapper:
    def __init__(self):
        self.langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "http://localhost:3000")
        )

    def create_trace(self, name: str, user_id: str = None, session_id: str = None):
        return self.langfuse.trace(name=name, user_id=user_id, session_id=session_id)

    def create_observation(self, trace, name: str, input: dict = None, output: dict = None, parent_observation_id: str = None):
        return trace.observation(name=name, input=input, output=output, parent_observation_id=parent_observation_id)

    def log_metrics(self, observation: Observation, latency: float, reasoning_quality: float, tool_use_accuracy: float):
        observation.score(name="latency", value=latency)
        observation.score(name="reasoning_quality", value=reasoning_quality)
        observation.score(name="tool_use_accuracy", value=tool_use_accuracy)

# Singleton instance
langfuse_wrapper = LangFuseWrapper()