#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""CSV splitter
This script is the adaptation of the gist found here (https://gist.github.com/jrivero/1085501/12cc8ff4ee581628c0d62a6ea4922fc09f169219)
in order to split CSV file directly in command line.
## EXAMPLE
    - python csv_splitter.py -i my_input_csv.csv -d ';' -t my_output_csv_%s.csv -o ./output-directory -k
"""
import os
import csv
import optparse
import sys

__version__ = "1.0"

USAGE = "%prog [options]"
VERSION = "%prog v" + __version__

def split(filehandler, delimiter=',', row_limit=1000, 
    output_name_template='output_%s.csv', output_path='.', keep_headers=True):
    """
    Splits a CSV file into multiple pieces.
    
    A quick bastardization of the Python CSV library.
    Arguments:
        `row_limit`: The number of rows you want in each output file. 10,000 by default.
        `output_name_template`: A %s-style template for the numbered output files.
        `output_path`: Where to stick the output files.
        `keep_headers`: Whether or not to print the headers in each output file.
    Example usage:
    
        >> from toolbox import csv_splitter;
        >> csv_splitter.split(open('/home/ben/input.csv', 'r'));
    
    """
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
         output_path,
         output_name_template  % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = reader.next()
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
               output_path,
               output_name_template  % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)

def parse_options():
    """parse_options() -> opts, args
    Parse any command-line options given returning both
    the parsed options and arguments.
    """

    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-i", "--input",
            action="store", type="string", dest="input",
            help="The csv file path to split (required)")

    parser.add_option("-d", "--delimiter",
            action="store", type="string", default=",", dest="delimiter",
            help="The delimiter of your csv file")

    parser.add_option("-r", "--rowlimit",
            action="store", type="int", default=1000, dest="rowlimit",
            help="Maximum number of row in your split output file")

    parser.add_option("-t", "--template",
            action="store", type="string", default="output_%s.csv", dest="template",
            help="The output file name template")

    parser.add_option("-o", "--outputpath",
            action="store", type="string", default=".", dest="outputpath",
            help="Directory in which output files will be created")

    parser.add_option("-k", "--keepheaders",
            action="store_true", default=False, dest="keepheaders",
            help="Keep CSV headers or not")

    opts, args = parser.parse_args()

    if not opts.input:
        parser.print_help(sys.stderr)
        raise SystemExit, 1

    if not os.path.exists(opts.input):
        print "[!] Input file '%s' not found" % (opts.input)
        raise SystemExit, 1

    return opts, args

def main():
    opts, args = parse_options()

    split(open(opts.input, 'r'), opts.delimiter, opts.rowlimit, opts.template, opts.outputpath, opts.keepheaders)

if __name__ == "__main__":
    main()
