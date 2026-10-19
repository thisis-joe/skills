import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--excited", action="store_true")
    args = parser.parse_args()
    punctuation = "!" if args.excited else "."
    print(f"Hello, {args.name}{punctuation}")

if __name__ == "__main__":
    main()
