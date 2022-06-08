# HDI Highlighter

## Description 

Reading helper for pharmacological interaction articles

HDI-Highlighter is a tool allowing user to highlight PDFs of scientific articles about Herb-Drug Interactions (HDI).
It provides a visual assistance by highlighting terms of interests, including: 

- DCI, herbs and enzyme names. Enzymes mostly focus on CYP450 isoenzymes as they are by far the most studied interactions targets.
- Study types; i.e. case reports, clinical studies, in vitro, ...
- Dosages
- Percentages
- Words implying a variation in a parameter

## PDF extraction

To be able to process the content of a PDF file, the first task is to extract it from the file. This is a non-trivial task, as PDF are not designed to be reworked. Fortunately, a Python module named "PyMuPDF" (https://github.com/pymupdf/PyMuPDF) allows for an easy extraction. This package provides a solution to extract content of the file in a formatted way. One options allows to extract it in HTML format, what is interesting for us as:

1. HTML files are handeld directly by Unitex without any preprocessing step required, in exchange of a longer processing time
2. PDF-Highlighter being a webapp, HTML can be directly displayed without any need to rework it.

PyMuPDF provides a nearly perfect extraction of the PDF, even though some imprefections might appear in different step of the highlighting process. 

## Expressions highlighting

HDI-Highlighter uses automatons generated using Unitex/Gramlab (https://github.com/UnitexGramLab/) and incorporated in Python script using it's Python bindings (https://github.com/patwat/python-unitex) to extract content. 

## Requirements

- Python 3
- PyMuPDF
- python-unitex
- Unidecode
- Flask
- Flaskwebgui
- Gunicorn

## Use

In a terminal, go to hdi highlighter folder:
```
  cd path/to/hdi_higlighter 
```
Run gui.py to start a local server:
```
  python gui.py
```
A message in the terminal will give you the adress of the local server. Copy the link and open it in any browser.
