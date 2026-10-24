from pathlib import Path

from config import OS_NAME, VERSION, TOTAL_MEMORY_MB

from filesystem import FileSystemManager
from memory import MemoryManager
from processes import ProcessManager
from shell import MiniOSShell
from users import UserManager


def show_banner():
    print("=" * 48)
    print(f"{OS_NAME} v{VERSION}".center(48))
    print("=" * 48)
    print("    Command-Line Operating System Simulator")
    print()


def main():
    show_banner()

    project_directory = Path(__file__).resolve().parent
    try:
        user_manager = UserManager(project_directory / "data" / "users.json")
    except (OSError, ValueError) as exc:
        print(f"Startup error: {exc}")
        return

    if not user_manager.interactive_login():
        print("\nStartup cancelled. Goodbye!")
        return

    storage_directory = project_directory / "minios_storage"

    filesystem = FileSystemManager(storage_directory)
    process_manager = ProcessManager()
    memory_manager = MemoryManager(total_memory=TOTAL_MEMORY_MB)

    shell = MiniOSShell(
        user_manager=user_manager,
        filesystem=filesystem,
        process_manager=process_manager,
        memory_manager=memory_manager,
    )

    shell.start()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print(f"\nShutting down {OS_NAME}... Goodbye!")
