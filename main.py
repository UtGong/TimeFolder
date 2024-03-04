import os
import time
import pandas as pd
from clustering.hcluster import perform_hierarchical_clustering
from treecut_selection.treecut_selector import find_best_treecut, find_best_treecut_restricted
from visualization.visualization import draw_init_line_plot, draw_merged_line_plot, compute_y_axis_parameters


def main():
    # Load and filter data
    csv_file_path = 'data/StnData_2020-2023_dailytemp.csv'
    date_range = ['2020-01-01', '2023-12-31']
    date_column = 'Date'
    value_column = 'Max'
    method = 'entropy'

    test_data = load_and_filter_data(
        csv_file_path, date_range, date_column, value_column)

    # Compute Y-axis parameters for plots
    y_params = compute_y_axis_parameters(
        min(test_data[value_column]), max(test_data[value_column]))

    # Create output folder
    folder_name = create_output_folder(date_range, method)

    # Initial plot
    plot_initial_data(test_data, date_column,
                      value_column, y_params, folder_name, method)

    # Perform hierarchical clustering
    root_node, clustering_time = perform_clustering(
        test_data, date_column, value_column, method)

    # Find best tree cut
    best_cut, treecut_time = select_best_treecut(root_node, clustering_time, method)

    # Merge data and plot
    merged_data = merge_data(best_cut)
    plot_merged_data(merged_data, y_params, folder_name, method)

def load_and_filter_data(csv_file_path, date_range, date_column, value_column):
    csv = pd.read_csv(csv_file_path)
    csv[date_column] = pd.to_datetime(csv[date_column])
    filtered_data = csv[(csv[date_column] >= date_range[0])
                        & (csv[date_column] <= date_range[1])]
    filtered_data = filtered_data.reset_index(drop=True)
    print(f"Filtered data length: {len(filtered_data[value_column])}")
    return filtered_data


def create_output_folder(date_range, method):
    folder_name = date_range[0] + "-" + date_range[1]
    output_path = os.path.join('output/StnData_max/', method, folder_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return folder_name


def plot_initial_data(data, date_column, value_column, y_params, folder_name, method):
    init_plt = draw_init_line_plot(data, date_column, value_column, *y_params)
    init_plt.savefig(os.path.join(
        'output/StnData_max', method, folder_name, 'init.png'))


def perform_clustering(data, date_column, value_column, method):
    start_time = time.time()
    root_node = perform_hierarchical_clustering(
        data, date_column, value_column, method)
    elapsed_time = time.time() - start_time
    print("--- hcluster: %s seconds ---" % elapsed_time)
    return root_node, elapsed_time


def select_best_treecut(root_node, prev_elapsed_time, method):
    start_time = time.time()
    print("treecut level: %s ---" % 7)
    # best_cut = find_best_treecut(root_node, method)
    best_cut = find_best_treecut_restricted(root_node, method, 7)
    elapsed_time = time.time() - start_time + prev_elapsed_time
    print("--- select best treecut: %s seconds ---" % elapsed_time)
    return best_cut, elapsed_time


def merge_data(best_cut):
    res = []
    for node in best_cut:
        res.append({"data": node.data[0], "date": node.date.split("|")[0]})
        if best_cut.index(node) == len(best_cut)-1:
            res.append(
                {"data": node.data[-1], "date": node.date.split("|")[1]})
    print("Merged data length:", len(res))
    return res


def plot_merged_data(data, y_params, folder_name, method):
    plt = draw_merged_line_plot(data, *y_params)
    plt.savefig(os.path.join('output/StnData_max', method, folder_name, 'merged.png'))


if __name__ == "__main__":
    main()
