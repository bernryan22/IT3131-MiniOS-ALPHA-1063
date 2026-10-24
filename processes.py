from dataclasses import dataclass


@dataclass
class SimulatedProcess:
    pid: int
    name: str
    status: str = "RUNNING"


class ProcessManager:
    """Simulates process creation, listing, and termination."""

    def __init__(self):
        self._processes = {}
        self._next_pid = 1

    def run(self, name: str):
        name = name.strip()
        if not name:
            return False, "Process name cannot be empty.", None

        process = SimulatedProcess(pid=self._next_pid, name=name)
        self._processes[process.pid] = process
        self._next_pid += 1

        message = (
            "Process started.\n\n"
            f"PID: {process.pid}\n"
            f"Name: {process.name}\n"
            f"Status: {process.status}"
        )
        return True, message, process

    def kill(self, pid: int):
        process = self._processes.get(pid)

        if process is None:
            return False, "Process does not exist."

        del self._processes[pid]
        return True, f"Process {pid} terminated."

    def list_processes(self):
        return list(self._processes.values())

    def process_table(self) -> str:
        processes = self.list_processes()

        if not processes:
            return "No running processes."

        rows = [
            "PID    NAME                         STATUS",
            "-----  ---------------------------  ----------",
        ]

        for process in processes:
            rows.append(
                f"{process.pid:<5}  {process.name[:27]:<27}  {process.status}"
            )

        return "\n".join(rows)

    @property
    def running_count(self):
        return len(self._processes)
