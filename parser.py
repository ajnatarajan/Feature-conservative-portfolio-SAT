import pandas as pd
import numpy as np
import os

if __name__ == '__main__':
	for filename in os.listdir(os.getcwd()):
		if '.csv' in filename:
			print('Working on ', filename)
			df = pd.read_csv(filename)

			slv_times_cols = ['INSTANCE_ID']
			slv_times_cols.extend([x for x in df.columns if '_time' in x.lower()])
			slv_times_df = df[slv_times_cols]

			ft_times_cols = ['INSTANCE_ID']
			ft_times_cols.extend([x for x in df.columns if '_featuretime' in x.lower()])
			ft_times_df = df[ft_times_cols]

			# could not find a matching pattern between features
			col_vals = df.columns.values
			ft_start_idx = 0
			for i in range(len(col_vals)):
				if 'INSTANCE_ID' in col_vals[i]:
					ft_start_idx = i

			solver_cols = col_vals[:ft_start_idx]
			solver_names = set()
			for name in solver_cols:
				split_name = name.split('_')
				solver_names.add(split_name[0])
			solver_names.remove('INSTANCE')
			mapping = dict()
			for name in solver_names:
				
			col_vals = col_vals[ft_start_idx:]
			ft_vals_cols = [x for x in col_vals if '_featuretime' not in x.lower()]
			ft_vals_df = df[ft_vals_cols]
			ft_vals_with_time_df = df[col_vals]

			all_times_df = df[np.append(slv_times_cols, ft_times_cols[1:])]
			all_times_with_vals_df = df[np.append(slv_times_cols, col_vals[1:])]

			dir_name = filename[:-4]
			os.mkdir(dir_name + '_data')
			ft_times_df.to_csv(dir_name + '_data' + '/' + dir_name + '_ft_times.csv', index=False)
			slv_times_df.to_csv(dir_name + '_data' + '/' + dir_name + '_slv_times.csv', index=False)
			ft_vals_df.to_csv(dir_name + '_data' + '/' + dir_name + '_ft_vals.csv', index=False)
			ft_vals_with_time_df.to_csv(dir_name + '_data' + '/' + dir_name + '_ft_vals_with_time.csv', index=False)
			all_times_df.to_csv(dir_name + '_data' + '/' + dir_name + '_ft_and_slv_times.csv', index=False)
			all_times_with_vals_df.to_csv(dir_name + '_data' + '/' + dir_name + 'ft_and_slv_times_with_vals.csv', index=False)
