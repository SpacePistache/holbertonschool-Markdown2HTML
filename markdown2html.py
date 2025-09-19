#!/usr/bin/python3

"""A script that takes an argument of 2 strings"""

import os
import sys

def main():
	"""Function checking arguments and file existence"""
	if len(sys.argv) != 3:
		print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
		sys.exit(1)

	input_file = sys.argv[1]
	output_file = sys.argv[2]

	if not os.path.isfile(input_file):
		print(f"Missing {input_file}", file=sys.stderr)
		sys.exit(1)

	sys.exit(0)

if __name__ == "__main__":
	main()
