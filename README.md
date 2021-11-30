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

HDI-Highlighter is a Flask webapp using automatons generated using Unitex/Gramlab (https://github.com/UnitexGramLab/), and it's Python bindings (https://github.com/patwat/python-unitex)

## Requirements

- Python 3
- Unidecode
- Flask
- Flaskwebgui
- Gunicorn
