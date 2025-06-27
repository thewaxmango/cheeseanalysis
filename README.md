executables available for windows + linux, or run main.py from this folder

minimum supported terminal size 78x28, suggested 30 vertical

## special thanks
* thanks iitali for blockfish
* thanks chouhy for windows exe

## analysis interface
* turn: one turn for every piece placed
* accuracy: how many moves matched blockfish best score
* rank: order blockfish returns choices in, first is best
* score: rating that blockfish uses, lower is better. '?' used when player chooses move blockfish didn't return
* current: rough idea of where piece goes, <piece>-<\columns used>
* star: what move you chose
* arrow: what choice/path you are looking at
* page: following moves suggested by blockfish
* ghosts: show forecasted moves as ghosts

## i need to do error handling
* if it bricks on initializing or analyzing it's probably blockfish error and not handled properly, just restart
