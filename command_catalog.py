"""One command reference shared by shell help and the user manual."""
from dataclasses import dataclass
from typing import Optional
from textwrap import fill, wrap


@dataclass(frozen=True)
class Command:
    name: str
    category: str
    required: bool
    syntax: str
    purpose: str
    example: str
    result: str
    notes: str
    min_args: int = 0
    max_args: Optional[int] = 0


CATEGORIES = ("General", "File Management", "Process Management",
              "Memory Management", "User Management")

COMMANDS = (
    Command("help", "General", True, "help [command]",
            "Display the grouped command list or detailed help for one command.",
            "help allocate", "Shows the purpose, syntax, example and notes for allocate.",
            "Use help by itself for the full list, organized by category.",
            0, 1),
    Command("clear", "General", True, "clear",
            "Clear the Command Prompt display.",
            "clear", "The screen is cleared and the MiniOS prompt returns.",
            "Files, processes, memory and command history are preserved."),
    Command("date", "General", True, "date",
            "Show today's date using the computer's local clock.",
            "date", "Displays the weekday, month, day and year.",
            "This reads the host clock; it does not change the Windows date."),
    Command("time", "General", True, "time",
            "Show the current local time in 12-hour format.",
            "time", "Displays hours, minutes, seconds and AM or PM.",
            "This reads the host clock; it does not change the Windows time."),
    Command("whoami", "General", True, "whoami",
            "Identify the currently signed-in MiniOS account.",
            "whoami", "Current User: admin (when signed in as admin).",
            "This is the simulated MiniOS user, not the Windows account."),
    Command("systeminfo", "General", True, "systeminfo",
            "Show the MiniOS name, group, version, virtual hardware, memory and current user.",
            "systeminfo", "Includes MiniOSAlphaSC1063 and 131,072 MB (128.00 GB) of simulated RAM.",
            "CPU and architecture describe the simulation. Host Python is the installed interpreter version."),
    Command("exit", "General", True, "exit",
            "Shut down MiniOS and return to Windows CMD.",
            "exit", "Shutting down MiniOSAlphaSC1063... Goodbye!",
            "Files remain saved. Simulated processes, memory usage and history reset on the next launch."),
    Command("history", "General", False, "history",
            "List commands entered during the current application session.",
            "history", "Displays numbered commands, including the history command itself.",
            "History is kept in memory and resets after exit. Password prompts are never added to it."),
    Command("echo", "General", False, "echo [text]",
            "Display text without creating a file.",
            'echo "Welcome to Group Alpha"',
            "Welcome to Group Alpha",
            "With no text, echo prints a blank line. MiniOS does not support CMD redirection or pipelines.",
            0, None),
    Command("calculator", "General", False, "calculator <number> <operator> <number>",
            "Calculate with +, -, *, /, %, or **.",
            "calculator 12 * 5", "Result: 60",
            "% computes a remainder; ** computes a power. Negative and decimal numbers are accepted. Division by zero and non-finite or complex results are rejected. Use calculator directly: run calculator only creates a simulated process.",
            3, 3),
    Command("status", "General", False, "status",
            "Show a short summary of the current session.",
            "status", "Displays the user, directory, running process count and total, used and free memory.",
            "Use systeminfo for the full system profile, process for process details, or memory for RAM details."),
    Command("version", "General", False, "version",
            "Display the MiniOS application name and version.",
            "version", "MiniOSAlphaSC1063 v1.0",
            "This is the project version, not the Windows or Python version."),
    Command("shutdown", "General", False, "shutdown",
            "Shut down MiniOS; an alias for exit.",
            "shutdown", "Displays a goodbye message and returns to CMD.",
            "Only MiniOS closes. The computer and Windows remain running."),
    Command("dir", "File Management", True, "dir [path]",
            "List files and subfolders in the selected directory.",
            "dir Documents", "Displays folder names and file sizes in bytes.",
            "Without a path, lists the current directory. Folders appear before files. Paths must stay inside MiniOS storage.",
            0, 1),
    Command("mkdir", "File Management", True, "mkdir <folder>",
            "Create a folder in MiniOS storage.",
            'mkdir "Project Notes"', "Directory created.",
            "Quotes allow spaces in names. Missing parent folders are also created. Existing names produce an error.",
            1, 1),
    Command("create", "File Management", True, "create <file> [text]",
            "Create a UTF-8 text file, optionally with initial content.",
            'create notes.txt "Operating Systems Final Project"', "File created.",
            "Without text, creates an empty file. Existing files are not overwritten. Missing parent folders are created automatically.",
            1, None),
    Command("read", "File Management", True, "read <file>",
            "Display a UTF-8 text file's contents.",
            "read notes.txt", "Displays the text saved in notes.txt.",
            "Empty files display [File is empty.]. Missing files, folders and non-UTF-8 files produce an error.",
            1, 1),
    Command("delete", "File Management", True, "delete <file>",
            "Permanently remove a file from MiniOS storage.",
            "delete notes.txt", "File deleted.",
            "Deletion has no undo. This command accepts files only; use rmdir for an empty folder.",
            1, 1),
    Command("write", "File Management", False, "write <file> <text>",
            "Replace all contents of an existing text file.",
            'write notes.txt "Updated project notes"', "Text written to notes.txt.",
            'The file must exist. Earlier content is replaced. Use write notes.txt "" to empty a file, or append to preserve its content.',
            2, None),
    Command("rename", "File Management", False, "rename <old> <new>",
            "Rename a file or folder, or move it to an existing folder within MiniOS storage.",
            "rename notes.txt final_notes.txt", "Renamed successfully.",
            "The source must exist and the destination must not exist. The destination's parent must exist. The storage root, current directory and its ancestors cannot be renamed.",
            2, 2),
    Command("cd", "File Management", False, "cd <directory>",
            "Change the current MiniOS directory.",
            "cd Documents", "Current directory: \\Documents",
            "Use cd .. for the parent and cd / for the storage root. Both / and backslash separators are accepted. Moving above the root is blocked.",
            1, 1),
    Command("append", "File Management", False, "append <file> <text>",
            "Add text to the end of an existing file.",
            'append notes.txt " - Group Alpha"', "Text appended to notes.txt.",
            "The file must exist. Text is appended exactly as entered, without adding a space or newline automatically. Include a leading space inside quotes when needed.",
            2, None),
    Command("pwd", "File Management", False, "pwd",
            "Show the current MiniOS directory.",
            "pwd", "Displays \\ at the root or a path such as \\Documents.",
            "This is a virtual path relative to minios_storage, not a Windows drive path."),
    Command("rmdir", "File Management", False, "rmdir <directory>",
            "Remove an empty folder.",
            "rmdir Documents", "Directory deleted.",
            "Delete the folder's files and empty subfolders first. The storage root, current directory and its ancestors cannot be deleted. There is no recursive deletion option.",
            1, 1),
    Command("process", "Process Management", True, "process",
            "Display the simulated running-process table.",
            "process", "Lists PID, process name and RUNNING status, or No running processes.",
            "Only processes created by run appear here. Windows programs are not listed."),
    Command("run", "Process Management", True, "run <name>",
            "Create a simulated process record with a unique PID.",
            "run calculator", "Process started. PID: 1; Name: calculator; Status: RUNNING.",
            "Any nonempty name is accepted, including a quoted name with spaces. PIDs start at 1 and increase within the session. This does not open a real program or automatically allocate simulated memory.",
            1, None),
    Command("kill", "Process Management", True, "kill <pid>",
            "Terminate a simulated process by its PID.",
            "kill 1", "Process 1 terminated.",
            "Use process to find a PID. The PID must be a positive whole number and identify an existing process. Manually allocated memory is unaffected.",
            1, 1),
    Command("memory", "Memory Management", True, "memory",
            "Show total, used and free simulated RAM.",
            "memory", "On a fresh launch: total 131,072 MB, used 0 MB, free 131,072 MB.",
            "MiniOS uses the classroom convention 1 GB = 1024 MB; technically these are GiB and MiB. Thus 128 GB = 131,072 MB. No real RAM is reserved."),
    Command("allocate", "Memory Management", True, "allocate <MB>",
            "Increase the amount of simulated RAM in use.",
            "allocate 4096", "4096 MB allocated. Used becomes 4,096 MB; free becomes 126,976 MB on a fresh session.",
            "Enter a positive whole number in MB, without commas or units. Requests exceeding free memory are rejected and leave memory unchanged.",
            1, 1),
    Command("free", "Memory Management", True, "free <MB>",
            "Release previously allocated simulated RAM.",
            "free 1024", "1024 MB released. After allocate 4096, used becomes 3,072 MB and free becomes 128,000 MB.",
            "Enter a positive whole number in MB. You cannot release more than is currently allocated. Memory is one shared pool, separate from process records.",
            1, 1),
    Command("users", "User Management", False, "users",
            "List all available MiniOS usernames.",
            "users", "Lists demo accounts and added users; marks the signed-in account with (current).",
            "Passwords are not displayed. Both demo accounts can use the same commands and shared file area."),
    Command("login", "User Management", False, "login <username>",
            "Switch to another account after verifying its password.",
            "login student", "Prompts for a password; after student, welcomes student and updates the prompt.",
            "Do not place a password in the command. It is requested privately and does not appear in history. Invalid credentials preserve the current account. Files, directory, processes, memory and history stay in the same session.",
            1, 1),
    Command("logout", "User Management", False, "logout",
            "Sign out and display the login screen again.",
            "logout", "Logs out the current user and requests new credentials.",
            "Enter another account to continue in the same session, or type exit at the Username prompt to close MiniOS. Session state is preserved when another user logs in."),
    Command("adduser", "User Management", False, "adduser <username>",
            "Create a user account that remains available after restarting MiniOS.",
            "adduser ralph", "Asks for a new password and confirmation, then creates ralph.",
            "Usernames must be 3-24 letters, numbers or underscores; exit is reserved. Passwords must be at least 4 characters and not only spaces. Duplicate names and mismatched passwords are rejected. All signed-in users can add accounts; files and commands are shared. Passwords are requested privately, never in the command. Accounts are saved automatically in data/users.json.",
            1, 1),
)

BY_NAME = {command.name: command for command in COMMANDS}


def detail_text(command: Command) -> str:
    lines = [f"{command.name} - {command.category}"]
    for label, value in (("Purpose", command.purpose), ("Syntax", command.syntax),
                         ("Example", command.example), ("Result", command.result),
                         ("Notes", command.notes)):
        lines.append(fill(value, width=88, initial_indent=f"{label + ':':<9}",
                          subsequent_indent=" " * 9))
    return "\n".join(lines)


def help_text() -> str:
    lines = ["MiniOSAlphaSC1063 - Command Guide", "=" * 48,
             "Type help <command> for an example and detailed guidance."]
    for category in CATEGORIES:
        lines.extend(["", category.upper()])
        for item in (c for c in COMMANDS if c.category == category):
            description = wrap(item.purpose, width=48)
            lines.append(f"  {item.syntax:<42} {description[0]}")
            lines.extend(" " * 45 + line for line in description[1:])
    lines.extend(["", 'Tip: Quote names or text with spaces, e.g. mkdir "Project Notes".',
                  "Memory amounts are whole MB, e.g. allocate 4096."])
    return "\n".join(lines)
