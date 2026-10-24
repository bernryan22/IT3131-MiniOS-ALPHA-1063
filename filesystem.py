from pathlib import Path, PureWindowsPath


class FileSystemManager:
    """
    Provides a safe MiniOS file area.

    All operations are restricted to minios_storage so a user cannot use
    MiniOS commands to modify arbitrary files elsewhere on the computer.
    """

    def __init__(self, root: Path):
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.current_dir = self.root

    def _safe_path(self, user_path: str = ".") -> Path:
        user_path = user_path.strip() or "."
        if PureWindowsPath(user_path).drive or user_path.startswith("//"):
            raise ValueError("Use a MiniOS path, not a Windows drive or network path.")
        normalized = user_path.replace("\\", "/")
        if normalized.startswith("/"):
            candidate = (self.root / normalized.lstrip("/")).resolve()
        else:
            candidate = (self.current_dir / normalized).resolve()

        if candidate != self.root and self.root not in candidate.parents:
            raise ValueError("Access outside MiniOS storage is not allowed.")

        return candidate

    def _display_path(self, path: Path = None) -> str:
        path = (path or self.current_dir).resolve()
        if path == self.root:
            return "\\"

        relative = path.relative_to(self.root)
        return "\\" + str(relative).replace("/", "\\")

    def pwd(self) -> str:
        return self._display_path()

    def change_directory(self, target: str):
        try:
            path = self._safe_path(target)
        except ValueError as exc:
            return False, str(exc)

        if not path.exists():
            return False, "Directory does not exist."

        if not path.is_dir():
            return False, "Target is not a directory."

        self.current_dir = path
        return True, f"Current directory: {self._display_path()}"

    def list_directory(self, target: str = "."):
        try:
            path = self._safe_path(target)
        except ValueError as exc:
            return False, str(exc)

        if not path.exists():
            return False, "Directory does not exist."

        if not path.is_dir():
            return False, "Target is not a directory."

        entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))

        lines = [
            f"Directory of {self._display_path(path)}",
            "",
            f"{'TYPE':<8} {'SIZE':>10}  NAME",
            f"{'-' * 8} {'-' * 10}  {'-' * 24}",
        ]

        if not entries:
            lines.append("<empty>")
        else:
            for entry in entries:
                if entry.is_dir():
                    lines.append(f"{'<DIR>':<8} {'':>10}  {entry.name}")
                else:
                    lines.append(f"{'<FILE>':<8} {entry.stat().st_size:>10}  {entry.name}")

        return True, "\n".join(lines)

    def make_directory(self, name: str):
        try:
            path = self._safe_path(name)
        except ValueError as exc:
            return False, str(exc)

        if path.exists():
            return False, "A file or directory with that name already exists."

        try:
            path.mkdir(parents=True)
            return True, "Directory created."
        except OSError as exc:
            return False, f"Could not create directory: {exc}"

    def create_file(self, name: str, content: str = ""):
        try:
            path = self._safe_path(name)
        except ValueError as exc:
            return False, str(exc)

        if path.exists():
            return False, "File already exists."

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            return True, "File created."
        except OSError as exc:
            return False, f"Could not create file: {exc}"

    def read_file(self, name: str):
        try:
            path = self._safe_path(name)
        except ValueError as exc:
            return False, str(exc)

        if not path.exists():
            return False, "File does not exist."

        if not path.is_file():
            return False, "Target is not a file."

        try:
            content = path.read_text(encoding="utf-8")
            return True, content if content else "[File is empty.]"
        except UnicodeDecodeError:
            return False, "File is not a readable UTF-8 text file."
        except OSError as exc:
            return False, f"Could not read file: {exc}"

    def write_file(self, name: str, content: str, append: bool = False):
        try:
            path = self._safe_path(name)
        except ValueError as exc:
            return False, str(exc)

        if not path.exists():
            return False, "File does not exist."

        if not path.is_file():
            return False, "Target is not a file."

        try:
            if append:
                with path.open("a", encoding="utf-8") as file:
                    file.write(content)
            else:
                path.write_text(content, encoding="utf-8")

            action = "appended to" if append else "written to"
            return True, f"Text {action} {path.name}."
        except OSError as exc:
            return False, f"Could not write file: {exc}"

    def delete_file(self, name: str):
        try:
            path = self._safe_path(name)
        except ValueError as exc:
            return False, str(exc)

        if not path.exists():
            return False, "File does not exist."

        if not path.is_file():
            return False, "Target is a directory. Use 'rmdir' for directories."

        try:
            path.unlink()
            return True, "File deleted."
        except OSError as exc:
            return False, f"Could not delete file: {exc}"

    def remove_directory(self, name: str):
        try:
            path = self._safe_path(name)
        except ValueError as exc:
            return False, str(exc)

        if path == self.root:
            return False, "The MiniOS storage root cannot be deleted."

        if not path.exists():
            return False, "Directory does not exist."

        if not path.is_dir():
            return False, "Target is not a directory."

        if path == self.current_dir or path in self.current_dir.parents:
            return False, "Cannot delete the current directory or one of its parent directories."

        try:
            if any(path.iterdir()):
                return False, "Directory is not empty. Delete its contents first."
            path.rmdir()
            return True, "Directory deleted."
        except OSError as exc:
            return False, f"Could not delete directory: {exc}"

    def rename(self, old_name: str, new_name: str):
        try:
            old_path = self._safe_path(old_name)
            new_path = self._safe_path(new_name)
        except ValueError as exc:
            return False, str(exc)

        if not old_path.exists():
            return False, "Source file or directory does not exist."

        if old_path == self.root or old_path == self.current_dir or old_path in self.current_dir.parents:
            return False, "Cannot rename the storage root, current directory or its ancestors."
        if new_path.exists():
            return False, "Destination name already exists."
        if not new_path.parent.is_dir():
            return False, "Destination parent directory does not exist."

        try:
            old_path.rename(new_path)
            return True, "Renamed successfully."
        except OSError as exc:
            return False, f"Could not rename item: {exc}"
