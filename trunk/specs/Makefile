
FILE = specs


DEPS = 

# ----------------------------------------------------------------------

#LATEXFLAGS = -interaction=nonstopmode
PSFLAGS = -Ppdf -G0
PDFFLAGS = -dPDFSETTINGS=/prepress

LATEXCMD = latex
PSCMD = dvips
PDFCMD = ps2pdf
EDITCMD = emacs -i -l itemize.el
MACEDITCMD = open

# ----------------------------------------------------------------------

default: ps

dvi: $(FILE).dvi

ps: $(FILE).ps

pdf: $(FILE).pdf

clean: cleantmp
	-rm -f $(FILE).pdf

cleantmp:
	-rm -f *.aux *.log *.bbl *.blg *.toc *.lof *.lot *.ent *.fff *.ttt *.*~ *.snm *.nav *.out *.vrb *.rel
	-rm -f *.dvi *.ps

cleanall:
	-rm -f *.aux *.log *.bbl *.blg *.toc *.lof *.lot *.ent *.fff *.ttt *~ *.snm *.nav *.out *.vrb *.rel
	-rm -f *.dvi *.ps
	-rm -f *.pdf

view: ps
	gv --watch $(FILE).ps &

edit:
	$(EDITCMD) $(FILE).tex &

macedit:
	$(MACEDITCMD) $(FILE).tex

notes: dvi
	$(PSCMD) $(PSFLAGS) -ta4 -o $(FILE)_tmp.ps $(FILE).dvi
	psnup -4 -W128mm -H96mm -pa4 -m1cm $(FILE)_tmp.ps $(FILE).ps
	-rm -f $(FILE)_tmp.ps

count:
	grep \begin{frame} $(FILE).tex | wc -l

# ----------------------------------------------------------------------

$(FILE).dvi: $(FILE).tex $(DEPS)
	( \
	$(LATEXCMD) $(LATEXFLAGS) $<; \
	while grep -q "Rerun to get cross-references right." $(<:.tex=.log); \
	do \
		$(LATEXCMD) $(LATEXFLAGS) $<; \
	done \
	)	

$(FILE).ps: $(FILE).dvi
	$(PSCMD) $(PSFLAGS) -o $(FILE).ps $(FILE).dvi

$(FILE).pdf: $(FILE).ps
	$(PDFCMD) $(PDFFLAGS) $(FILE).ps $(FILE).pdf
