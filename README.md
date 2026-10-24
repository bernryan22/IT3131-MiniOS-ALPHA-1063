# MiniOSAlphaSC1063

Group **Alpha** | Version **1.2**

A Python command-line operating-system simulator for Windows Command Prompt.

## Start

Extract the ZIP, open the folder containing main.py, type cmd into File
Explorer's address bar, and press Enter. In CMD, run:

```cmd
python main.py
```

Use py -3 main.py if your Python launcher is available.
Requires Python 3.8 or newer; no third-party packages are needed.

| Username | Password |
|---|---|
| admin | admin |
| student | student |

Password characters stay hidden. Press Enter after typing.
Type help for all commands or help adduser for an example.

## Add a User

```text
adduser ralph
```

Enter a new password, then confirm it at the separate prompts.
Use users to list accounts and login ralph to switch to the new account.

Usernames use 3-24 letters, numbers or underscores. The name exit is reserved.
Passwords need at least 4 characters and cannot contain only spaces.
All signed-in users can add accounts. Accounts share the same files and commands.

New accounts remain after restart and are saved in data/users.json.
**Keep your existing data/ and minios_storage/ folders when updating or moving
the project.** Added passwords are saved as salted hashes. Demo accounts remain
available. The account file is created automatically when the first user is added.

## Commands

| Category | Commands |
|---|---|
| General | `help`, `clear`, `date`, `time`, `whoami`, `systeminfo`, `exit`, `history`, `echo`, `calculator`, `status`, `version`, `shutdown` |
| File Management | `dir`, `mkdir`, `create`, `read`, `delete`, `write`, `rename`, `cd`, `append`, `pwd`, `rmdir` |
| Process Management | `process`, `run`, `kill` |
| Memory Management | `memory`, `allocate`, `free` |
| User Management | `users`, `login`, `logout`, `adduser` |


## User Guide

- [User manual](docs/User_Manual.pdf): a clean seven-page guide with every
  command's syntax, function and example, plus account creation and troubleshooting.
- [Editable guide](docs/User_Guide.md): Markdown version for viewing or editing.

## Memory and Files

MiniOS has 131,072 MB (128 GB) of simulated RAM, using 1 GB = 1024 MB
(technically GiB/MiB). No real RAM is reserved.
allocate 4096 consumes 4 GB of simulated memory; free 4096 releases it.
run creates only a simulated process and does not consume simulated RAM.

Files are real UTF-8 text files saved inside minios_storage.
Quote names containing spaces. cd / returns to its virtual root; cd .. moves
to the parent. Both slash styles work. delete permanently removes a file,
and rmdir removes only empty folders.

Files and accounts stay saved after exit. Simulated memory, processes, history
and the current folder reset at the next launch. Account switching preserves
the active session.

## Project Files

| File / folder | Purpose |
|---|---|
| main.py | Startup and login |
| shell.py | Command loop, parsing, validation and handlers |
| command_catalog.py | Shared command descriptions and help |
| config.py | Name, version and simulated RAM capacity |
| users.py | Account creation, persistence and authentication |
| filesystem.py | MiniOS file area |
| processes.py | Simulated processes and PIDs |
| memory.py | Simulated memory counters |
| system_info.py | System details, local date and time |
| utils.py | Terminal helpers |
| docs/ | User guide and test notes |
| tests/ | Automated tests |
| data/ | Automatically created account data |
| minios_storage/ | Automatically created file area |

## Testing

```cmd
python -m unittest discover -s tests -v
```

All **19 tests passed** in the Linux development environment.
Account persistence, password confirmation, duplicate names, save failures and
help formatting are covered alongside file, process and memory behavior.
Your group should also test in Windows CMD and capture actual screenshots.

## Group

Group name: **Alpha**. Add the actual members and roles before submitting.
The project instructions also require a repository, technical documentation,
actual CMD screenshots, individual contribution reports and a demo video.
