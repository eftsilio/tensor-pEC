%----------------within area -----------------%
initiatedAt(withinArea(Vessel,fishing)=true, T) :-
     happensAt(entersArea_fishing(Vessel), T).

initiatedAt(withinArea(Vessel,nearCoast)=true, T) :-
     happensAt(entersArea_nearCoast(Vessel), T).

initiatedAt(withinArea(Vessel,nearCoast5k)=true, T) :-
     happensAt(entersArea_nearCoast5k(Vessel), T).

initiatedAt(withinArea(Vessel,nearPorts)=true, T) :-
     happensAt(entersArea_nearPorts(Vessel), T).

initiatedAt(withinArea(Vessel, fishing)=false, T) :-
    happensAt(leavesArea_fishing(Vessel), T).

initiatedAt(withinArea(Vessel, nearCoast)=false, T) :-
    happensAt(leavesArea_nearCoast(Vessel), T).

initiatedAt(withinArea(Vessel, nearCoast5k)=false, T) :-
    happensAt(leavesArea_nearCoast5k(Vessel), T).

initiatedAt(withinArea(Vessel, nearPorts)=false, T) :-
    happensAt(leavesArea_nearPorts(Vessel), T).

initiatedAt(withinArea(Vessel, _AreaType)=false, T) :-
    happensAt(gap_start(Vessel), T).

%--------------- communication gap -----------%
initiatedAt(gap(Vessel)=nearPorts, T) :-
    happensAt(gap_start(Vessel), T),
    cached(holdsAt(withinArea(Vessel, nearPorts)=true, T)).

initiatedAt(gap(Vessel)=farFromPorts, T) :-
    happensAt(gap_start(Vessel), T),
    \+cached(holdsAt(withinArea(Vessel, nearPorts)=true, T)).

initiatedAt(gap(Vessel)=false, T) :-
    happensAt(gap_end(Vessel), T).

%-------------- stopped-----------------------%
initiatedAt(stopped(Vessel)=nearPorts, T) :-
    happensAt(stop_start(Vessel), T),
    cached(holdsAt(withinArea(Vessel, nearPorts)=true, T)).

initiatedAt(stopped(Vessel)=farFromPorts, T) :-
    happensAt(stop_start(Vessel), T),
    \+cached(holdsAt(withinArea(Vessel, nearPorts)=true, T)).

initiatedAt(stopped(Vessel)=false, T) :-
    happensAt(stop_end(Vessel), T).

initiatedAt(stopped(Vessel)=false, T) :-
    initiatedAt(gap(Vessel)=nearPorts, T).

initiatedAt(stopped(Vessel)=false, T) :-
    initiatedAt(gap(Vessel)=farFromPorts, T).

%-------------- lowspeed----------------------%
initiatedAt(lowSpeed(Vessel)=true, T) :-
    happensAt(slow_motion_start(Vessel), T).

initiatedAt(lowSpeed(Vessel)=false, T) :-
    happensAt(slow_motion_end(Vessel), T).

initiatedAt(lowSpeed(Vessel)=false, T) :-
    initiatedAt(gap(Vessel)=nearPorts, T).

initiatedAt(lowSpeed(Vessel)=false, T) :-
    initiatedAt(gap(Vessel)=farFromPorts, T).

%-------------- changingSpeed ----------------%
initiatedAt(changingSpeed(Vessel)=true, T) :-
    happensAt(change_in_speed_start(Vessel), T).

initiatedAt(changingSpeed(Vessel)=false, T) :-
    happensAt(change_in_speed_end(Vessel), T).

initiatedAt(changingSpeed(Vessel)=false, T) :-
    initiatedAt(gap(Vessel)=nearPorts, T).

initiatedAt(changingSpeed(Vessel)=false, T) :-
    initiatedAt(gap(Vessel)=farFromPorts, T).

%------------ highSpeedNearCoast -------------%
initiatedAt(highSpeedNearCoast(Vessel)=true, T):-
    happensAt(velocity_GrHcNCMax(Vessel), T),
    cached(holdsAt(withinArea(Vessel, nearCoast)=true, T)).

initiatedAt(highSpeedNearCoast(Vessel)=false, T):-
    happensAt(velocity_LtHcNCMax(Vessel), T).

initiatedAt(highSpeedNearCoast(Vessel)=false, T):-
    \+cached(holdsAt(withinArea(Vessel, nearCoast)=true, T)).

%--------------- movingSpeed -----------------%
initiatedAt(movingSpeed(Vessel)=below, T) :-
    happensAt(velocity_GrMovMin_LtMin(Vessel), T).

initiatedAt(movingSpeed(Vessel)=normal, T) :-
    happensAt(velocity_GrMin_LtMax(Vessel), T).

initiatedAt(movingSpeed(Vessel)=above, T) :-
    happensAt(velocity_GrMax(Vessel), T).

initiatedAt(movingSpeed(Vessel)=false, T) :-
    happensAt(velocity_LtMovMin(Vessel), T).

initiatedAt(movingSpeed(Vessel)=false, T) :-
    initiatedAt(gap(Vessel)=nearPorts, T).

initiatedAt(movingSpeed(Vessel)=false, T) :-
    initiatedAt(gap(Vessel)=farFromPorts, T).

%---------------- tuggingSpeed ----------------%
initiatedAt(tuggingSpeed(Vessel)=true , T) :-
    happensAt(velocity_GrTugMin_LeTugMax(Vessel), T).

initiatedAt(tuggingSpeed(Vessel)=false , T) :-
    happensAt(velocity_GrTugMax(Vessel), T).

initiatedAt(tuggingSpeed(Vessel)=false , T) :-
    happensAt(velocity_LtTugMin(Vessel), T).

initiatedAt(tuggingSpeed(Vessel)=false , T) :-
    initiatedAt(gap(Vessel)=nearPorts, T).

initiatedAt(tuggingSpeed(Vessel)=false , T) :-
    initiatedAt(gap(Vessel)=farFromPorts, T).
