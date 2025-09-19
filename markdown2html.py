#!/usr/bin/python3
"""
Script that converts a Markdown file to HTML (only headings # through ######).

Usage: ./markdown2html.py <input_markdown> <output_html>
"""

import os
import sys


def parse_markdown_line(line):
    """
    Convert a Markdown heading line into an HTML heading.

    Supports only # to ###### at the start of the line.
    """
    line = line.rstrip()
    if line.startswith('#'):
        i = 0
        while i < len(line) and line[i] == '#':
            i += 1
        if 1 <= i <= 6 and line[i] == ' ':
            return f"<h{i}>{line[i+1:].strip()}</h{i}>"
    return None


def main():
    """Check arguments, read Markdown, and write HTML."""
    if len(sys.argv) != 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    html_lines = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            html_line = parse_markdown_line(line)
            if html_line:
                html_lines.append(html_line)

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in html_lines:
            f.write(line + "\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
