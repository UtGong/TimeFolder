import pandas as pd
import matplotlib.pyplot as plt


def data_transformation(data_name, time_column, user_column, status_column):
    file_path = "data/" + data_name + ".csv"
    df = pd.read_csv(file_path)
    
    # sort by time_column and only keep the first 10000 rows
    df = df.sort_values(by=[time_column]).head(1000000)

    unique_id_num = df[user_column].nunique()
    unique_id = df[user_column].unique()
    
    # filter df to only keep 100 unique value of user_column
    df = df[df[user_column].isin(unique_id[:30])]
    
    # filter the rows that has the lowest 10 value in the column time_column
    df = df[df[time_column] > df[time_column].quantile(0.1)]
    
    # Assuming df is your DataFrame
    grouped = df.groupby(time_column)

    def transform_group(group):
        return [{'user_id': row[user_column], 'task_status': row[status_column]} for index, row in group.iterrows()]

    transformed_df = grouped.apply(transform_group).reset_index()
    transformed_df.columns = ['time_value', 'user_task_status']
    
    # add new column tp_value to the transformed_df, where tp_value = sum(for each type of task_status, count the number of users that have that task_status at that time/total number of users), do not use lambda
    transformed_df['tp_value'] = transformed_df['user_task_status'].apply(lambda x: sum([x.count(task_status) / unique_id_num for task_status in x]))
    # only keep column event_date, tp_value  
    df = transformed_df[['time_value', 'tp_value']]
    
    # to csv, save in path 'data/transformed_symbseq.csv'
    df.to_csv("data/ss_to_ts.csv", index=False)

    return transformed_df, unique_id
    