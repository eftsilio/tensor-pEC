
from src.eventRecognition import *

from time import process_time
from scipy.sparse import linalg as lg
# from scikits.umfpack import spsolve
from itertools import groupby

# lg.use_solver(useUmfpack=True, assumeSortedIndices=True)

inf = float('inf')


class SimpleFluent(EventRecognition):
	instances = {}

	def __init__(self, fluent_str: tuple, ndim: int):

		self.fluent_str = fluent_str
		self.ndim = ndim

		self.intervals = {}
		self.open_interval = None
		self.matrix = None

		SimpleFluent.instances[fluent_str] = self

	def __getString__(self, create_intervals: bool = False):

		sym_str = ''
		arg = ()

		if len(self.fluent_str) > 2:
			arg = self.fluent_str[1:-1]

		if not create_intervals:
			probs = self.matrix.data
			indices = self.matrix.nonzero()
			current_entity = None
			entity_str = None
			for idx, (en_pos, t) in enumerate(zip(*indices)):
				if current_entity != en_pos:
					if self.ndim > 1:
						rem = en_pos
						en_get = ()
						for d in range(self.ndim, 0, -1):
							temp = int(rem / (self.dim1 ** (d - 1)))
							rem = rem - temp * (self.dim1 ** (d - 1))
							en_get += (temp,)
					else:
						en_get = (en_pos,)
					entity = itemgetter(*en_get)(self.inv_map_entities)
					current_entity = en_pos
					entity_str = ()
					if self.ndim > 1:
						for en in entity:
							entity_str += en
					else:
						entity_str = entity
					entity_str = ','.join(entity_str + arg)
				prob = probs[idx]
				time = self.initTime + t * self.clock
				if time <= self.qt:
					sym_str += '{:.9f}'.format(prob) + ' ::holdsAt(%s(%s)=%s, ' % (self.fluent_str[0], entity_str, self.fluent_str[-1])
					sym_str += str(self.initTime + t * self.clock) + ').\n'

		else:
			indices = groupby(zip(*self.matrix.nonzero()), lambda l: l[0])
			for en_pos, group in indices:
				if self.ndim > 1:
					rem = en_pos
					en_get = ()
					for d in range(self.ndim, 0, -1):
						temp = int(rem / (self.dim1 ** (d - 1)))
						rem = rem - temp * (self.dim1 ** (d - 1))
						en_get += (temp,)
				else:
					en_get = (en_pos,)
				entity = itemgetter(*en_get)(self.inv_map_entities)
				start_i = next(group)[-1]
				temp = start_i
				intervals = []
				for r in group:
					if r[1] - temp == 1:
						temp = r[-1]
					else:
						dist = temp - start_i
						start_i = self.initTime + start_i * self.clock
						end_i = start_i + dist * self.clock
						intervals.append((start_i, end_i))
						start_i = r[1]
						temp = start_i

				dist = temp - start_i
				start_i = self.initTime + start_i * self.clock
				end_i = start_i + dist * self.clock
				if end_i > self.qt + self.clock:
					end_i = inf
				intervals.append((start_i, end_i))
				self.intervals[entity] = intervals

			for i in self.intervals:
				if self.ndim == 1:
					entity = i
				else:
					entity = ()
					for en in i:
						entity += en

				entity = ','.join(entity + arg)

				sym_str += '(%s(%s)=%s, [' % (self.fluent_str[0], entity, self.fluent_str[-1])
				sym_str += ','.join(map(str, self.intervals[i])) + ']).\n'

		return sym_str

	def __execute__(self, definition: dict, linear: bool = False):

		open_matrix = None

		if linear:
			open_matrix = self.empty[self.ndim]
			if self.open_interval:
				open_matrix = sp.dok_matrix((self.dim1 ** self.ndim, self.dim2))
				for (entity, prob) in self.open_interval:
					if self.ndim == 1:
						i = self.map_entities[entity]
					else:
						x = itemgetter(*entity)(self.map_entities)
						i = 0
						for d in range(len(x)):
							i += x[d] * (self.dim1 ** (self.ndim - d - 1))
					open_matrix[i, 0] = prob
					open_matrix.tocsr()

		self.__holdsAtMatrix__(definition, open_matrix, linear)

		if not self.matrix.size:
			del SimpleFluent.instances[self.fluent_str]
			del self

	def __holdsAtMatrix__(self, definition, open_matrix, linear_method: bool = True):

		self.intervals = {}
		holdsAt = None

		if linear_method:

			shape = ((self.dim1 ** self.ndim) * self.dim2, 1)

			matrix_B, matrix_C = definition['holdsAt'](open_matrix, self.termAtQt[self.ndim])

			vector_b = matrix_B @ self.U
			vector_b = vector_b.reshape(shape, order='C')

			vector_t = np.reshape(matrix_C.todense(), newshape=(1, shape[0]), order='C')
			vector_t = -1.0 + vector_t[:, :-1]

			matrix_G = sp.diags_array([[1.0] * shape[0], vector_t], offsets=[0, -1], shape=(shape[0], shape[0]), format='csc')

			vector_h = lg.spsolve(matrix_G, vector_b, use_umfpack=True)
			vector_h[vector_h < 1e-06] = 0.0

			holdsAt = vector_h.reshape((self.dim1 ** self.ndim, self.dim2), order='C')
			holdsAt = sp.csr_matrix(holdsAt)

			indices = holdsAt[:, -1].nonzero()[0]
			probs = holdsAt[:, -1].data
			self.open_interval = []

			for idx, en_pos in enumerate(indices):
				rem = en_pos
				en_get = ()
				for d in range(self.ndim, 0, -1):
					temp = int(rem / (self.dim1 ** (d - 1)))
					rem = rem - temp * (self.dim1 ** (d - 1))
					en_get += (temp,)
				entity = itemgetter(*en_get)(self.inv_map_entities)
				self.open_interval.append((entity, probs[idx]))

		self.matrix = sp.csr_matrix(holdsAt)

	@staticmethod
	def __getHoldsAtMatrix__(fluent: tuple, dim: int = 1, negative: bool = False):

		if fluent in SimpleFluent.instances:

			matrix = SimpleFluent.instances[fluent].matrix

		else:
			matrix = SimpleFluent.empty[dim]

		if negative:
			return SimpleFluent.eye - matrix

		return matrix

	@classmethod
	def __forget__(cls):

		for fluent in cls.instances:
			instance = cls.instances[fluent]
			del instance

		cls.instances = {}

	@classmethod
	def __createNewInstance__(cls, fluent: tuple, dim: int):

		if fluent not in cls.instances:
			SimpleFluent(fluent, dim)

		return cls.instances[fluent]
