#!/usr/bin/env python3
"""
plot_from_file.py

Reads a file containing one numeric value per line and plots a line graph using matplotlib.

Usage:
  python plot_from_file.py input.txt -o plot.png
  python plot_from_file.py input.txt --show          # show interactive window (if available)
  python plot_from_file.py input.txt --title "My Plot" --xlabel "Time" --ylabel "Value"

Notes:
 - Blank lines and lines starting with '#' are ignored.
 - Non-numeric lines are skipped with a warning printed to stderr.
"""
import argparse
import sys

def read_numbers(path):
    nums = []
    with open(path, 'r') as f:
        for lineno, line in enumerate(f, start=1):
            s = line.strip()
            if not s or s.startswith('#'):
                continue
            try:
                nums.append(float(s))
            except ValueError:
                print(f"Warning: skipping non-numeric line {lineno}: {s}", file=sys.stderr)
    return nums

def main():
    parser = argparse.ArgumentParser(description="Plot numbers from a file (one number per line).")
    parser.add_argument("input", help="Path to input text file with one number per line.")
    parser.add_argument("-o", "--output", help="Path to save the plot image (e.g. plot.png). If omitted, the plot will not be saved.")
    parser.add_argument("--title", default="Line plot", help="Plot title.")
    parser.add_argument("--xlabel", default="Index", help="X-axis label.")
    parser.add_argument("--ylabel", default="Value", help="Y-axis label.")
    parser.add_argument("--show", action="store_true", help="Show the plot interactively (if your environment supports it).")
    args = parser.parse_args()

    y = read_numbers(args.input)
    if not y:
        print("No numeric data found in the input file.", file=sys.stderr)
        sys.exit(2)

    x = list(range(1, len(y) + 1))

    import matplotlib.pyplot as plt
    plt.figure()
    plt.plot(x, y)               # simple line plot (x indices vs values)
    plt.title(args.title)
    plt.xlabel(args.xlabel)
    plt.ylabel(args.ylabel)
    plt.grid(True)

    if args.output:
        plt.savefig(args.output, bbox_inches='tight')
        print(f"Saved plot to {args.output}")

    if args.show:
        plt.show()

if __name__ == "__main__":
    main()
