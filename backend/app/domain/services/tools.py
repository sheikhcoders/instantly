"""
External tool management service.
"""

import asyncio
import docker
from typing import Dict, List, Optional
from app.core.config import settings
from app.domain.models.base import ToolType

class ToolService:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.active_sandboxes: Dict[str, str] = {}  # task_id -> container_id

    async def create_sandbox(self, task_id: str, tools: List[ToolType]) -> str:
        """Create a new sandbox for a task."""
        container = self.docker_client.containers.run(
            settings.SANDBOX_IMAGE,
            detach=True,
            environment={
                "TASK_ID": task_id,
                "ENABLED_TOOLS": ",".join(tools),
            },
            mem_limit=settings.MAX_SANDBOX_MEMORY,
            cpu_quota=int(100000 * settings.SANDBOX_CPU_LIMIT),  # Docker uses microseconds
            network_mode="bridge",
            auto_remove=True
        )
        self.active_sandboxes[task_id] = container.id
        return container.id

    async def destroy_sandbox(self, task_id: str):
        """Destroy a task's sandbox."""
        if task_id in self.active_sandboxes:
            container_id = self.active_sandboxes[task_id]
            try:
                container = self.docker_client.containers.get(container_id)
                container.stop()
            except docker.errors.NotFound:
                pass
            finally:
                del self.active_sandboxes[task_id]

    async def execute_tool(self, task_id: str, tool_type: ToolType, command: Dict) -> Dict:
        """Execute a tool command in the sandbox."""
        if task_id not in self.active_sandboxes:
            raise ValueError(f"No active sandbox for task {task_id}")
        
        container_id = self.active_sandboxes[task_id]
        container = self.docker_client.containers.get(container_id)
        
        # Execute command in sandbox
        exec_id = container.exec_run(
            cmd=["python", "-c", f"import json; print(json.dumps({command}))"],
            detach=True
        )
        
        # Wait for result
        while True:
            exec_info = self.docker_client.api.exec_inspect(exec_id)
            if not exec_info["Running"]:
                break
            await asyncio.sleep(0.1)
        
        # Get output
        output = container.logs(stdout=True, stderr=True)
        return {"status": "success", "output": output.decode()}