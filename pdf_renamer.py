#!/usr/bin/env python
# -*- coding: windows-1252 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#

import os
import re
import sys
from string import Template

try:
    from pypdf import PdfFileReader  # https://github.com/claird/PyPDF4
    raise ImportError
except ImportError:
    try:
        from PyPDF3 import PdfFileReader  # https://github.com/mstamy2/PyPDF3
    except ImportError:
        from PyPDF2 import PdfFileReader  # https://github.com/mstamy2/PyPDF2 / https://pythonhosted.org/PyPDF2/

from mobi_renamer import safe_filename  # FIXME/TODO move this into a util library

def get_metadata(filename):
    f = open(filename, 'rb')
    pdf = PdfFileReader(f)
    if hasattr(pdf, 'getDocumentInfo'):
        info = pdf.getDocumentInfo()  # PyPDF3 and earlier
    else:
        info = pdf.documentInfo  # PyPDF4
    #print(info)
    #print(info.title)
    #print(info['/Title'])
    f.close()
    return info

def generate_pdf_name(in_filename, template=Template(u'$author - $title.$extn')):
    # Either set extn to 'pdf' or pickup original?
    """
    extn = os.path.splitext(in_filename)[1]
    extn = extn[1:]  # removed leading period
    """
    extn = 'pdf'
    basename = os.path.basename(in_filename)
    original_filename_sans_extn = os.path.splitext(basename)[0]

    info = get_metadata(in_filename)
    author, title = 'missing author', 'missing title'
    #author, title = info.author, info.title
    author, title = info.author, info.title or info['/Title']  # workaround https://github.com/claird/PyPDF4/issues/59, https://github.com/mstamy2/PyPDF3/issues/13, https://github.com/mstamy2/PyPDF2/issues/511
    #title = ' '.join(title.strip().split())  # remove all whitespace and replace with single space
    assert title is not None
    assert author is not None
    # if at least one is not-None, use original name `original_filename_sans_extn` with meta data?

    new_filename = template.substitute(author=author, title=title, extn=extn)  # TODO use a dict?
    new_filename = safe_filename(new_filename)
    return new_filename

generate_filename = generate_pdf_name

def main(argv=None):
    if argv is None:
        argv = sys.argv

    # dumb argv processing for simplicity - TODO update and use a library
    #in_filename = argv[1]
    in_filename = 'C:\\w541\\c\\user_clach04\\py\\ebook_rename\\test_books\\Retro Gaming on Raspberry Pi.pdf'  # FAILS reports no meta, there is a title though. PDF version 1.4 (acrobat 5.x)
    #in_filename = 'C:\\w541\\c\\user_clach04\\py\\ebook_rename\\test_books\\Expert C Programming Deep C Secrets Peter van der Linden c5a70918890b389ed026705577159093.pdf'  # works (contains useful meta). PDF version 1.3 (acrobat 4.x)
    #in_filename = 'C:\\w541\\c\\user_clach04\\py\\ebook_rename\\test_books\\How_to_Recover_from_Email_Marketing_Mistakes.pdf'  # no meta data - unclear if this works. PDF version 1.7 (acrobat 9.x)
    out_filename = generate_pdf_name(in_filename)
    print(repr(out_filename))
    print(out_filename)

    return 0


if __name__ == "__main__":
    sys.exit(main())
