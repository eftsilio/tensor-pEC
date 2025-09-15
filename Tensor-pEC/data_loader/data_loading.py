
from src.processEvents import InputEvent


def readAppDynamicData(csv_file, initTime: int, queryTime: int, declarations: dict, previous_rows=None):

	kept_rows = []

	if previous_rows:

		for row in previous_rows:

			time = int(row[1])
			if initTime < time <= queryTime:
				assertInputEvents(time, row, declarations)
			else:
				kept_rows += [row]

	for row in csv_file:

		time = int(row[1])

		if initTime < time <= queryTime:

			assertInputEvents(time, row, declarations)

		elif time > queryTime:
			kept_rows += [row]
			previous_rows = kept_rows
			break

	return previous_rows


def assertInputEvents(time: int, row: list, declarations: dict):

	event = (row[0],)
	if row[3] == 'false' or row[3] == 'true':
		event += (row[3],)

	if event in declarations:
		event_dim = declarations[event]['Ndim']
		if event_dim == 1:
			index = (row[declarations[event]['index'][0]],)
		else:
			index = ()
			for i in declarations[event]['index']:
				index += ((row[i],),)

		assertSimpleEvent(event, time, index, event_dim, float(row[-1]))


def assertSimpleEvent(event, time, index, dim, prob):

	if event in InputEvent.instances:

		InputEvent.instances[event].__update__(index, time, prob)

	else:
		InputEvent(event, index, dim, time, prob)
