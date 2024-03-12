import os
import time
import matplotlib.pyplot as plt
import pandas as pd
from data import build_time_frames
from cluster import find_mdl
from ts.plot import draw_init_line_plot, draw_merged_line_plot_non_linear, draw_merged_line_plot, compute_y_axis_parameters

def load_and_filter_data(csv_file_path, date_range, date_column, value_column):
    csv = pd.read_csv(csv_file_path)
    csv[date_column] = pd.to_datetime(csv[date_column])
    filtered_data = csv[(csv[date_column] >= date_range[0])
                        & (csv[date_column] <= date_range[1])]
    filtered_data = filtered_data.reset_index(drop=True)
    print(f"Filtered data length: {len(filtered_data[value_column])}")
    return filtered_data

def main():
    data_file_name = 'StnData_2020-2023_dailytemp'
    csv_file_path = 'data/' + data_file_name + '.csv'
    date_range = ['2020-01-01', '2023-12-31']
    date_column = 'Date'
    value_column = ['Max']
    
    dataset = load_and_filter_data(
        csv_file_path, date_range, date_column, value_column)
    
    start_time = time.time()

    tfs = build_time_frames(dataset, date_column, value_column)
    best_folded_timeline, min_dl = find_mdl(tfs)
    print("Length best folded timeline, ", len(best_folded_timeline))
    
    elapsed_time = time.time() - start_time
    print("Runtime: ", elapsed_time)

    # plot
    # create output folder
    if len(value_column) == 1:
        ts_type = 'single'
    else:
        ts_type = 'multi'
    folder_name = date_range[0] + "-" + date_range[1]
    output_path = os.path.join('output/ts/', ts_type, data_file_name, folder_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
     
    global_min = dataset[value_column[0]].min()
    global_max = dataset[value_column[0]].max()

    # Iterate over all columns specified in value_column to find the global min and max
    for column in value_column:
        column_min = dataset[column].min()
        column_max = dataset[column].max()
        global_min = min(global_min, column_min)
        global_max = max(global_max, column_max)
    # Compute Y-axis parameters for plots
    y_params = compute_y_axis_parameters(global_min, global_max)
    
    # Plot the initial data
    init_plt = draw_init_line_plot(dataset, date_column, value_column, *y_params)
    init_plt.savefig(os.path.join(output_path, 'init.png'))
    
    # Plot merged data
    plt = draw_merged_line_plot(best_folded_timeline, *y_params)
    plt.savefig(os.path.join(output_path, 'merged.png'))
    plt = draw_merged_line_plot_non_linear(best_folded_timeline, *y_params)
    plt.savefig(os.path.join(output_path, 'merged-nonlinear.png'))

if __name__ == "__main__":
    main()

