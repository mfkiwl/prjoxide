#!/usr/bin/env python3
"""
Convert the tile grid for a given family and device to HTML format
"""
import sys, re
import argparse
import database
import libprjoxide

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('family', type=str,
                    help="FPGA family (e.g. LIFCL)")
parser.add_argument('device', type=str,
                    help="FPGA device (e.g. LIFCL-40)")
parser.add_argument('tiletype', type=str,
                    help="tile type (e.g. PLC)")
parser.add_argument('outfile', type=str,
                    help="output HTML file")

def main(argv):
    args = parser.parse_args(argv[1:])
    db = libprjoxide.Database(database.get_db_root())
    libprjoxide.write_tilebits_html(db, args.family, args.device, args.tiletype, args.outfile)

if __name__ == "__main__":
    main(sys.argv)