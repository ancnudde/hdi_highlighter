import re
import fitz
import operator
import unidecode
from html import unescape


class PDFExtractor():
    """
    A class based on the "fitz"(PyMuPDF) package, and allows to extract the
    content of a PDF and tag it's content based on text format properties.
    Fitz extracts the content of the PDF and stocks it on the form of  a "doc"
    object. This object contains each page of the PDF separately. Each page
    contains in turn a set of "blocks" and their informations, on the form of
    a dictionary.
    Among these informations, this class will use the following:
        - type: A block with type 0 contains text, those are the
                ones we want to extract;
        - lines: Lines are subsections of blocks. A line corresponds
                 to a line of text (usually a sentence);
        - spans: spans are subsets of lines, and correspond to specific
                 elements, e.g. subscripts, superscripts, bold or italic
                 words inside a regular sentence, ...
    The elements extracted from PDF are:
        - the content table;
        - the full content, including body, headers, references, ...
        - the body only, which contains the main content.
    The content table is constructed using method provided by PyMuPDF and that
    uses metadata from the PDF file. If the PDF doesn't contains these
    metadata, a method is designed within this class to use header tags to
    try to construct this table, but the result is not always reliable.
    The body of the text might lack some informations such as indices and
    exponants.
    The result of the process is contained within an "ExtractedPDF" object.
    """

    def __init__(self, pdf):
        self.pdf = fitz.open(pdf)
        self.pages = [page for page in self.pdf.pages()]
        self.marked_text = []
        self.blocks_containers = {}

    def _repare_font(self, otext):
        pos1 = 0
        font_serif = "font-family:Times"
        font_sans = "font-family:Helvetica"
        font_mono = "font-family:Courier"
        found_one = False
        while True:
            pos0 = otext.find("font-family:", pos1)
            if pos0 < 0:
                break
            pos1 = otext.find(";", pos0)
            # complete font spec string
            test = otext[pos0: pos1]
            testn = ""
            if test.endswith(",serif"):
                testn = font_serif
            elif test.endswith(",sans-serif"):
                testn = font_sans
            elif test.endswith(",monospace"):
                testn = font_mono
            if testn != "":
                otext = otext.replace(test, testn)
                found_one = True
                pos1 = 0
        if not found_one:
            print("Warning: could not find any font specs!")
        return otext

    def _markup_page(self, page, page_index):
        blocks = page.getText('blocks', flags=fitz.TEXT_PRESERVE_IMAGES)
        marked_blocks = []
        containers_dict = {}
        for i, block in enumerate(blocks):
            marked_blocks.append(block[4] + f'|B|{page_index}_{i}|B|')
            containers_dict[f'{page_index}_{i}'] = block
        return marked_blocks, containers_dict

    def _remove_images(self, html_string):
        image_re = re.compile(r'<img(.|\s)*?>')
        without_images = image_re.sub('', html_string)
        return without_images

    def _page_to_html(self, page, remove_images=False):
        html_string = unescape(page.getText('html'))
        if remove_images:
            html_string = self._remove_images(html_string)
        return html_string

    def _pdf_to_html(self, remove_images=False):
        html_pdf = ''
        for page in self.pages:
            clean_formatted = self._page_to_html(page, remove_images)
            clean_formatted = unidecode.unidecode(clean_formatted)
            html_pdf += (clean_formatted + '\n')
        clean_pdf = self._repare_font(html_pdf)
        with open('full_pdf.html', 'w') as fp:
            fp.write(clean_pdf)


if __name__ == '__main__':
    extractor = PDFExtractor('test4.pdf')
    extractor._pdf_to_html()
