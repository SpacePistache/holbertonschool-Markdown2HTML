#!/usr/bin/python3
"""
Script that converts a Markdown file to HTML (supports headings # to ###### and unordered lists).

Usage: ./markdown2html.py <input_markdown> <output_html>
"""

import os
import sys


def parse_markdown(lines):
    """
    Convert a list of Markdown lines to HTML lines.

    Supports:
    - Headings: # to ######
    - Unordered lists: lines starting with '- '
    """
    html_lines = []
    in_list = False

    for line in lines:
        line = line.rstrip()

        if line.startswith('#'):
            i = 0
            while i < len(line) and line[i] == '#':
                i += 1
            if 1 <= i <= 6 and line[i] == ' ':
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                html_lines.append(f"<h{i}>{line[i+1:].strip()}</h{i}>")
                continue

        if line.startswith('- '):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")
            continue

        if in_list:
            html_lines.append("</ul>")
            in_list = False

    if in_list:
        html_lines.append("</ul>")

    return html_lines


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

    with open(input_file, 'r', encoding='utf-8') as f:
        markdown_lines = f.readlines()

    html_lines = parse_markdown(markdown_lines)

    with open(output_file, 'w', encoding='utf-8') as f:
        for line in html_lines:
            f.write(line + "\n")

    sys.exit(0)


if __name__ == "__main__":
    main()
