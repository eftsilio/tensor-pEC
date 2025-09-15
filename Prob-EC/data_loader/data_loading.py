from itertools import permutations


def readAppDynamicData(csv_file, initTime: int, queryTime: int, previous_rows=None):
	kept_rows = []
	entities = set()
	facts_to_assert = '\n'

	if previous_rows:

		for row in previous_rows:

			time = int(row[1])
			if initTime < time <= queryTime:
				entities, facts_to_assert = assertInputEvents(row, entities, facts_to_assert)
			else:
				kept_rows += [row]

	for row in csv_file:

		time = int(row[1])

		if initTime < time <= queryTime:

			entities, facts_to_assert = assertInputEvents(row, entities, facts_to_assert)

		elif time > queryTime:
			kept_rows += [row]
			previous_rows = kept_rows
			break

	return entities, facts_to_assert, previous_rows


def assertInputEvents(row: list, entities: set, facts: str):
	if len(row) == 5:
		facts += row[-1] + '::happensAt(' + row[0] + '(' + row[3] + '), ' + row[1] + ').\n'
		entities.add(row[3])
	else:
		facts += row[-1] + '::holdsAtIE(' + row[0] + '(' + row[4] + ',' + row[5] + ')=' + row[3] + ', ' + row[
			1] + ').\n'
		entities.add(row[4])
		entities.add(row[5])

	return entities, facts


def createQueries(entities: set, complex_events: list, time: int, gt: bool = True, dg: bool = False):
	perms = {}
	queries = '\n'

	t = 'T'
	if gt:
		t = str(time)

	for ce in complex_events:
		if dg:
			if ce[-1] not in perms:
				perms[ce[-1]] = list(permutations(entities, ce[-1]))
			for tup_en in perms[ce[-1]]:
				if ce[2]:
					for arg in ce[2]:
						queries += 'query(' + 'holdsAt(' + ce[0] + '(' + ','.join(tup_en) + ',' + arg + ')=' + ce[
							1] + ',' + t + ')' + ').\n'
				else:
					queries += 'query(' + 'holdsAt(' + ce[0] + '(' + ','.join(tup_en) + ')=' + ce[
						1] + ',' + t + ')' + ').\n'

	return queries


def createCachedFacts(prob_ces: dict, entities: set, lw: bool, theta: float, startTime: int):
	cached = '\n'

	for ce in prob_ces:
		prob = prob_ces[ce]
		if prob >= theta and ce.is_ground:
			time = int(ce.args[-1])
			if time == startTime:
				if lw:
					cached += str(prob) + '::' + str(ce) + '.\n'
				else:
					cached += str(prob) + '::cached(' + str(ce) + ').\n'
				en_tuple = ce.args[0].args[0].args
				for en in en_tuple:
					en = str(en)
					if en not in entities:
						entities.add(en)

	return cached, entities
