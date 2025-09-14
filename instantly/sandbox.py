"""
Sandbox environment for secure tool execution.
"""

import os
import resource
import asyncio
from typing import Any, Callable, Dict, Optional
from contextlib import contextmanager

class ResourceLimits:
    """Resource limits for sandboxed execution."""
    
    def __init__(
        self,
        max_memory: int = 512 * 1024 * 1024,  # 512MB
        max_cpu_time: int = 30,  # 30 seconds
        max_file_size: int = 50 * 1024 * 1024,  # 50MB
    ):
        self.max_memory = max_memory
        self.max_cpu_time = max_cpu_time
        self.max_file_size = max_file_size

class SandboxContext:
    """Context for sandboxed tool execution."""
    
    def __init__(
        self,
        working_dir: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        resource_limits: Optional[ResourceLimits] = None
    ):
        self.working_dir = working_dir or os.getcwd()
        self.env_vars = env_vars or {}
        self.resource_limits = resource_limits or ResourceLimits()
        self._original_dir = None
        self._original_env = None

    @contextmanager
    def __enter__(self):
        """Enter sandbox context with resource limits."""
        self._original_dir = os.getcwd()
        self._original_env = dict(os.environ)
        
        # Set working directory
        os.chdir(self.working_dir)
        
        # Set environment variables
        os.environ.update(self.env_vars)
        
        # Set resource limits
        resource.setrlimit(resource.RLIMIT_AS, (self.resource_limits.max_memory, self.resource_limits.max_memory))
        resource.setrlimit(resource.RLIMIT_CPU, (self.resource_limits.max_cpu_time, self.resource_limits.max_cpu_time))
        resource.setrlimit(resource.RLIMIT_FSIZE, (self.resource_limits.max_file_size, self.resource_limits.max_file_size))
        
        yield self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit sandbox context and restore original state."""
        # Restore working directory
        if self._original_dir:
            os.chdir(self._original_dir)
        
        # Restore environment variables
        if self._original_env:
            os.environ.clear()
            os.environ.update(self._original_env)

class Sandbox:
    """Sandbox for secure tool execution."""
    
    @staticmethod
    async def run(
        func: Callable,
        *args,
        working_dir: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None,
        resource_limits: Optional[ResourceLimits] = None,
        **kwargs
    ) -> Any:
        """
        Run a function in a sandboxed environment.
        
        Args:
            func: Function to execute
            *args: Function arguments
            working_dir: Working directory for execution
            env_vars: Environment variables
            resource_limits: Resource limits
            **kwargs: Additional function keyword arguments
            
        Returns:
            Result of the function execution
        """
        context = SandboxContext(
            working_dir=working_dir,
            env_vars=env_vars,
            resource_limits=resource_limits
        )
        
        with context:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            
            return result