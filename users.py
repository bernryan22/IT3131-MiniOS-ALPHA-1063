from getpass import getpass
import hashlib
import hmac
import json
import os
from pathlib import Path
import re
import secrets
import tempfile
from config import OS_NAME
from typing import Optional


class UserManager:
    """Handles the simulated MiniOS user accounts and login session."""

    def __init__(self, accounts_file: Optional[Path] = None):
        # Required minimum: at least two accounts.
        # These are demo credentials for this school project.
        self._users = {
            "admin": "admin",
            "student": "student",
        }
        self.current_user: Optional[str] = None
        self.accounts_file = Path(accounts_file) if accounts_file is not None else None
        self._saved_users = {}
        self._load_accounts()

    def _load_accounts(self):
        """Load created accounts while keeping the demo accounts available."""
        if self.accounts_file is None or not self.accounts_file.exists():
            return
        try:
            data = json.loads(self.accounts_file.read_text(encoding="utf-8"))
            if not isinstance(data, dict) or data.get("version") != 1:
                raise ValueError("Unsupported accounts format.")
            records = data.get("users")
            if not isinstance(records, dict):
                raise ValueError("Invalid accounts list.")
            for username, record in records.items():
                if self.username_error(username) or username in self._users:
                    raise ValueError("Invalid saved username.")
                if not isinstance(record, dict):
                    raise ValueError("Invalid password record.")
                if not isinstance(record.get("salt"), str) or not re.fullmatch(r"[0-9a-f]{32}", record["salt"]):
                    raise ValueError("Invalid password salt.")
                if not isinstance(record.get("hash"), str) or not re.fullmatch(r"[0-9a-f]{64}", record["hash"]):
                    raise ValueError("Invalid password hash.")
            self._saved_users = records
        except (ValueError, TypeError, UnicodeError) as exc:
            raise ValueError(
                "Cannot read saved accounts in data/users.json. Restore a valid backup "
                "of that file before restarting MiniOS."
            ) from exc

    @staticmethod
    def username_error(username: str) -> Optional[str]:
        if not isinstance(username, str) or not re.fullmatch(r"[A-Za-z0-9_]{3,24}", username):
            return "Username must be 3-24 characters: letters, numbers or underscores."
        if username.lower() == "exit":
            return "The username 'exit' is reserved."
        return None

    def new_username_error(self, username: str) -> Optional[str]:
        error = self.username_error(username)
        if error:
            return error
        if username in self._users or username in self._saved_users:
            return "That username already exists. Choose another name."
        return None

    @staticmethod
    def _password_hash(password: str, salt: str) -> str:
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt), 200000
        ).hex()

    def add_user(self, username: str, password: str):
        error = self.new_username_error(username)
        if error:
            return False, error
        if len(password) < 4 or not password.strip():
            return False, "Password must contain at least 4 characters and cannot be only spaces."

        salt = secrets.token_hex(16)
        records = dict(self._saved_users)
        records[username] = {"salt": salt, "hash": self._password_hash(password, salt)}
        if self.accounts_file is not None:
            temporary_path = None
            try:
                self.accounts_file.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(
                    mode="w", encoding="utf-8", dir=self.accounts_file.parent,
                    prefix="users-", suffix=".tmp", delete=False
                ) as file:
                    temporary_path = Path(file.name)
                    json.dump({"version": 1, "users": records}, file, indent=2)
                    file.write("\n")
                os.replace(temporary_path, self.accounts_file)
            except OSError:
                if temporary_path is not None:
                    try:
                        temporary_path.unlink(missing_ok=True)
                    except OSError:
                        pass
                return False, "Could not save the account. Check that the project folder is writable."

        self._saved_users = records
        return True, f"User '{username}' created. Use login {username} to sign in."

    def authenticate(self, username: str, password: str) -> bool:
        if username in self._users:
            return self._users[username] == password
        record = self._saved_users.get(username)
        if record is None:
            return False
        return hmac.compare_digest(self._password_hash(password, record["salt"]), record["hash"])

    def login(self, username: str, password: str) -> bool:
        if self.authenticate(username, password):
            self.current_user = username
            return True
        return False

    def logout(self):
        self.current_user = None

    def interactive_login(self) -> bool:
        """
        Ask for credentials until a valid login is entered.
        Typing 'exit' as the username cancels startup/login.
        """
        print("=" * 48)
        print(f"{OS_NAME} LOGIN".center(48))
        print("=" * 48)
        print("Type 'exit' as the username to quit.\n")

        while True:
            username = input("Username: ").strip()

            if username.lower() == "exit":
                return False

            password = getpass("Password: ")

            if self.login(username, password):
                print("\nLogin successful.")
                print(f"Welcome, {self.current_user}!")
                return True

            print("\nInvalid username or password. Please try again.\n")

    def whoami(self) -> str:
        if self.current_user is None:
            return "No user is currently logged in."
        return f"Current User: {self.current_user}"

    def list_users(self):
        return list(self._users.keys()) + sorted(self._saved_users.keys())
