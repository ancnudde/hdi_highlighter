from text_extractor import PDFExtractor
from unitex_tagger import TextTagger


class PDFTagger:

    def __init__(self, pdf, config=None, grammar=None):
        self.pdf_path = pdf
        self.extractor = PDFExtractor(pdf)
        self.extractor._pdf_to_html()
        self.tagger = None
        self._initiate_tagger()
        self._tag_pdf()

    def _initiate_tagger(self, config_file=None):
        if config_file:
            config = config_file
        else:
            config = "config/unitex-example.yaml"
        self.tagger = TextTagger(config)
        self.tagger.import_text('full_pdf.html')

    def _tag_pdf(self, grammar_file=None):
        if grammar_file:
            grammar = grammar_file
        else:
            grammar = "config/graphs/highlight.fst2"
        self.tagger.tag_text(grammar)


if __name__ == '__main__':
    tag = PDFTagger('test3.pdf')
