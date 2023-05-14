.PHONY : report main open clean

report : main open

main : ./tex/MakefileTex
	cd ./tex && make -f MakefileTex

open :
	xdg-open pdf/report.pdf

clean :
	rm -rf ./pdf/report.pdf ./out/
	cd ./tex && make -f MakefileTex clean
