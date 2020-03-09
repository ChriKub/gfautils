#!/usr/bin/env python

import argparse

from gfa import gfaHandler


def main():
    desc = 'MISSING'

    parser = argparse.ArgumentParser(description=desc, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument(metavar='gfa', type=str, nargs=1, dest='gfa', help='GFA input file.')

    args = parser.parse_args()

    gfa_fh = open(args.gfa[0], 'r')

    gfa_dt = gfa_fh.read()

    gfa_fh.close()

    gfa_obj = gfaHandler(gfa_dt)

    print("DEBUG")


main()
