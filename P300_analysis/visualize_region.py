import pandas as pd
import numpy as np
import os
ORDER = ["FP1", "FP2", "F3", "F4", "F7", "F8", "C3", "C4", "P3", "P4", "O1", "O2", "T3", "T4", "T5", "T6", "FZ", "CZ", "PZ"] # This will change if Wavi changes their lead names
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

def visualize_region(df, node_order_list, save_file_name):
	num_subplots = len(node_order_list)
	plt.rcParams["figure.figsize"] = (22,2*num_subplots)
	fig, ax = plt.subplots(num_subplots)
	for subplot_index, node_name in enumerate(node_order_list):
		line_segments = []
		colors = []
		voltage_values = df[node_name].values
		artifact_values = df[node_name+'_Artifact'].values
		min_y = min(voltage_values)
		max_y = max(voltage_values)
		for i in range(len(voltage_values)-1):
			line_segments.append([[i,voltage_values[i]], [i+1,voltage_values[i+1]]])
			if max(artifact_values[i], artifact_values[i+1]) == 0:
				colors.append('black')
			elif max(artifact_values[i], artifact_values[i+1]) == 1:
				colors.append('blue')
			elif max(artifact_values[i], artifact_values[i+1]) > 1:
				colors.append('red')
			   
		line_segments2 = LineCollection(line_segments, linestyles='solid', colors=colors, linewidth=3)
		ax[subplot_index].add_collection(line_segments2)
		ax[subplot_index].set_xlim([0, 250])
		ax[subplot_index].set_ylim([min_y, max_y])
		ax[subplot_index].set(ylabel=node_name)
	plt.savefig(save_file_name)
	plt.show()
