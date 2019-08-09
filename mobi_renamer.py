#!/usr/bin/env python
# -*- coding: windows-1252 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
"""Given a single (unencrypted) MOBI format file rename it to:
    author - title.FILE_EXTENSION

TODO:
  * directories/multiple files
  * allow control over the format of the new filename
      * other meta data, series information?
  * work out what's the best library for this - if in doubt raw format details https://wiki.mobileread.com/wiki/MOBI
      * https://github.com/kroo/mobi-python
      * KindleNamer
          * https://www.mobileread.com/forums/showthread.php?t=197168
      * KindleUnpack (MobiUnpack)
          * https://www.mobileread.com/forums/showthread.php?t=61986
          * https://wiki.mobileread.com/wiki/KindleUnpack
          * https://wiki.mobileread.com/wiki/MOBI
      * https://github.com/booktype/ebooklib/blob/mobi/ebooklib/mobi.py - not sure this has it but might be worth adding
      * https://sourceforge.net/projects/pythonpalmdb/
          * See https://stackoverflow.com/questions/9465158/how-to-get-isbn-number-from-mobi-file-with-python
      * Last time I checked Calibre it was not usable as a library
  * other file formats; epub
"""

import os
import re
import sys
from string import Template

from mobi import Mobi  # https://github.com/kroo/mobi-python Python 2.x only :-(


def safe_filename(in_filename):
    """Inspired by KindlerNamer
    """
    name = in_filename  # keep in_filename around for debugging/compare purposes

    # replace characters that are not valid for filenames on different Operating Systems
    # TODO \u2013 to '-'?
    rename_safe_map = {
        '<': u'[',
        '>': u']',
        #' : ': u' – ',
        ' : ': u' - ',
        #': ': u' – ',
        ': ': u' - ',
        ':': u'—',
        '/': u'_',
        '\\': u'_',
        '|': u'_',
        '"': u'\'',
        '*': u'_',
        '?': u'',
    }
    for unsafe_char in rename_safe_map:
        name = name.replace(unsafe_char, rename_safe_map[unsafe_char])

    # strip control characters
    name = u"".join(char for char in name if ord(char)>=32)

    # strip and condence white space, delete leading and trailing while space
    name = name.strip()
    name = re.sub(ur"\s", u" ", name)
    while '  ' in name:
        name = name.replace('  ', ' ')
    name = name.strip()

    # remove leading dots
    while name.startswith(u'.'):
        name = name[1:]

    # remove trailing dots (problem under Microsoft Windows)
    while name.endswith(u'.'):
        name = name[:-1]

    name = name.strip()  # second cleanup just in case
    return name


def generate_mobi_name(in_filename, template=Template(u'$author - $title.$extn')):
    # NOTE assume in_filename is in correct encoding (ideally Unicode string) and will "just work"
    book = Mobi(in_filename)
    book.parse()
    # title is sometimes different compared with "503" entry. E.g. compare 'Broken Homes' and 'Broken Homes (PC Peter Grant Book 4)' for https://www.amazon.com/Broken-Homes-Peter-Grant-Book-ebook/dp/B00DYX9OPC/
    author, title = book.author(), book.title()  # returns bytes. NOTE not going to use these...
    #print(type(author))
    #print((author, title))
    book_codepage = book.config.get('mobi', {}).get('text Encoding', 1252)  # not sure if this is text encoding for content or all meta data (e.g. titles)
    #print(book_codepage)
    """
    import pprint
    pprint.pprint(book.config)
    """
    BOOK_CODEPAGE2ENCODING = {
        1252 : 'windows-1252',
        65001 : 'utf-8',
    }
    #print(BOOK_CODEPAGE2ENCODING[book_codepage])  # use this with names
    #print((author, title))
    author = book.config['exth']['records'][100]
    title = book.config['exth']['records'].get(503) or book.config['mobi'].get('Full Name')  # NOTE if both exist, may want the longest one. So far all books from Amazon I've seen have consistently been 503 (e.g. "SERIES Book X")
    author = author.decode(BOOK_CODEPAGE2ENCODING[book_codepage])
    title = title.decode(BOOK_CODEPAGE2ENCODING[book_codepage])
    extn = os.path.splitext(in_filename)[1]
    extn = extn[1:]  # removed leading period
    #print((author, title, extn))
    #print('%s - %s' % (author, title))
    new_filename = template.substitute(author=author, title=title, extn=extn)  # TODO use a dict?
    #new_filename = '      .... ??? <1of 2>  "hello"...........' ## DEBUG
    new_filename = safe_filename(new_filename)
    print(repr(new_filename))
    return new_filename

generate_filename = generate_mobi_name

def main(argv=None):
    if argv is None:
        argv = sys.argv

    # dumb argv processing for simplicity - TODO update and use a library
    #in_filename = argv[1]
    in_filename = 'C:\\Users\\clach04\\py\\DeDRM_tools\\DeDRM_Windows_Application\\DeDRM_App\\DeDRM_lib\\lib\\Black Rain_nodrm.azw3'
    in_filename = 'C:\\Users\\clach04\\py\\DeDRM_tools\\DeDRM_Windows_Application\\DeDRM_App\\DeDRM_lib\\lib\\kindle_books_fixed\\\\Broken Homes (PC Peter Grant Book 4)_nodrm.azw3'
    in_filename = 'C:\\Users\\clach04\\py\\DeDRM_tools\\DeDRM_Windows_Application\\DeDRM_App\\DeDRM_lib\\lib\\kindle_books_fixed\\A Latent Dark_nodrm.mobi'
    #in_filename = 'C:\\Users\\clach04\\py\\DeDRM_tools\\DeDRM_Windows_Application\\DeDRM_App\\DeDRM_lib\\lib\\kindle_books_fixed\\Besieged – Stories from The Iron Druid Chronicles_nodrm.azw3'
    generate_mobi_name(in_filename)

    return 0


if __name__ == "__main__":
    sys.exit(main())
