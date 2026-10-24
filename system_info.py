from datetime import datetime
import platform
from config import OS_NAME, VERSION, GROUP_NAME, format_memory


class SystemInfo:
    """Provides simulated MiniOS information and simple date/time helpers."""

    OS_NAME = OS_NAME
    VERSION = VERSION
    ARCHITECTURE = "64-bit"
    CPU = "Virtual CPU"

    @classmethod
    def current_date(cls):
        return datetime.now().strftime("%A, %B %d, %Y")

    @classmethod
    def current_time(cls):
        return datetime.now().strftime("%I:%M:%S %p")

    @classmethod
    def info_text(cls, username: str, total_memory: int):
        return (
            "================================================\n"
            "               SYSTEM INFORMATION\n"
            "================================================\n"
            f"OS Name:      {cls.OS_NAME}\n"
            f"Group:        {GROUP_NAME}\n"
            f"Version:      {cls.VERSION}\n"
            f"Architecture: {cls.ARCHITECTURE}\n"
            f"CPU:          {cls.CPU}\n"
            f"Memory:       {format_memory(total_memory)}\n"
            f"User:         {username or 'None'}\n"
            f"Host Python:  {platform.python_version()}\n"
            "================================================"
        )
