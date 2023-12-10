# Makefile for LaTeX documents

DOCNAME = test

all: $(DOCNAME).pdf

$(DOCNAME).pdf: $(DOCNAME).tex
	pdflatex $(DOCNAME)
	biber $(DOCNAME)
	makeglossaries $(DOCNAME)
	pdflatex $(DOCNAME)
	pdflatex $(DOCNAME)

clean:
	rm -f $(DOCNAME).aux $(DOCNAME).bbl $(DOCNAME).blg $(DOCNAME).log $(DOCNAME).out $(DOCNAME).toc $(DOCNAME).run.xml

.PHONY: all clean

