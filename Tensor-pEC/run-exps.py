import os
from os import listdir
from os.path import isfile, join
import sys
from time import sleep, process_time_ns
from datetime import datetime
import csv


import src
from data_loader.data_loading import readAppDynamicData

topDir = os.getcwd()

fos = 'csr'
linear = True
dynamic_grounding = True

clock = None

examples = {'c': 'caviar', 'm': 'maritime'}
times = {'c': [0, [24360]], 'm': [1443650400, [610]]}
example = sys.argv[1]

example_dir = topDir + '/../examples/' + examples[example] + '/datasets'

sys.path.insert(1, topDir + '/../examples/' + examples[example])
import Tensor_pEC_files as app

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
	results_dir = topDir + '/../examples/' + examples[example] + '/results/Tensor-pEC/'


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

			with open(inputFile) as fr:
				for line in fr:
					pass

			er_start_total = process_time_ns()

			end_time = int(line.split('|')[1]) + w
			print(end_time)

			step = w
			er = src.ER(w, step, clock, dynamic_grounding, fos)
			cachingOrder, definitions, tensors_dim = app.readDefinitions()

			data = open(inputFile)
			csv_f = csv.reader(data, delimiter='|')
			previous_row = None

			results_file = open(final_write_dir + 'CEs-wm=%d' % w, 'w')
			stats = []
			memory = []

			for initTime in range(start_time, end_time, step):

				er_start_w = process_time_ns()

				qt = initTime + step

				if qt > end_time:
					break

				er.__windowParams__(initTime, qt)

				print('ER: ', qt, ' Remaining steps: ', int(round((end_time - qt) / step)))

				src.sev.__forget__()

				previous_row = readAppDynamicData(csv_f, initTime, qt, app.declarations, previous_row)

				if dynamic_grounding:
					app.dg()
					er.__updateParams__(tensors_dim)

				src.sev.__finalize__()

				er.__run__(cachingOrder, app.declarations, definitions, linear)

				writeResults(results_file, qt)
				er_end_w = process_time_ns()
				stats.append(int(round(((er_end_w - er_start_w) / 1e6))))

			er_end_total = process_time_ns()
			total_time = int(round(((er_end_total - er_start_total) / 1e6)))
			writeStats(final_write_dir, stats, total_time, w, step)

			data.close()
			results_file.close()
			src.simple.__forget__()
			src.sev.__forget__()
			del er
			# exit(1)


def writeResults(results, qt):
	results.write('ER: ' + str(qt) + '\n\n')

	for fluent in src.simple.instances:
		results.write(src.simple.instances[fluent].__getString__())

	results.write('\n\n')


def writeStats(w_dir, stats, total_time, window, step):
	with open(w_dir + 'stats-wm=%d' % window, 'w') as fw:
		fw.write('Times:\n')
		fw.write('[')
		fw.write(', '.join(map(str, stats)))
		fw.write(']\n\n')
		total = sum(stats)
		average = round(total / len(stats))
		fw.write('Total/Sum/Average Time: ' + str(total_time) + '/' + str(total) + '/' + str(average) + '\n\n')

		
if __name__ == "__main__":
	main()
