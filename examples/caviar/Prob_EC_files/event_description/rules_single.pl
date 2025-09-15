%% These rules also consider the "abrupt" event.

initiatedAt( person(Id)=true, T ) :-
   happensAt( walking(Id), T),
   \+ happensAt( disappear(Id), T).

initiatedAt( person(Id)=true, T ) :-
   happensAt( running(Id), T),
   \+ happensAt( disappear(Id), T).

initiatedAt( person(Id)=true, T ) :-
   happensAt( active(Id), T),
   \+ happensAt( disappear(Id), T).

initiatedAt( person(Id)=true, T ) :-
   happensAt( abrupt(Id), T),
   \+ happensAt( disappear(Id), T).

initiatedAt( person(Id)=false, T) :-
   happensAt( disappear(Id), T).

% ==================================================
% LONG-TERM BEHAVIOUR: fighting(Person, Person2)
% ==================================================


% ----- initiate fighting

initiatedAt(fighting(Person, Person2) = true, T):-
    happensAt(abrupt(Person), T), % This proves that Person is a person.
    cached(holdsAt(person(Person2) = true, T)),
    holdsAtIE(close_fightDist(Person, Person2) = true, T),
    \+ happensAt( inactive(Person2), T),
    \+ happensAt(disappear(Person), T),
    \+ happensAt(disappear(Person2), T).

% ----- terminate fighting: split up

initiatedAt(fighting(Person, Person2) = false, T):-
    happensAt(walking(Person), T),
    holdsAtIE(close_fightDist(Person, Person2) = false, T).

initiatedAt(fighting(Person, Person2) = false, T):-
    happensAt(walking(Person2), T),
    holdsAtIE(close_fightDist(Person, Person2) = false, T).

initiatedAt(fighting(Person, Person2) = false, T):-
    happensAt(running(Person), T),
    holdsAtIE(close_fightDist(Person, Person2) = false, T).

initiatedAt(fighting(Person, Person2) = false, T):-
    happensAt(running(Person2), T),
    holdsAtIE(close_fightDist(Person, Person2) = false, T).

initiatedAt(fighting(Person, Person2) = false, T):-
    happensAt(disappear(Person), T).

initiatedAt(fighting(Person, Person2) = false, T):-
    happensAt(disappear(Person2), T).


% ==================================================
% LONG-TERM BEHAVIOUR: meeting(Person, Person2)
% ==================================================

% allow for a long-term behaviour to be both fighting and meeting
% ie, I cannot tell the difference

% ----- initiate meeting

initiatedAt(meeting(Person, Person2) = true, T):-
    happensAt(active(Person), T),
    cached(holdsAt(person(Person2) = true, T)),
    holdsAtIE(close_interactDist(Person, Person2) = true, T),
    \+ happensAt(abrupt(Person2), T),
    \+ happensAt(running(Person2), T),
    \+ happensAt(disappear(Person), T),
    \+ happensAt(disappear(Person2), T).

initiatedAt(meeting(Person, Person2) = true, T):-
    happensAt(inactive(Person), T),
    cached(holdsAt(person(Person) = true, T)),
    cached(holdsAt(person(Person2) = true, T)),
    holdsAtIE(close_interactDist(Person, Person2) = true, T),
    \+ happensAt(running(Person2), T),
    \+ happensAt(active(Person2), T),
    \+ happensAt(abrupt(Person2), T),
    \+ happensAt(disappear(Person), T),
    \+ happensAt(disappear(Person2), T).

% ----- terminate meeting: split up

initiatedAt(meeting(Person, Person2) = false, T):-
    happensAt(walking(Person), T),
    holdsAtIE(close_meetDist(Person, Person2) = false, T).

initiatedAt(meeting(Person, Person2) = false, T):-
    happensAt(walking(Person2), T),
    holdsAtIE(close_meetDist(Person, Person2) = false, T).

initiatedAt(meeting(Person, Pesron2) = false, T):-
    happensAt(running(Person), T).

initiatedAt(meeting(Person, Person2) = false, T):-
    happensAt(running(Person2), T).

initiatedAt(meeting(Person, Person2) = false, T):-
    happensAt(abrupt(Person), T).

initiatedAt(meeting(Person, Person2) = false, T):-
    happensAt(abrupt(Person2), T).

initiatedAt(meeting(Person, Person2) = false, T):-
    happensAt(disappear(Person), T).

initiatedAt(meeting(Person, Person2) = false, T):-
    happensAt(disappear(Person2), T).

% ==================================================
% LONG-TERM BEHAVIOUR: moving(Person, Person2)
% ==================================================


% two people are moving together

% ----- initiate moving

initiatedAt(moving(Person, Person2) = true, T):-
    happensAt(walking(Person), T),
    holdsAtIE(close_moveDist(Person, Person2) = true, T),
    happensAt( walking(Person2), T ),
    \+ happensAt(disappear(Person), T),
    \+ happensAt(disappear(Person2), T),
    holdsAtIE(orientation(Person, Person2) = true, T).

% ----- terminate moving: split up

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(walking(Person), T),
    holdsAtIE(close_moveDist(Person, Person2) = false, T).

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(walking(Person2), T),
    holdsAtIE(close_moveDist(Person, Person2) = false, T).

% ----- terminate moving: stop moving

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(active(Person), T),
    happensAt( active( Person2 ), T ).

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(active(Person), T),
    happensAt( inactive( Person2 ), T ).

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(active(Person2), T),
    happensAt( inactive( Person ), T ).

% ----- terminate moving: start running

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(running(Person), T).

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(running(Person2), T).

% ----- terminate moving: abrupt motion

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(abrupt(Person), T).

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(abrupt(Person2), T).

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(disappear(Person), T).

initiatedAt(moving(Person, Person2) = false, T):-
    happensAt(disappear(Person2), T).


% ==================================================
% LONG-TERM BEHAVIOUR: leaving_object(Person, Object)
% ==================================================

% ----- initiate leaving_object

initiatedAt(leaving_object(Person, Object) = true, T):-
    happensAt(inactive(Object), T),
    happensAt(appear(Object), T),
    holdsAtIE(close_leaveDist(Person, Object) = true, T),
    cached(holdsAt(person(Person)=true, T)).

% ----- terminate leaving_object: pick up object
%       disappear(Object) means that the Object has disappeared
%       which is what will happen if it has been picked up

initiatedAt(leaving_object(_, Object) = false, T):-
    happensAt(disappear(Object), T).

