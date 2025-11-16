from contextlib import contextmanager
from pathlib import Path
import subprocess

from backend.routes.react import STYLES_FILE

TAILWIND_INPUT_FILE = Path("src") / "tailwind.css"

TAILWIND_CMD = [
    "npx",
    "@tailwindcss/cli",
    "-i",
    str(TAILWIND_INPUT_FILE),
    "-o",
    str(STYLES_FILE),
]


@contextmanager
def watch():
    cmds = [
        *TAILWIND_CMD,
        "--watch=always",
    ]

    print(f"Watching tailwind from input file: {TAILWIND_INPUT_FILE}")
    print(" ".join(cmds))
    proc = subprocess.Popen(
        cmds,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    try:
        yield proc
    finally:
        if proc.poll() is None:
            print("🛑 Stopping Tailwind...")
            proc.terminate()


def build():
    print(f"Building tailwind from input file: {TAILWIND_INPUT_FILE}")
    print(" ".join(TAILWIND_CMD))

    subprocess.run(TAILWIND_CMD, check=True)

    print(f"Output tailwind file: {STYLES_FILE}")


if __name__ == "__main__":
    build()
