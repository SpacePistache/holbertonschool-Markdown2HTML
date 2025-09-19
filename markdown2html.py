#!/usr/bin/python3
"""
Script that converts a Markdown file to HTML (supports headings, unordered lists, ordered lists, and paragraphs).

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
    - Ordered lists: lines starting with '* '
    - Paragraphs: consecutive non-empty lines separated by empty lines
    """
    html_lines = []
    in_ul = False
    in_ol = False
    paragraph_lines = []

    def flush_paragraph():
        """Convert collected paragraph lines to HTML and clear the buffer."""
        if paragraph_lines:
            html_lines.append("<p>")
            for i, pline in enumerate(paragraph_lines):
                html_lines.append(pline if i == 0 else f"<br/>{pline}")
            html_lines.append("</p>")
            paragraph_lines.clear()

    for line in lines:
        line = line.rstrip()

        if not line.strip():
            flush_paragraph()
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            continue

        if line.startswith('#'):
            flush_paragraph()
            i = 0
            while i < len(line) and line[i] == '#':
                i += 1
            if 1 <= i <= 6 and line[i] == ' ':
                if in_ul:
                    html_lines.append("</ul>")
                    in_ul = False
                if in_ol:
                    html_lines.append("</ol>")
                    in_ol = False
                html_lines.append(f"<h{i}>{line[i+1:].strip()}</h{i}>")
                continue

        if line.startswith('- '):
            flush_paragraph()
            if in_ol:
                html_lines.append("</ol>")
                in_ol = False
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")
            continue

        if line.startswith('* '):
            flush_paragraph()
            if in_ul:
                html_lines.append("</ul>")
                in_ul = False
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
            html_lines.append(f"<li>{line[2:].strip()}</li>")
            continue

        flush_paragraph() if False else None
        paragraph_lines.append(line)

    flush_paragraph()

    if in_ul:
        html_lines.append("</ul>")
    if in_ol:
        html_lines.append("</ol>")

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
