## 2025-10-22 Region of Interest (ROI) Analysis Code

# import necessary packages and functions
import numpy as np
import pandas as pd
from ysmr.helper_file import get_data
from ysmr.plot_functions import rose_graph

frame_height = 1080
frame_width = 1920

# run video to generate the cv file

# read cv file

# convert to pandas data frame
# get_data function is defined in helper_file.py
# """load csv file to pandas data frame.
#
#     Default dtype:
#
#     dtype = {
#         'TRACK_ID':         np.uint32,
#         'POSITION_T':       np.uint32,
#         'POSITION_X':       np.float64,
#         'POSITION_Y':       np.float64,
#         'WIDTH':            np.float64,
#         'HEIGHT':           np.float64,
#         'DEGREES_ANGLE':    np.float64,
#     }
#
#     :param csv_file_path: csv file to read
#     :param dtype: dict of columns to be loaded and their data types
#     :type dtype: dict
#     :param check_sorted: check if df is sorted by TRACK_ID / POSITION_T if available
#     :type check_sorted: bool
#     :return: pandas data frame
#     """

testdf = get_data(r"C:\Users\kisch050\Desktop\Graduate School Work\240119 S. oneidensis Chemotaxis\Videos_for_Analysis_Manuscript\251020_Results\IMG_0230_analysed.csv",
         dtype=None,
         check_sorted=True)

# load pandas data frame
# print(testdf.shape) # output was (855783, 7)

# split the pandas data frame into 5 sections along the x-axis
# 0 to x1 (start to left side of bar 1)
# x1 to x2 (left side of bar 1 to right side of bar 1)
# x2 to x3 (right side of bar 1 to left side of bar 2)
# x3 to x4 (left side of bar 2 to right side of bar 2)
# x4 to end (right side of bar 2 to end)

df1 = testdf.copy()
max_x = df1['POSITION_X'].max()
print(max_x)
# define the bins
# The last bin includes max_x
bins = [0, 600, 610, 1010, 1020, max_x + 1]
# Define labels for the bins
labels = [
    '0_to_600_Electrode1',
    '600_to_610_Electrode1Edge',
    '610_to_1010_Gap',
    '1010_to_1020_Electrode2Edge',
    '1020_to_MaxX_Electrode2'
]

# Create the new column that categorizes each row's POSITION_X
df1['position_group'] = pd.cut(
    df1['POSITION_X'],
    bins=bins,
    labels=labels,
    right=False, # This makes the left side of the bin inclusive, such as [0,600)
    include_lowest=True # First interval is left inclusive
)

# Isolate the unique TRACK_ID for each group
# def.groupby temporarily (so doesn't alter the original df I think) partitions the df based on the position_group column
# indexing at TRACK_ID selects the column of interest from the column groups created by groupby
# .unique() is the aggregation function applied to selected column (the TRACK_ID) within each group
    # .unique() gathers all the TRACK_ID values and returns only the unique ones
    # so if track 100 appears 5 times, it will only return the number 100 once. Is this a problem??
    # result is a series
# .to_dict() takes the resulting series (unique TRACK_ID grouped by position) and converts to dictionary
    # the keys of the dictionary are position group names such as 0_to_600_Electrode1.
    # the values of the dictionary are lists of unique TRACK_IDs that are found in that region

grouped_tracks = df1.groupby('position_group', observed=False)['TRACK_ID'].unique().to_dict()

# test to see if it worked
df1_check = df1[df1['TRACK_ID'] == 3678]
print(df1_check['POSITION_X'].min(), df1_check['POSITION_X'].max())

# check to see how many tracks are in each section
for label, tracks in grouped_tracks.items():
    print(f"{label}: {len(tracks)} unique tracks")

# generate plots for each section
