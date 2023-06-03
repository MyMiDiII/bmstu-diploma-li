.PHONY : report main open clean

report : main

main : ./tex/MakefileTex
	cd ./tex && make -f MakefileTex

open :
	xdg-open pdf/presentation.pdf

clean :
	rm -rf ./pdf/presentation.pdf ./out/
	cd ./tex && make -f MakefileTex clean
