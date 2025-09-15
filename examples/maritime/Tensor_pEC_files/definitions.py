from src.processEvents import InputEvent
from src.processSimpleFluents import SimpleFluent
from . import declarations

import numpy as np
from scipy import sparse as sp

from time import process_time


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% GAP %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtGapNP():
    x = InputEvent.__getTimeMatrix__(('gap_start',))
    y = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    result = x.multiply(y)

    return result


def holdsAtGapNP(open_tensor, termAtQt):
    initiations = initiatedAtGapNP()
    terminations = terminatedAtGap()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


def initiatedAtGapFFP():
    x = InputEvent.__getTimeMatrix__(('gap_start',))
    y = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    result = x - x.multiply(y)

    return result


def holdsAtGapFFP(open_tensor, termAtQt):
    initiations = initiatedAtGapFFP()
    terminations = terminatedAtGap()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


def terminatedAtGap():
    x = InputEvent.__getTimeMatrix__(('gap_end',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))

    return x + y - x.multiply(y)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% STOPPED %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtStoppedNP():
    x = InputEvent.__getTimeMatrix__(('stop_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    result = x.multiply(z)

    return result


def holdsAtStoppedNP(open_tensor, termAtQt):
    initiations = initiatedAtStoppedNP()
    terminations = terminatedAtStopped()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


def initiatedAtStoppedFFP():
    x = InputEvent.__getTimeMatrix__(('stop_start',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearPorts', 'true'))

    result = x - x.multiply(z)

    return result


def holdsAtStoppedFFP(open_tensor, termAtQt):
    initiations = initiatedAtStoppedFFP()
    terminations = terminatedAtStopped()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


def terminatedAtStopped():
    x = InputEvent.__getTimeMatrix__(('stop_end',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = InputEvent.__getTimeMatrix__(('stop_start',))

    t1 = x + y - x.multiply(y)
    result = t1 - t1.multiply(z) + z

    return result


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LOWSPEED %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtLowSpeed():
    x = InputEvent.__getTimeMatrix__(('slow_motion_start',))

    return x


def terminatedAtLowSpeed():
    x = InputEvent.__getTimeMatrix__(('slow_motion_end',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = InputEvent.__getTimeMatrix__(('slow_motion_start',))

    t1 = x + y - x.multiply(y)
    result = t1 - t1.multiply(z) + z

    return result


def holdsAtLowSpeed(open_tensor, termAtQt):
    initiations = initiatedAtLowSpeed()
    terminations = terminatedAtLowSpeed()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LOWSPEED %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtChangingSpeed():
    x = InputEvent.__getTimeMatrix__(('change_in_speed_start',))

    return x


def terminatedAtChangingSpeed():
    x = InputEvent.__getTimeMatrix__(('change_in_speed_end',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = InputEvent.__getTimeMatrix__(('change_in_speed_start',))

    t1 = x + y - x.multiply(y)
    result = t1 + z - t1.multiply(z)

    return result


def holdsAtChangingSpeed(open_tensor, termAtQt):
    initiations = initiatedAtChangingSpeed()
    terminations = terminatedAtChangingSpeed()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% highSpeedNearCoast %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtHighSpeedNearCoast():
    x = InputEvent.__getTimeMatrix__(('velocity_GrHcNCMax',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearCoast', 'true'))

    return x.multiply(z)


def terminatedAtHighSpeedNearCoast():
    x = InputEvent.__getTimeMatrix__(('velocity_LtHcNCMax',))
    y = InputEvent.__getTimeMatrix__(('velocity_GrHcNCMax',))
    z = SimpleFluent.__getHoldsAtMatrix__(('withinArea', 'nearCoast', 'true'))

    t1 = z - z.multiply(y)
    result = t1 - t1.multiply(x)

    return result


def holdsAtHighSpeedNearCoast(open_tensor, termAtQt):
    initiations = initiatedAtHighSpeedNearCoast()
    terminations = terminatedAtHighSpeedNearCoast()
    matrix_B = initiations + open_tensor
    matrix_C = sp.csr_matrix(1.0 - terminations.toarray())

    return matrix_B, matrix_C


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% movingSpeed %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtMovingSpeedBelow():
    x = InputEvent.__getTimeMatrix__(('velocity_GrMovMin_LtMin',))

    return x


def initiatedAtMovingSpeedNormal():
    x = InputEvent.__getTimeMatrix__(('velocity_GrMin_LtMax',))

    return x


def initiatedAtMovingSpeedAbove():
    x = InputEvent.__getTimeMatrix__(('velocity_GrMax',))

    return x


def terminatedAtMovingSpeed():
    x = InputEvent.__getTimeMatrix__(('velocity_GrMovMin_LtMin',))
    y = InputEvent.__getTimeMatrix__(('velocity_GrMin_LtMax',))
    z = InputEvent.__getTimeMatrix__(('velocity_GrMax',))
    w = InputEvent.__getTimeMatrix__(('velocity_LtMovMin',))
    s = InputEvent.__getTimeMatrix__(('gap_start',))

    t1 = x + y - x.multiply(y)
    t2 = t1 + z - t1.multiply(z)
    t3 = t2 + w - t2.multiply(w)
    result = t3 + s - t3.multiply(s)

    return result


def holdsAtMovingSpeedBelow(open_tensor, termAtQt):
    initiations = initiatedAtMovingSpeedBelow()
    terminations = terminatedAtMovingSpeed()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


def holdsAtMovingSpeedNormal(open_tensor, termAtQt):
    initiations = initiatedAtMovingSpeedNormal()
    terminations = terminatedAtMovingSpeed()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


def holdsAtMovingSpeedAbove(open_tensor, termAtQt):
    initiations = initiatedAtMovingSpeedAbove()
    terminations = terminatedAtMovingSpeed()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% tuggingSpeed %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtTuggingSpeed():
    x = InputEvent.__getTimeMatrix__(('velocity_GrTugMin_LeTugMax',))

    return x


def terminatedAtTuggingSpeed():
    x = InputEvent.__getTimeMatrix__(('velocity_GrTugMin_LeTugMax',))
    y = InputEvent.__getTimeMatrix__(('velocity_GrTugMax',))
    z = InputEvent.__getTimeMatrix__(('velocity_LtTugMin',))
    w = InputEvent.__getTimeMatrix__(('gap_start',))

    t1 = x + y - x.multiply(y)
    t2 = t1 + z - t1.multiply(z)
    result = t2 + w - t2.multiply(w)

    return result


def holdsAtTuggingSpeed(open_tensor, termAtQt):
    initiations = initiatedAtTuggingSpeed()
    terminations = terminatedAtTuggingSpeed()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% WITHIN_AREA %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def initiatedAtWithinAreaFishing():
    x = InputEvent.__getTimeMatrix__(('entersArea_fishing',))

    return x


def initiatedAtWithinAreaNearCoast():
    x = InputEvent.__getTimeMatrix__(('entersArea_nearCoast',))

    return x


def initiatedAtWithinAreaNearCoast5k():
    x = InputEvent.__getTimeMatrix__(('entersArea_nearCoast5k',))

    return x


def initiatedAtWithinAreaNearPorts():
    x = InputEvent.__getTimeMatrix__(('entersArea_nearPorts',))

    return x


######################################################################################################################
def terminatedAtWithinAreaFishing():
    x = InputEvent.__getTimeMatrix__(('leavesArea_fishing',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = InputEvent.__getTimeMatrix__(('entersArea_fishing',))

    t1 = x + y - x.multiply(y)
    result = t1 + z - t1.multiply(z)

    return result


def terminatedAtWithinAreaNearCoast():
    x = InputEvent.__getTimeMatrix__(('leavesArea_nearCoast',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = InputEvent.__getTimeMatrix__(('entersArea_nearCoast',))

    t1 = x + y - x.multiply(y)
    result = t1 + z - t1.multiply(z)

    return result


def terminatedAtWithinAreaNearCoast5k():
    x = InputEvent.__getTimeMatrix__(('leavesArea_nearCoast5k',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = InputEvent.__getTimeMatrix__(('entersArea_nearCoast5k',))

    t1 = x + y - x.multiply(y)
    result = t1 + z - t1.multiply(z)

    return result


def terminatedAtWithinAreaNearPorts():
    x = InputEvent.__getTimeMatrix__(('leavesArea_nearPorts',))
    y = InputEvent.__getTimeMatrix__(('gap_start',))
    z = InputEvent.__getTimeMatrix__(('entersArea_nearPorts',))

    t1 = x + y - x.multiply(y)
    result = t1 + z - t1.multiply(z)

    return result


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def holdsAtWithinAreaFishing(open_tensor, termAtQt):
    initiations = initiatedAtWithinAreaFishing()
    terminations = terminatedAtWithinAreaFishing()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


def holdsAtWithinAreaNearCoast(open_tensor, termAtQt):
    initiations = initiatedAtWithinAreaNearCoast()
    terminations = terminatedAtWithinAreaNearCoast()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


def holdsAtWithinAreaNearCoast5k(open_tensor, termAtQt):
    initiations = initiatedAtWithinAreaNearCoast5k()
    terminations = terminatedAtWithinAreaNearCoast5k()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


def holdsAtWithinAreaNearPorts(open_tensor, termAtQt):
    initiations = initiatedAtWithinAreaNearPorts()
    terminations = terminatedAtWithinAreaNearPorts()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

definitions = {('withinArea', 'fishing', 'true'):

                   {'initiatedAt': initiatedAtWithinAreaFishing, 'terminatedAt': terminatedAtWithinAreaFishing, 'holdsAt': holdsAtWithinAreaFishing},

               ('withinArea', 'nearCoast', 'true'):

                   {'initiatedAt': initiatedAtWithinAreaNearCoast, 'terminatedAt': terminatedAtWithinAreaNearCoast, 'holdsAt': holdsAtWithinAreaNearCoast},

               ('withinArea', 'nearCoast5k', 'true'):

                   {'initiatedAt': initiatedAtWithinAreaNearCoast5k, 'terminatedAt': terminatedAtWithinAreaNearCoast5k, 'holdsAt': holdsAtWithinAreaNearCoast5k},

               ('withinArea', 'nearPorts', 'true'):

                   {'initiatedAt': initiatedAtWithinAreaNearPorts, 'terminatedAt': terminatedAtWithinAreaNearPorts, 'holdsAt': holdsAtWithinAreaNearPorts},

               ('gap', 'nearPorts'):

                   {'initiatedAt': initiatedAtGapNP, 'terminatedAt': terminatedAtGap, 'holdsAt': holdsAtGapNP},

               ('gap', 'farFromPorts'):

                   {'initiatedAt': initiatedAtGapFFP, 'terminatedAt': terminatedAtGap, 'holdsAt': holdsAtGapFFP},

               ('stopped', 'nearPorts'):

                   {'initiatedAt': initiatedAtStoppedNP, 'terminatedAt': terminatedAtStopped, 'holdsAt': holdsAtStoppedNP},

               ('stopped', 'farFromPorts'):

                   {'initiatedAt': initiatedAtStoppedFFP, 'terminatedAt': terminatedAtStopped, 'holdsAt': holdsAtStoppedFFP},

               ('lowSpeed', 'true'):

                   {'initiatedAt': initiatedAtLowSpeed, 'terminatedAt': terminatedAtLowSpeed, 'holdsAt': holdsAtLowSpeed},

               ('changingSpeed', 'true'):

                   {'initiatedAt': initiatedAtChangingSpeed, 'terminatedAt': terminatedAtChangingSpeed, 'holdsAt': holdsAtChangingSpeed},

               ('highSpeedNearCoast', 'true'):

                   {'initiatedAt': initiatedAtHighSpeedNearCoast, 'terminatedAt': terminatedAtHighSpeedNearCoast, 'holdsAt': holdsAtHighSpeedNearCoast},

               ('movingSpeed', 'below'):

                   {'initiatedAt': initiatedAtMovingSpeedBelow, 'terminatedAt': terminatedAtMovingSpeed, 'holdsAt': holdsAtMovingSpeedBelow},

               ('movingSpeed', 'above'):

                   {'initiatedAt': initiatedAtMovingSpeedAbove, 'terminatedAt': terminatedAtMovingSpeed, 'holdsAt': holdsAtMovingSpeedAbove},

               ('movingSpeed', 'normal'):

                   {'initiatedAt': initiatedAtMovingSpeedNormal, 'terminatedAt': terminatedAtMovingSpeed, 'holdsAt': holdsAtMovingSpeedNormal},

               ('tuggingSpeed', 'true'):

                   {'initiatedAt': initiatedAtTuggingSpeed, 'terminatedAt': terminatedAtTuggingSpeed, 'holdsAt': holdsAtTuggingSpeed},

               }


def readDefinitions():

    tensors_dim = [1]
    return definitions.keys(), definitions, tensors_dim
