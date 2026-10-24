import shlex
import math

from command_catalog import BY_NAME, detail_text, help_text
from config import OS_NAME, format_memory
from getpass import getpass

from system_info import SystemInfo
from utils import clear_screen


HELP_TEXT = help_text()

class MiniOSShell:
    def __init__(self, user_manager, filesystem, process_manager, memory_manager):
        self.user_manager = user_manager
        self.filesystem = filesystem
        self.process_manager = process_manager
        self.memory_manager = memory_manager
        self.running = True
        self.history = []

    def prompt(self):
        user = self.user_manager.current_user or "guest"
        path = self.filesystem.pwd()
        return f"{user}@{OS_NAME}:{path}> "

    def start(self):
        print("\nWelcome! Type help for all commands or help <command> for guidance.")
        print("Example: help create\n")

        while self.running:
            try:
                raw = input(self.prompt()).strip()
            except (EOFError, KeyboardInterrupt):
                self._cmd_exit([])
                break

            if not raw:
                continue

            self.history.append(raw)
            self.execute(raw)

    def execute(self, raw: str):
        try:
            parts = shlex.split(raw, posix=False)
        except ValueError as exc:
            self._error(f"Invalid command syntax: {exc}")
            return

        if not parts:
            return

        command = parts[0].lower()
        args = [self._strip_matching_quotes(arg) for arg in parts[1:]]

        commands = {
            "help": self._cmd_help,
            "clear": self._cmd_clear,
            "date": self._cmd_date,
            "time": self._cmd_time,
            "whoami": self._cmd_whoami,
            "systeminfo": self._cmd_systeminfo,
            "status": self._cmd_status,
            "version": self._cmd_version,
            "history": self._cmd_history,
            "echo": self._cmd_echo,
            "calculator": self._cmd_calculator,
            "dir": self._cmd_dir,
            "mkdir": self._cmd_mkdir,
            "create": self._cmd_create,
            "read": self._cmd_read,
            "write": self._cmd_write,
            "append": self._cmd_append,
            "delete": self._cmd_delete,
            "rename": self._cmd_rename,
            "cd": self._cmd_cd,
            "pwd": self._cmd_pwd,
            "rmdir": self._cmd_rmdir,
            "process": self._cmd_process,
            "run": self._cmd_run,
            "kill": self._cmd_kill,
            "memory": self._cmd_memory,
            "allocate": self._cmd_allocate,
            "free": self._cmd_free,
            "users": self._cmd_users,
            "adduser": self._cmd_adduser,
            "login": self._cmd_login,
            "logout": self._cmd_logout,
            "exit": self._cmd_exit,
            "shutdown": self._cmd_exit,
        }

        handler = commands.get(command)

        if handler is None:
            print("Unknown command.")
            print("Type 'help' to see the available commands.")
            return

        spec = BY_NAME[command]
        if len(args) < spec.min_args or (spec.max_args is not None and len(args) > spec.max_args):
            self._error("Incorrect number of arguments.")
            print(f"Syntax: {spec.syntax}")
            print(f"Tip: Type help {command} for an example.")
            return
        if self.user_manager.current_user is None and command not in ("help", "login", "exit", "shutdown"):
            self._error("Please log in before using this command.")
            return

        try:
            handler(args)
        except Exception as exc:
            # Last-resort protection so an unexpected input does not crash MiniOS.
            self._error(f"Command could not be completed: {exc}")

    @staticmethod
    def _strip_matching_quotes(value: str) -> str:
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            return value[1:-1]
        return value

    @staticmethod
    def _error(message: str):
        print(f"Error: {message}")

    @staticmethod
    def _require_args(args, count, syntax):
        if len(args) < count:
            print(f"Error: Missing argument(s).\nSyntax: {syntax}")
            return False
        return True

    # ---------- General commands ----------

    def _cmd_help(self, args):
        if not args:
            print(HELP_TEXT)
            return
        spec = BY_NAME.get(args[0].lower())
        if spec is None:
            self._error("Unknown help topic. Type help to see the command list.")
            return
        print(detail_text(spec))

    def _cmd_clear(self, args):
        clear_screen()

    def _cmd_date(self, args):
        print(SystemInfo.current_date())

    def _cmd_time(self, args):
        print(SystemInfo.current_time())

    def _cmd_whoami(self, args):
        print(self.user_manager.whoami())

    def _cmd_systeminfo(self, args):
        print(
            SystemInfo.info_text(
                self.user_manager.current_user,
                self.memory_manager.total_memory,
            )
        )

    def _cmd_status(self, args):
        print(f"{OS_NAME} Status")
        print("------------------------")
        print(f"User:              {self.user_manager.current_user}")
        print(f"Directory:         {self.filesystem.pwd()}")
        print(f"Running processes: {self.process_manager.running_count}")
        print(f"Memory total:      {format_memory(self.memory_manager.total_memory)}")
        print(f"Memory used:       {format_memory(self.memory_manager.used_memory)}")
        print(f"Memory free:       {format_memory(self.memory_manager.free_memory)}")

    def _cmd_version(self, args):
        print(f"{SystemInfo.OS_NAME} v{SystemInfo.VERSION}")

    def _cmd_history(self, args):
        if not self.history:
            print("No command history.")
            return

        for number, item in enumerate(self.history, start=1):
            print(f"{number:>3}: {item}")

    def _cmd_echo(self, args):
        print(" ".join(args))

    def _cmd_calculator(self, args):
        if not self._require_args(args, 3, "calculator <number> <operator> <number>"):
            return

        if len(args) != 3:
            self._error("Calculator accepts exactly three arguments.")
            print("Syntax: calculator <number> <operator> <number>")
            return

        left_text, operator, right_text = args

        try:
            left = float(left_text)
            right = float(right_text)
        except ValueError:
            self._error("Calculator values must be numbers.")
            return

        if not math.isfinite(left) or not math.isfinite(right):
            self._error("Calculator values must be finite numbers.")
            return

        operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "%": lambda a, b: a % b,
            "**": lambda a, b: a ** b,
        }

        operation = operations.get(operator)
        if operation is None:
            self._error("Unsupported operator. Use +, -, *, /, %, or **.")
            return

        if operator in ("/", "%") and right == 0:
            self._error("Division by zero is not allowed.")
            return

        try:
            result = operation(left, right)
        except (OverflowError, ZeroDivisionError):
            self._error("Calculation is too large or divides by zero.")
            return
        if isinstance(result, complex) or not math.isfinite(result):
            self._error("The result must be a finite real number.")
            return
        if isinstance(result, float) and result.is_integer():
            result = int(result)

        print(f"Result: {result}")

    # ---------- File management ----------

    def _cmd_dir(self, args):
        target = args[0] if args else "."
        ok, message = self.filesystem.list_directory(target)
        print(message if ok else f"Error: {message}")

    def _cmd_mkdir(self, args):
        if not self._require_args(args, 1, "mkdir <folder>"):
            return

        ok, message = self.filesystem.make_directory(args[0])
        print(message if ok else f"Error: {message}")

    def _cmd_create(self, args):
        if not self._require_args(args, 1, "create <file> [text]"):
            return

        content = " ".join(args[1:]) if len(args) > 1 else ""
        ok, message = self.filesystem.create_file(args[0], content)
        print(message if ok else f"Error: {message}")

    def _cmd_read(self, args):
        if not self._require_args(args, 1, "read <file>"):
            return

        ok, message = self.filesystem.read_file(args[0])
        print(message if ok else f"Error: {message}")

    def _cmd_write(self, args):
        if not self._require_args(args, 2, "write <file> <text>"):
            return

        ok, message = self.filesystem.write_file(
            args[0],
            " ".join(args[1:]),
            append=False,
        )
        print(message if ok else f"Error: {message}")

    def _cmd_append(self, args):
        if not self._require_args(args, 2, "append <file> <text>"):
            return

        ok, message = self.filesystem.write_file(
            args[0],
            " ".join(args[1:]),
            append=True,
        )
        print(message if ok else f"Error: {message}")

    def _cmd_delete(self, args):
        if not self._require_args(args, 1, "delete <file>"):
            return

        ok, message = self.filesystem.delete_file(args[0])
        print(message if ok else f"Error: {message}")

    def _cmd_rename(self, args):
        if not self._require_args(args, 2, "rename <old> <new>"):
            return

        ok, message = self.filesystem.rename(args[0], args[1])
        print(message if ok else f"Error: {message}")

    def _cmd_cd(self, args):
        if not self._require_args(args, 1, "cd <directory>"):
            return

        ok, message = self.filesystem.change_directory(args[0])
        print(message if ok else f"Error: {message}")

    def _cmd_pwd(self, args):
        print(self.filesystem.pwd())

    def _cmd_rmdir(self, args):
        if not self._require_args(args, 1, "rmdir <directory>"):
            return

        ok, message = self.filesystem.remove_directory(args[0])
        print(message if ok else f"Error: {message}")

    # ---------- Process management ----------

    def _cmd_process(self, args):
        print(self.process_manager.process_table())

    def _cmd_run(self, args):
        if not self._require_args(args, 1, "run <process-name>"):
            return

        name = " ".join(args)
        ok, message, _ = self.process_manager.run(name)
        print(message if ok else f"Error: {message}")

    def _cmd_kill(self, args):
        if not self._require_args(args, 1, "kill <pid>"):
            return

        try:
            pid = int(args[0])
        except ValueError:
            self._error("PID must be a whole number.")
            return

        if pid <= 0:
            self._error("PID must be a positive whole number.")
            return
        ok, message = self.process_manager.kill(pid)
        print(message if ok else f"Error: {message}")

    # ---------- Memory management ----------

    def _cmd_memory(self, args):
        print(self.memory_manager.status_text())

    def _parse_memory_amount(self, args, syntax):
        if not self._require_args(args, 1, syntax):
            return None

        try:
            return int(args[0])
        except ValueError:
            self._error("Memory amount must be a whole number in MB.")
            return None

    def _cmd_allocate(self, args):
        amount = self._parse_memory_amount(args, "allocate <MB>")
        if amount is None:
            return

        ok, message = self.memory_manager.allocate(amount)
        print(message if ok else f"Error: {message}")

    def _cmd_free(self, args):
        amount = self._parse_memory_amount(args, "free <MB>")
        if amount is None:
            return

        ok, message = self.memory_manager.free(amount)
        print(message if ok else f"Error: {message}")

    # ---------- User management ----------

    def _cmd_adduser(self, args):
        username = args[0]
        error = self.user_manager.new_username_error(username)
        if error:
            self._error(error)
            return
        password = getpass("New password: ")
        confirmation = getpass("Confirm password: ")
        if password != confirmation:
            self._error("Passwords do not match. User was not created.")
            return
        ok, message = self.user_manager.add_user(username, password)
        print(message if ok else f"Error: {message}")

    def _cmd_users(self, args):
        print("MiniOS Users:")
        for username in self.user_manager.list_users():
            marker = " (current)" if username == self.user_manager.current_user else ""
            print(f"- {username}{marker}")

    def _cmd_login(self, args):
        if not self._require_args(args, 1, "login <username>"):
            return

        username = args[0]
        password = getpass("Password: ")

        if self.user_manager.login(username, password):
            print(f"Login successful. Welcome, {username}!")
        else:
            self._error("Invalid username or password.")

    def _cmd_logout(self, args):
        old_user = self.user_manager.current_user
        self.user_manager.logout()
        print(f"{old_user} logged out.")

        if not self.user_manager.interactive_login():
            self._cmd_exit([])

    # ---------- Shutdown ----------

    def _cmd_exit(self, args):
        print(f"\nShutting down {OS_NAME}...")
        print("Goodbye!")
        self.running = False
