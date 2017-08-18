#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Given a directory of (unencrypted) MOBI format files, rename each file
"""

import glob
import os
import sys

import mobi_renamer


def main(argv=None):
    if argv is None:
        argv = sys.argv

    # dumb argv processing for simplicity - TODO update and use a library
    in_directory = argv[1]
    try:
        out_directory = argv[2]
    except IndexError:
        out_directory = in_directory

    print('Using %s' % in_directory)
    for filename in glob.glob(os.path.join(in_directory, '*')):
        print(repr(filename))
        new_filename = mobi_renamer.generate_mobi_name(filename)
        print(repr(new_filename))
        new_filename = os.path.join(out_directory, new_filename)
        print(repr(new_filename))
        os.rename(filename, new_filename)

    return 0


if __name__ == "__main__":
    sys.exit(main())
