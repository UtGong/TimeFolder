import os
from symbolic_seq.data_transformation import data_transformation
from symbolic_seq.plot import plotting, plotting_nonlinear
from data import build_time_frames
from cluster import find_mdl
import pandas as pd
import time
import matplotlib.pyplot as plt

def main():
    # data_name = "symbolic_seq"
    # time_column = "event_date"
    # user_column = "sub_ID"
    # status_column = 'behav_comptype_h'
    
    data_name = "case2"
    time_column = "operate_time"
    user_column = "operator_id"
    status_column = 'phase'
    
    print("Starting data transformation...")
    start_time = time.time()
    df, unique_id = data_transformation(data_name, time_column, user_column, status_column)
    elapsed_time = time.time() - start_time
    print("Done transforming data...")
    print("Runtime: ", elapsed_time)
    
    output_path = os.path.join('output/symbolic_seq/', data_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        
    fig = plotting_with_status(df, unique_id, 'time_value', 'user_task_status')
    fig.savefig(output_path + "/init" + '.png')
    
    data_file_name = 'ss_to_ts'
    csv_file_path = 'data/' + data_file_name + '.csv'
    date_column = 'time_value'
    value_column = ["tp_value"]
    
    dataset = pd.read_csv(csv_file_path)
    # dataset[date_column] = pd.to_datetime(dataset[date_column])
    print("len(original)", len(dataset))
    
    start_time = time.time()

    print("Start find mdl process...")
    tfs = build_time_frames(dataset, date_column, value_column)
    best_folded_timeline, min_dl = find_mdl(tfs)
    print("Done finding mdl process...")
    elapsed_time = time.time() - start_time
    
    print("len(best_folded_timeline)", len(best_folded_timeline))
    print("Runtime: ", elapsed_time)
    
    dates = [point.start_point.time_value for point in best_folded_timeline]
    dates.append(best_folded_timeline[-1].end_point.time_value)

    df = df[df['time_value'].isin(dates)]
    fig = plotting_with_status(df, unique_id, 'time_value', 'user_task_status')
    fig.savefig(output_path + "/folded" + '.png')
    # fig = plotting_nonlinear(df, unique_id, 'time_value', user_column)
    # fig.savefig(output_path + "folded_nonlinear" + '.png')
    
def plotting_with_status(df, unique_id, time_column, user_task_status_column):
    # Extract all unique task statuses
    all_statuses = set([status['task_status'] for status_list in df[user_task_status_column] for status in status_list])
    
    # Generate a color map with a unique color for each task status
    # Uses a colormap from matplotlib - you can choose another if you prefer different colors
    colormap = plt.cm.get_cmap('viridis', len(all_statuses))
    color_map = {status: colormap(i) for i, status in enumerate(all_statuses)}
    
    fig, ax = plt.subplots()
    for _, row in df.iterrows():
        date = row[time_column]
        for status_info in row[user_task_status_column]:
            user_id = status_info['user_id']
            task_status = status_info['task_status']
            # Find the index of the user_id in unique_id to use as y-coordinate
            y = list(unique_id).index(user_id)
            # Plot using the color mapped to task_status
            ax.plot(date, y, 'o', color=color_map[task_status])
    
    ax.set_yticks(range(len(unique_id)))
    ax.set_yticklabels(unique_id)
    ax.set_xlabel("Time Range")
    ax.set_ylabel("Unique ID")
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Optionally, create a legend for the task statuses
    for status, color in color_map.items():
        ax.plot([], [], 'o', color=color, label=status)
    ax.legend(title="Task Status", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    return plt

    
main()