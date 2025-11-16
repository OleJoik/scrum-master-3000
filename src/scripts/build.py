from scripts.esbuild import build as build_esbuild
from scripts.tailwind import build as build_tailwind


def main():
    build_esbuild()
    build_tailwind()


if __name__ == "__main__":
    main()
