.PHONY : report main open clear

report : main open

main : ./tex/MakefileTex
	cd ./tex && make -f MakefileTex

open :
	xdg-open pdf/TOR.pdf

clear :
	rm -rf ./pdf/TOR.pdf ./out/
	cd ./tex && make -f MakefileTex clear
