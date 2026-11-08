"""Common interface for automated project checks."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseCheck(ABC):
    name: str

    @abstractmethod
    def run_check(self) -> Optional[bool]:
        """Run the check, preserving its optional success result."""
