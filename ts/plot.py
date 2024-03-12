import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def generic_plot_setup(title, xlabel, ylabel, y_start, y_end, gap, dates=None, values=None, line_color='green', rotation=None, x_ticks=None):
    plt.figure(figsize=(12, 6))
    if dates is not None and values is not None:
        plt.plot(dates, values, marker='o', linestyle='-', color=line_color)
    
    plt.title(title, fontsize=14)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    plt.ylim(y_start, y_end)
    plt.yticks(np.arange(y_start, y_end + gap, gap))
    
    if rotation is not None and x_ticks is not None:
        plt.xticks(x_ticks, rotation=rotation)
    
    return plt

def draw_init_line_plot(data, date_column, value_column, y_start, y_end, gap):
    dates, values = data[date_column], data[value_column]
    return generic_plot_setup('Value Over Time', 'Date', 'Value', y_start, y_end, gap, dates, values)

def draw_merged_line_plot_non_linear(data, y_start, y_end, gap):
    values = [point.start_point.data for point in data]
    dates = [str(point.start_point.time_value).split(" ")[0] for point in data]
    x_values = range(len(dates))
    
    plt = generic_plot_setup('Value Over Time', 'Date', 'Value', y_start, y_end, gap, x_values, values, line_color='blue', rotation=45)
    
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xticks(x_values, dates, rotation=45)

    print("Merged data length: ", len(values))
    return plt

def draw_merged_line_plot(data, y_start, y_end, gap):
    values = [point.start_point.data for point in data]
    dates = [point.start_point.time_value for point in data]
    return generic_plot_setup('Value Over Time', 'Date', 'Value', y_start, y_end, gap, dates, values, line_color='blue')

def compute_y_axis_parameters(y_min, y_max):
    # Expand the range by 10% for aesthetic reasons
    range_expansion = 0.1 * (y_max - y_min)
    range_expansion = max(range_expansion, 0.1)  # Ensure at least a minimal expansion

    adjusted_min = y_min - range_expansion
    adjusted_max = y_max + range_expansion

    # Determine a suitable gap for the y-axis ticks
    ideal_range = adjusted_max - adjusted_min
    possible_gaps = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    gap = next((gap for gap in possible_gaps if ideal_range / gap <= 10), possible_gaps[-1])

    # Adjust start and end to align with the gap
    start = gap * round(adjusted_min / gap)
    end = gap * round(adjusted_max / gap + 0.5)  # Ensure rounding up for the end

    return start, end, gap
