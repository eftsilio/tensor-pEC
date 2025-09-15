
from src.eventRecognition import EventRecognition
from src.processSimpleFluents import SimpleFluent


def dynamicGrounding():

	for fluent in SimpleFluent.instances:
		sf = SimpleFluent.instances[fluent]
		for (entity, _) in sf.open_interval:
			EventRecognition.__updateEntities__(entity)
