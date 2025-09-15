import os
from os import listdir
from os.path import isfile, join
import sys
from time import sleep, process_time_ns
from datetime import datetime
import csv

from data_loader.data_loading import readAppDynamicData, createQueries, createCachedFacts

from problog.program import PrologFile, PrologString
from problog.engine import DefaultEngine
from problog import get_evaluatable
from problog.formula import LogicFormula, LogicDAG
from problog.sdd_formula import SDD
from problog.ddnnf_formula import DDNNF
from problog.cnf_formula import CNF

topDir = os.getcwd()

dynamic_grounding = True
large_windows = False
ground_time = True
measure_memory = False

clock = None
theta = 1e-06


event_calculus_file = PrologFile(topDir + '/EC-files/event_calculus.pl')

examples = {'c': 'caviar', 'm': 'maritime'}
times = {'c': [0, [40]], 'm': [1443650400, [1]]}
example = sys.argv[1]

prolog_files = topDir + '/../examples/' + examples[example] + '/Prob_EC_files/event_description'
example_dir = topDir + '/../examples/' + examples[example] + '/datasets'



if example == 'c':
	clock = 40
else:
	clock = 1

if example_dir:
	inputFiles = []
	for root, dirs, files in os.walk(example_dir):
		if dirs:
			continue
		if files:
			for f in files:
				if f.endswith('.csv'):
					inputFiles.append(root + '/' + f)
	inputFiles = sorted(inputFiles)
	results_dir = topDir + '/../examples/' + examples[example] + '/results/Prob-EC/'
	declarations = None
	rules = None
	hierarchy = []
	for root, dirs, files in os.walk(prolog_files):
		if dirs:
			continue
		if files:
			for f in files:
				if f.endswith('.pl'):
					if 'declarations' in f:
						declarations = PrologFile(root + '/' + f)
					else:
						rules = PrologFile(root + '/' + f)
				else:
					with open(root + '/' + f) as fr:
						for line in fr:
							if 'hierarchy' in line:
								line = line.replace(' ', '').split('(')[-1].split(')')[0].split(',')
								args = []
								if len(line) > 3:
									args = list(line[2:-1])
								hierarchy.append((line[0], line[1], args, int(line[-1])))


def main():
	if not os.path.exists(results_dir):
		os.makedirs(results_dir)

	# Run experiments

	print('Running experiments...')
	dstart = datetime.now()

	run_from_file()

	dend = datetime.now()
	dexp = dend - dstart
	print('System time elapsed for experiments...')
	print(dexp)

	print('Done!')


def run_from_file():

	windows = times[example][1]
	start_time = times[example][0]

	for w in windows:

		for inputFile in inputFiles:
			print(inputFile)

			final_write_dir = results_dir + inputFile.split('/')[-1].split('.csv')[0] + '/'
			if not os.path.exists(final_write_dir):
				os.makedirs(final_write_dir)
			
			with open(inputFile) as efr:
				for eline in efr:
					pass

			er_start_total = process_time_ns()

			end_time = int(eline.split('|')[1]) + clock
			print(end_time)

			step = w
			# create the base db
			engine = DefaultEngine()
			db = engine.prepare(event_calculus_file)
			for statement in declarations:
				db += statement
			for statement in rules:
				db += statement

			data = open(inputFile)
			csv_f = csv.reader(data, delimiter='|')
			previous_row = None

			results_file = open(final_write_dir + 'CEs-wm=%d' % w, 'w')
			stats = []
			kc = []
			memory = []
			computed_probs = {}

			for initTime in range(start_time, end_time, step):
				
				er_start_w = process_time_ns()

				qt = initTime + step

				print('ER: ', qt, ' Remaining steps: ', int(round((end_time - qt) / step)))

				entities, facts, previous_row = readAppDynamicData(csv_f, initTime, qt, previous_row)

				facts = PrologString(facts)
				cached_facts, entities = createCachedFacts(computed_probs, entities, large_windows, theta=theta, startTime=initTime+clock)
				queries = PrologString(createQueries(entities, hierarchy, time=qt+clock, gt=ground_time, dg=dynamic_grounding))

				# measure compilation time
				er_start_kc = process_time_ns()
				# extend db
				db_w = db.extend()
				for statement in facts:
					db_w += statement
				for statement in PrologString(cached_facts):
					db_w += statement
				for statement in queries:
					db_w += statement
				db_w = engine.prepare(db_w)
				lf = engine.ground_all(db_w)
				
				dag = LogicDAG.create_from(lf)
				cnf = CNF.create_from(dag)
				ddnnf = DDNNF.create_from(cnf)
				# end measure compilation time
				er_end_kc = process_time_ns()

				computed_probs = ddnnf.evaluate()

				del db_w

				writeResults(results_file, computed_probs)
				er_end_w = process_time_ns()
				stats.append(int(round(((er_end_w - er_start_w) / 1e6))))
				kc.append(int(round(((er_end_kc - er_start_kc) / 1e6))))

			er_end_total = process_time_ns()
			total_time = int(round(((er_end_total - er_start_total) / 1e6)))
			writeStats(final_write_dir, stats, total_time, kc, w)

			data.close()
			results_file.close()


def writeResults(results, ce_probs):

	sym_str = ''

	for ce in ce_probs:
		prob = ce_probs[ce]
		if prob >= theta and ce.is_ground:
			sym_str += '{:.9f}'.format(prob) + '::' + str(ce) + '.\n'
	results.write(sym_str)


def writeStats(w_dir, stats, total_time, kc, window):
	with open(w_dir + 'stats-wm=%d' % window, 'w') as fw:
		fw.write('Times:\n')
		fw.write('[')
		fw.write(', '.join(map(str, stats)))
		fw.write(']\n\n')
		total = sum(stats)
		average = round(total / len(stats))
		kc_total = sum(kc)
		kc_mean = kc_total / len(kc)
		fw.write('Total/Sum/Average Time: ' + str(total_time) + '/' + str(total) + '/' + str(average) + '\n\n')
		fw.write('Sum/Average KC Time: ' + str(kc_total) + '/' + str(kc_mean) + '\n\n')


if __name__ == "__main__":
	main()
