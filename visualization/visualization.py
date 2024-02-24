import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

def setup_plot(dates, values, title, y_start, y_end, gap, line_color='green'):
    """
    Shared function to set up and customize the plot.

    Args:
    - dates (list): List of dates for the x-axis.
    - values (list): List of values for the y-axis.
    - title (str): Title of the plot.
    - y_start (float): The starting value of the y-axis.
    - y_end (float): The ending value of the y-axis.
    - gap (float): The interval between y-axis ticks.
    - line_color (str): Color of the line plot.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(dates, values, marker='o', linestyle='-', color=line_color)

    plt.title(title, fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Value', fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gcf().autofmt_xdate()

    plt.ylim(y_start, y_end)
    plt.yticks(np.arange(y_start, y_end + gap, gap))

    return plt

def draw_init_line_plot(data, date_column, value_column, y_start, y_end, gap):
    dates, values = data[date_column], data[value_column]
    return setup_plot(dates, values, 'Value Over Time', y_start, y_end, gap)

def draw_merged_line_plot(data, y_start, y_end, gap):
    values = [point['data'] for point in data]
    dates = [datetime.strptime(point['date'].strip(), '%Y-%m-%d %H:%M:%S') for point in data]
    return setup_plot(dates, values, 'Merged Data Value Over Time', y_start, y_end, gap, line_color='blue')


def compute_y_axis_parameters(y_min, y_max):
    """
    Computes the start, end, and gap for the y-axis based on the min and max values of the data.

    Args:
    - y_min (float): The minimum value in the data.
    - y_max (float): The maximum value in the data.

    Returns:
    - tuple: A tuple containing the start, end, and gap values for the y-axis.
    """
    # Print for debugging
    print("y_min: ", y_min, " y_max: ", y_max)

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
