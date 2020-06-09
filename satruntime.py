import numpy as np
import pandas as pd

if __name__ == '__main__':
	df = pd.read_csv('SATALL12S.csv')
	feat_df = pd.read_csv('SATALL12S_data/SATALL12S_ft_vals_with_time.csv')
	feat_df.rename(columns={feat_df.columns[0]: 'INSTANCE_ID'}, inplace=True)
	# needed_df = df[df.columns[-3:]]
	# needed_df.insert(0, "INSTANCE_ID", df['INSTANCE_ID'])
	needed_df = feat_df

	best_solvers = np.genfromtxt('output_all.csv', delimiter=',')[1:]
	feature_times = np.genfromtxt('SATALL12S_data/SATALL12S_ft_times.csv', delimiter=',')[1:]
	solver_id = [5, 17, 26, 31, 13, 18, 20, 3, 8]
	solve_times = np.empty((0, 2))

	# Formula is (x - 1) * 5 + 4 (+4 for PAR, +1 for time)
	'''
	Logic as follows:
	Check solver 1 for time:
		if 12000, then +1200 to time and check 2
		else: total time = sum of feature comp times + solver 1 time
	Check solver 2 for time:
		if 12000, then +1200 to time and check backup
		else: total time = sum of feature comp times + solver 1 time + solver 2 time
	Check backup solver for time:
		total time = sum of feature comp times + solver 1 time + solver 2 time + backup time
		!no need to worry about whether backup solver = solver 1 or solver 2

	Note: the backup solver and the presolver are the same for the ALL category. Presolver is not run for the ALL category.
	'''

	for i in range(len(best_solvers)):
		tot_time = 0

		# Otherwise, compute features and run two solvers
		for j in range(1, len(feature_times[i])):
			if feature_times[i][j] != -512:
				tot_time += feature_times[i][j]

		col = (solver_id[int(best_solvers[i][1])] - 1) * 5 + 4
		first = df.iloc[i, col]
		if first != 12000:
			tot_time += first
			solve_times = np.vstack((solve_times, [int(best_solvers[i][0]), tot_time]))
			continue
		else:
			tot_time += 1200

		col2 = (solver_id[int(best_solvers[i][2])] - 1) * 5 + 4
		second = df.iloc[i, col2]
		if second != 12000:
			tot_time += second
			solve_times = np.vstack((solve_times, [int(best_solvers[i][0]), tot_time]))
			continue
		else:
			tot_time += 1200
		
		# Presolver:
		col3 = (solver_id[0] - 1) * 5 + 4
		backup = df.iloc[i, col3]
		if backup != 12000:
			tot_time += backup
		else:
			tot_time += 1200

		solve_times = np.vstack((solve_times, [int(best_solvers[i][0]), tot_time]))
	

	sat_run_df = pd.DataFrame({'INSTANCE_ID': solve_times[:, 0], 'SATzilla_runtime': solve_times[:, 1]})
	print(sat_run_df.info())

	res_df = pd.merge(needed_df, sat_run_df, on='INSTANCE_ID')
	# res_df.drop(res_df[(res_df[' lobjois_featuretime'] == -512) | (res_df[' lobjois_featuretime'] == 512)].index, inplace=True)
	res_df.to_csv('SATALL12S_for_ajay.csv', index=False)
	print(res_df[res_df.columns[-8:]].describe())
