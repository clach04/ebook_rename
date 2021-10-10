# ebook_rename

Rename ebook file names.

Currently Amazon mobi (azw3) based files only supported.

Usage:

  bulk_rename.py DIR_NAME

Note relies on:
  * https://github.com/kroo/mobi-python which is Python 2.x only
      * Python 3 - https://github.com/kuhnchris/mobi-python
          * https://github.com/clach04/mobi-python/tree/py3_kuhnchris
      * Python 3 + enhancements and tests - https://github.com/btimby/mobi-python
          * https://github.com/clach04/mobi-python/tree/py3plus_btimby
  * https://github.com/claird/PyPDF4 or https://github.com/mstamy2/PyPDF2 which is Python 2.x and 3.x compatible
