
isSDFluent(some).
happensAt(some, some).
holdsAtIE(some, some).
cached(some).

nextTimepoint(T, Tnext):-
	Tnext is T+40.

prevTimepoint(T, Tprev):-
	Tprev is T-40.

