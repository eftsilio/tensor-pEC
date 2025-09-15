
from src.processEvents import InputEvent
from src.processSimpleFluents import SimpleFluent
from time import process_time
from . import declarations

from scipy import sparse as sp
import numpy as np


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Person %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def initiatedAtPerson():

    x = InputEvent.__getTimeMatrix__(('walking',))
    r1 = x

    x = InputEvent.__getTimeMatrix__(('running',))
    r2 = r1 + x - r1.multiply(x)

    x = InputEvent.__getTimeMatrix__(('active',))
    r3 = r2 + x - r2.multiply(x)

    x = InputEvent.__getTimeMatrix__(('abrupt',))
    r4 = r3 + x - r3.multiply(x)

    result = r4
    return result


def terminatedAtPerson():

    return InputEvent.__getTimeMatrix__(('disappear',))


def holdsAtPerson(open_tensor, termAtQt):

    initiations = initiatedAtPerson()
    terminations = terminatedAtPerson()
    matrix_B = initiations - initiations.multiply(terminations) + open_tensor
    matrix_C = matrix_B + terminations + termAtQt

    return matrix_B, matrix_C


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LONG-TERM BEHAVIOUR: fighting(Person, Person2) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def initiatedAtFighting():

    x = InputEvent.__getTimeMatrix__(('abrupt',))
    y = SimpleFluent.__getHoldsAtMatrix__(('person', 'true'), dim=1)
    z = InputEvent.__getTimeMatrix__(('close_fightDist', 'true'), dim=2)
    w = InputEvent.__getTimeMatrix__(('inactive',))
    dim = declarations[('fighting', 'true')]['Ndim'] - 1
    ones = np.ones((SimpleFluent.dim1 ** dim, 1))

    p2 = y - y.multiply(w)
    p1 = x

    p2 = sp.kron(ones, p2, format='csr')
    p1 = sp.kron(p1, ones, format='csr')

    result = p1.multiply(z).multiply(p2)

    return result


def terminatedAtFighting():

    x = InputEvent.__getTimeMatrix__(('walking',))
    y = InputEvent.__getTimeMatrix__(('running',))
    w = InputEvent.__getTimeMatrix__(('disappear',))
    z = InputEvent.__getTimeMatrix__(('close_fightDist', 'false'), dim=2)
    dim = declarations[('fighting', 'true')]['Ndim'] - 1
    ones = np.ones((SimpleFluent.dim1 ** dim, 1))

    p1 = sp.kron(x, ones, format='csr')
    p2 = sp.kron(ones, x, format='csr')
    r1 = p1 + p2 - p1.multiply(p2)

    p1 = sp.kron(y, ones, format='csr')
    p2 = sp.kron(ones, y, format='csr')
    r2 = p1 + p2 - p1.multiply(p2)

    r2 = (r1 + r2 - r1.multiply(r2)).multiply(z)

    p1 = sp.kron(w, ones, format='csr')
    p2 = sp.kron(ones, w, format='csr')
    r3 = p1 + p2 - p1.multiply(p2)

    t2 = r2

    t1 = r3

    return t1, t2


def holdsAtFighting(open_tensor, termAtQt):

    initiations = initiatedAtFighting()
    t1, t2 = terminatedAtFighting()
    matrix_B = initiations - initiations.multiply(t1) + open_tensor
    matrix_C = t1 + t2 - t1.multiply(t2) + matrix_B - matrix_B.multiply(t2) + termAtQt

    return matrix_B, matrix_C


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LONG-TERM BEHAVIOUR: fighting(Person, Person2) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def initiatedAtMeeting():

    x = InputEvent.__getTimeMatrix__(('active',))
    y = SimpleFluent.__getHoldsAtMatrix__(('person', 'true'), dim=1)
    z = InputEvent.__getTimeMatrix__(('close_interactDist', 'true'), dim=2)
    q = InputEvent.__getTimeMatrix__(('inactive',))
    dim = declarations[('meeting', 'true')]['Ndim'] - 1
    ones = np.ones((SimpleFluent.dim1 ** dim, 1))

    r1 = sp.kron(x, ones, format='csr')

    p1_r2 = q.multiply(y)
    p1_r2 = sp.kron(p1_r2, ones, format='csr')
    p2_r2 = sp.kron(ones, x, format='csr')
    r2 = p1_r2 - p1_r2.multiply(p2_r2)

    r2 = r1 + r2 - r1.multiply(r2)

    p2 = sp.kron(ones, y, format='csr')

    result = r2.multiply(p2).multiply(z)

    return result


def terminatedAtMeeting():

    x = InputEvent.__getTimeMatrix__(('walking',))
    y = InputEvent.__getTimeMatrix__(('running',))
    s = InputEvent.__getTimeMatrix__(('abrupt',))
    w = InputEvent.__getTimeMatrix__(('disappear',))
    z = InputEvent.__getTimeMatrix__(('close_meetDist', 'false'), dim=2)
    dim = declarations[('meeting', 'true')]['Ndim'] - 1
    ones = np.ones((SimpleFluent.dim1 ** dim, 1))

    p1 = sp.kron(x, ones, format='csr')
    p2 = sp.kron(ones, x, format='csr')
    r1 = (p1 + p2 - p1.multiply(p2)).multiply(z)

    r2 = sp.kron(y, ones, format='csr')
    r2 = r1 + r2 - r1.multiply(r2)

    r3 = sp.kron(s, ones, format='csr')
    t2 = r2 + r3 - r2.multiply(r3)

    p1 = sp.kron(w, ones, format='csr')
    p2 = sp.kron(ones, w, format='csr')
    r4 = p1 + p2 - p1.multiply(p2)
    p2 = sp.kron(ones, y, format='csr')
    r4 = r4 + p2 - r4.multiply(p2)
    p2 = sp.kron(ones, s, format='csr')
    t1 = r4 + p2 - r4.multiply(p2)

    return t1, t2


def holdsAtMeeting(open_tensor, termAtQt):

    initiations = initiatedAtMeeting()
    t1, t2 = terminatedAtMeeting()
    matrix_B = initiations - initiations.multiply(t1) + open_tensor
    matrix_C = t1 + t2 - t1.multiply(t2) + matrix_B - matrix_B.multiply(t2) + termAtQt

    return matrix_B, matrix_C


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LONG-TERM BEHAVIOUR: moving(Person, Person2) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def initiatedAtMoving():

    x = InputEvent.__getTimeMatrix__(('walking',))
    y = InputEvent.__getTimeMatrix__(('disappear',))
    z = InputEvent.__getTimeMatrix__(('close_moveDist', 'true'), dim=2)
    w = InputEvent.__getTimeMatrix__(('orientation', 'true'), dim=2)
    dim = declarations[('moving', 'true')]['Ndim'] - 1
    ones = np.ones((SimpleFluent.dim1 ** dim, 1))

    x1 = sp.kron(x, ones, format='csr')
    x2 = sp.kron(ones, x, format='csr')
    y1 = sp.kron(y, ones, format='csr')
    y2 = sp.kron(ones, y, format='csr')

    r1 = x1.multiply(x2).multiply(z).multiply(w)
    r2 = r1 - r1.multiply(y1)

    result = r2 - r2.multiply(y2)

    return result


def terminatedAtMoving():

    x = InputEvent.__getTimeMatrix__(('walking',))
    y1 = InputEvent.__getTimeMatrix__(('active',))
    y2 = InputEvent.__getTimeMatrix__(('inactive',))
    s = InputEvent.__getTimeMatrix__(('running',))
    t = InputEvent.__getTimeMatrix__(('abrupt',))
    w = InputEvent.__getTimeMatrix__(('disappear',))
    z = InputEvent.__getTimeMatrix__(('close_moveDist', 'true'), dim=2)
    z2 = InputEvent.__getTimeMatrix__(('close_moveDist', 'false'), dim=2)
    z3 = InputEvent.__getTimeMatrix__(('orientation', 'true'), dim=2)
    dim = declarations[('moving', 'true')]['Ndim'] - 1
    ones = np.ones((SimpleFluent.dim1 ** dim, 1))

    a1 = sp.kron(y1, ones, format='csr')
    a2 = sp.kron(ones, y1, format='csr')
    i1 = sp.kron(y2, ones, format='csr')
    i2 = sp.kron(ones, y2, format='csr')
    s1 = sp.kron(s, ones, format='csr')
    s2 = sp.kron(ones, s, format='csr')
    ab1 = sp.kron(t, ones, format='csr')
    ab2 = sp.kron(ones, t, format='csr')
    x1 = sp.kron(x, ones, format='csr')
    x2 = sp.kron(ones, x, format='csr')
    d1 = sp.kron(w, ones, format='csr')
    d2 = sp.kron(ones, w, format='csr')

    t_1 = a1.multiply(a2)
    t_2 = a1.multiply(i2)
    t_3 = a2.multiply(i1)
    t_4 = s1 + s2 - s1.multiply(s2)
    t_5 = ab1 + ab2 - ab1.multiply(ab2)

    t_1a = t_1 + t_2 - t_1.multiply(t_2)
    t_2a = t_1a + t_3 - t_1a.multiply(t_3)
    t_3a = t_2a + t_4 - t_2a.multiply(t_4)
    tf = t_3a + t_5 - t_3a.multiply(t_5)

    root_b = z3.multiply(z).multiply(x1).multiply(x2)
    root_b = root_b - root_b.multiply(d1)
    root_b = root_b - root_b.multiply(d2)

    A_2 = x1 - x1.multiply(tf)
    A_2 = A_2 - A_2.multiply(x2)
    A_2 = A_2 - A_2.multiply(z2)

    A_1 = x1 + x2.multiply(z2) - x1.multiply(x2).multiply(z2) + tf
    A_1 = A_1 - tf.multiply(x1) - tf.multiply(x2).multiply(z2)
    A_1 = A_1 - tf.multiply(x1).multiply(x2).multiply(z2)

    A = A_2 - A_1

    B = x1.multiply(x2)
    B = B - B.multiply(z2)
    B = B - B.multiply(tf)
    B = B - B.multiply(z).multiply(z3)

    AB = A + B
    root_a = AB - d1 - AB.multiply(d1)
    root_a = root_a - d2 - root_a.multiply(d2)
    root_a = root_a * -1

    return root_a, root_b
    

def holdsAtMoving(open_tensor, termAtQt):

    terminations, initiations = terminatedAtMoving()
    matrix_B = initiations + open_tensor
    matrix_C = terminations + termAtQt

    return matrix_B, matrix_C


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% LONG-TERM BEHAVIOUR: leaving_object(Person, Object) %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def initiatedAtLeavingObject():

    x = InputEvent.__getTimeMatrix__(('appear',))
    y = InputEvent.__getTimeMatrix__(('inactive',))
    z = SimpleFluent.__getHoldsAtMatrix__(('person', 'true'), dim=1)
    dim = declarations[('leaving_object', 'true')]['Ndim'] - 1
    ones = np.ones((SimpleFluent.dim1 ** dim, 1))

    s = x.multiply(y)
    s = sp.kron(ones, s, format='csr')
    z = sp.kron(z, ones, format='csr')

    v = InputEvent.__getTimeMatrix__(('close_leaveDist', 'true'), dim=2)

    result = z.multiply(v).multiply(s)

    return result


def terminatedAtLeavingObject():

    x = InputEvent.__getTimeMatrix__(('disappear',))
    dim = declarations[('leaving_object', 'true')]['Ndim'] - 1
    ones = np.ones((SimpleFluent.dim1 ** dim, 1))

    result = sp.kron(ones, x, format='csr')

    return result


def holdsAtLeavingObject(open_tensor, termAtQt):

    initiations = initiatedAtLeavingObject()
    terminations = terminatedAtLeavingObject()
    matrix_B = initiations - initiations.multiply(terminations) + open_tensor
    matrix_C = matrix_B + terminations + termAtQt

    return matrix_B, matrix_C


definitions = {('person', 'true'):

                   {'initiatedAt': initiatedAtPerson, 'terminatedAt': terminatedAtPerson, 'holdsAt': holdsAtPerson},

               ('fighting', 'true'):

                   {'initiatedAt': initiatedAtFighting, 'terminatedAt': terminatedAtFighting, 'holdsAt': holdsAtFighting},

               ('meeting', 'true'):

                   {'initiatedAt': initiatedAtMeeting, 'terminatedAt': terminatedAtMeeting, 'holdsAt': holdsAtMeeting},

               ('moving', 'true'):

                   {'initiatedAt': initiatedAtMoving, 'terminatedAt': terminatedAtMoving, 'holdsAt': holdsAtMoving},

               ('leaving_object', 'true'):

                   {'initiatedAt': initiatedAtLeavingObject, 'terminatedAt': terminatedAtLeavingObject, 'holdsAt': holdsAtLeavingObject}
               }


def readDefinitions():

    tensors_dim = [1, 2]
    return definitions.keys(), definitions, tensors_dim
