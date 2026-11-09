import argparse
import re
from collections import Counter
from pathlib import Path


def count_words(text):
    """Count words in text, ignoring case."""
    words = re.findall(r"\b\w+\b", text.lower())
    return Counter(words)


def get_top_words(file_path, n=10):
    """Read a file and return its top N words."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    text = path.read_text(encoding="utf-8")
    counts = count_words(text)

    return counts.most_common(n)


def main():
    parser = argparse.ArgumentParser(description="Display the most frequent words in a text file.")

    parser.add_argument("file", help="Path to the text file")
    parser.add_argument(
        "-n", "--top", type=int, default=10, help="Number of top words to display (default: 10)"
    )

    args = parser.parse_args()

    if args.top < 1:
        parser.error("--top must be at least 1")

    try:
        results = get_top_words(args.file, args.top)

        if not results:
            print("The file is empty or contains no words.")
            return

        print(f"\nTop {args.top} words:\n")

        for word, count in results:
            print(f"{word}: {count}")

    except FileNotFoundError as error:
        print(f"Error: {error}")
        raise SystemExit(1) from None


if __name__ == "__main__":
    main()
