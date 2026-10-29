"""Header and progress lines shared by the examples.

Imports nothing heavy, so the header prints straight away while usdm4 and
usdm4_excel are still loading.
"""

import platform
from importlib.metadata import PackageNotFoundError, version

WIDTH = 64
PACKAGES = ["usdm4", "usdm4_excel"]


def _version(package: str) -> str:
    try:
        return version(package)
    except PackageNotFoundError:
        return "not installed"


def header(number: int, title: str, purpose: str, packages: list[str] = PACKAGES) -> None:
    """Print the example's header, then a loading line."""
    versions = "  ·  ".join(f"{p} {_version(p)}" for p in packages)
    print("═" * WIDTH)
    print(f" USDM and Python  ·  Example {number:02d}  ·  {title}")
    print(f" {purpose}")
    print("─" * WIDTH)
    print(f" {versions}  ·  Python {platform.python_version()}")
    print("═" * WIDTH)
    step("Loading packages")


def step(message: str) -> None:
    """Say what's about to happen, before a slow call."""
    print(f"» {message} ...", flush=True)


def section(title: str) -> None:
    """Separate the progress lines from the results."""
    print(f"\n── {title} " + "─" * max(0, WIDTH - len(title) - 4))
