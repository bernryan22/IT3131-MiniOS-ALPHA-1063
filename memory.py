from config import TOTAL_MEMORY_MB, format_memory


class MemoryManager:
    """Simulates RAM allocation without touching the computer's real memory."""

    def __init__(self, total_memory: int = TOTAL_MEMORY_MB):
        self.total_memory = total_memory
        self.used_memory = 0

    @property
    def free_memory(self) -> int:
        return self.total_memory - self.used_memory

    def allocate(self, amount: int):
        if amount <= 0:
            return False, "Memory amount must be greater than 0 MB."

        if amount > self.free_memory:
            return (
                False,
                f"Not enough free memory. Only {self.free_memory} MB is available.",
            )

        self.used_memory += amount
        return True, f"{amount} MB allocated."

    def free(self, amount: int):
        if amount <= 0:
            return False, "Memory amount must be greater than 0 MB."

        if amount > self.used_memory:
            return (
                False,
                f"Cannot release {amount} MB because only {self.used_memory} MB is allocated.",
            )

        self.used_memory -= amount
        return True, f"{amount} MB released."

    def status_text(self) -> str:
        return (
            "Memory Status\n"
            "------------------------\n"
            f"Total Memory: {format_memory(self.total_memory)}\n"
            f"Used Memory:  {format_memory(self.used_memory)}\n"
            f"Free Memory:  {format_memory(self.free_memory)}"
        )
