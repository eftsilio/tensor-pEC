
from src.eventRecognition import *


class Event(EventRecognition):
	
	def __init__(self, event_str: tuple, dim: int):

		self.event_str = event_str
		self.ndim = dim
		self.matrix = None

	def __getString__(self):

		points = self.matrix.nonzero()[0]
		sym_str = ''
		for p in points:
			time = self.initTime + p

			sym_str += '(%s(%s' % (self.event_str, ','.join(map(str, self.index)))

			sym_str += '), [%d])\n' % time

		return sym_str
	

class InputEvent(Event):

	instances = {}

	def __init__(self, event_str: tuple, index: tuple, dim: int, time: int = None, prob: float = None):

		super().__init__(event_str, dim)

		if self.dynamic_grounding:
			EventRecognition.__updateEntities__(index)
		t = int((time - self.initTime) / self.clock)

		if dim == 1:
			x = self.map_entities[index]
		else:
			x = itemgetter(*index)(self.map_entities)
		self.init_matrix = defaultdict()
		self.init_matrix[x, t] = prob

		InputEvent.instances[event_str] = self

	def __update__(self, index: tuple, time: int, prob: float):

		if self.dynamic_grounding:
			EventRecognition.__updateEntities__(index)
		t = int((time - self.initTime) / self.clock)

		if self.ndim == 1:
			x = self.map_entities[index]
		else:
			x = itemgetter(*index)(self.map_entities)
		self.init_matrix[x, t] = prob

	@staticmethod
	def __getTimeMatrix__(event: tuple, dim: int = 1, negative: bool = False):

		if event in InputEvent.instances:

			matrix = InputEvent.instances[event].matrix

		else:
			matrix = InputEvent.empty[dim]

		if negative:
			return InputEvent.eye - matrix

		return matrix
	
	@classmethod
	def __finalize__(cls):

		for event in cls.instances:
			instance = cls.instances[event]
			matrix = sp.dok_matrix((cls.dim1 ** instance.ndim, cls.dim2))
			if instance.ndim > 1:
				for key in instance.init_matrix:
					i = 0
					for d in range(instance.ndim, 0, -1):
						i += key[0][d-1] * (cls.dim1 ** (instance.ndim - d))
					new_key = (i, key[-1])
					matrix[new_key] = instance.init_matrix[key]
			else:
				for key in instance.init_matrix:
					matrix[key] = instance.init_matrix[key]
			instance.matrix = matrix.tocsr()
			del instance.init_matrix

	@classmethod
	def __forget__(cls):

		for event in cls.instances:
			instance = cls.instances[event]
			del instance

		cls.instances = {}
