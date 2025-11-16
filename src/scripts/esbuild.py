from contextlib import contextmanager
import subprocess

from backend.routes.react import SRC_DIRECTORY, EntryPoint, REACT_DIRECTORY


BUILD_COMMANDS = [
    "esbuild",
    *[str(SRC_DIRECTORY / file.value) for file in EntryPoint],
    "--bundle",
    f"--outdir={REACT_DIRECTORY}",
    "--format=esm",
    "--target=chrome58,firefox57,safari11,edge16",
]


def build():
    cmd = [
        *BUILD_COMMANDS,
        "--minify",
        "--sourcemap",
    ]
    print(f"Running esbuild cmd: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


@contextmanager
def watch():
    print("🔨 Starting esbuild watch...")
    cmd = [
        *BUILD_COMMANDS,
        "--watch",
    ]
    print(f"Running esbuild cmd: {' '.join(cmd)}")
    proc = subprocess.Popen(cmd)

    try:
        yield proc
    finally:
        if proc.poll() is None:
            print("🛑 Stopping esbuild...")
            proc.terminate()


if __name__ == "__main__":
    build()
