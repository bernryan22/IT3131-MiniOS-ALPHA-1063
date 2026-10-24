"""Shared display settings and simulated RAM configuration."""

OS_NAME = "MiniOSAlphaSC1063"
GROUP_NAME = "Alpha"
VERSION = "1.0"
# Classroom convention: 1 GB = 1024 MB (technically GiB and MiB).
TOTAL_MEMORY_MB = 128 * 1024


def format_memory(amount: int) -> str:
    return f"{amount:,} MB ({amount / 1024:,.2f} GB)"
