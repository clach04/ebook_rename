# ebook_rename

Rename ebook file names.

Currently Amazon mobi (azw3) based files only supported.

Usage:

  bulk_rename.py DIR_NAME

Note relies on:
  * https://github.com/kroo/mobi-python which is Python 2.x only
      * Python 3 ONLY - https://github.com/kuhnchris/mobi-python
          * https://github.com/clach04/mobi-python/tree/py3_kuhnchris
      * does NOT work Python 3 and 2 + enhancements and tests - https://github.com/btimby/mobi-python
          * https://github.com/clach04/mobi-python/tree/py3plus_btimby
          * Fails to parse header for REC_DATA_OFF
  * https://github.com/claird/PyPDF4 or https://github.com/mstamy2/PyPDF2 which is Python 2.x and 3.x compatible

## Getting Started

    python -m pip install -r requirements.txt

