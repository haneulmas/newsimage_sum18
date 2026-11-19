from pathlib import Path
import os


def main():
    source = Path(__file__).resolve().parent / "assets" / "entry.png"
    image = source.read_bytes()
    output = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    output.mkdir(parents=True, exist_ok=True)
    (output / "entry.png").write_bytes(image)


if __name__ == "__main__":
    main()
