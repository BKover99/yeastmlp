# Import packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import skimage.io
import skimage.filters
import skimage.measure
import seaborn as sns
import os
import glob


def load_floc_data(file):
    """
    Load OD measurements data from an Excel file.

    Args:
        file (str): Path to the Excel file.

    Returns:
        pandas.DataFrame: Loaded data with rows where the first column is numeric or string with length <= 3.
    """
    # read in file
    data = pd.read_excel(file)
    # retain only rows where the first column is numeric or string with length <= 3
    data = data[
        (data.iloc[:, 0].str.len() <= 3)
        | (data.iloc[:, 0] == "Unused")
        | (pd.to_numeric(data.iloc[:, 0], errors="coerce").notna())
    ]
    return data


def results_from_df(df, sqrt_n_measurements, neg_control_num, map_file):
    """
    Calculate results from a DataFrame of OD data.

    Args:
        df (pandas.DataFrame): DataFrame containing the OD data.
        sqrt_n_measurements (int): Square root of the number of measurements per well.
        neg_control_num (int): Index of the negative control well.
        map_file (str): Path to the strain map Excel file.

    Returns:
        pandas.DataFrame: DataFrame with calculated CVs and corresponding strain information.
    """
    identifiers = []
    data_list = []
    for i in range(
        0, len(df), sqrt_n_measurements + 1
    ):  # sqrt_n_scans_per_well_plus_one is 11 for seg and wt, and sometimes 10
        identifiers.append(df.iloc[i, 0])
        data_list.append(df.iloc[i + 1 : i + sqrt_n_measurements + 1])

    CVs = []
    # find the 38th entry in data_list.
    control = data_list[neg_control_num]  # 37 for seg, 82 for wi
    # replace entries with Unused to np.nan
    control = control.replace("Unused", np.nan)
    control = control.to_numpy().flatten()
    control = control[~np.isnan(control)]
    # take mean of control
    control_mean = np.mean(control)

    # loading in the strains
    strain_map = pd.read_excel(map_file, header=None)
    # creating a np array of the strains
    strains = strain_map.to_numpy().flatten()
    # take as many strains as there are entries in data_list
    strains = strains[0 : len(data_list)]

    for i in data_list:

        # change entries with Unused to 0

        i = i.replace("Unused", np.nan)
        i = np.array(i).flatten()
        i = i[~np.isnan(i)]

        i = [x for x in i if isinstance(x, float)]

        # subtract control_mean
        i = i - control_mean
        cv = np.std(i) / np.mean(i)
        CVs.append(cv)
    CVs[neg_control_num] = 0
    # if any value is less than 0, set it to 0
    CVs = [0 if x < 0 else x for x in CVs]
    CV_dataframe = pd.DataFrame({"Position": identifiers, "CV": CVs, "Strain": strains})

    return CV_dataframe


def folder_to_results(
    folder, sqrt_n_measurements, neg_control_num, map_file, groupby="Strain"
):
    """
    Calculate results from a folder of OD data files.

    Args:
        folder (str): Path to the folder containing the OD data files.
        sqrt_n_measurements (int or list): Square root of the number of measurements per well (single value or list).
        neg_control_num (int or list): Index of the negative control well (single value or list).
        map_file (str): Path to the strain map Excel file.
        groupby (str): Grouping variable for the results ("Strain" or "Position"). Default is "Strain".

    Returns:
        pandas.DataFrame: DataFrame with calculated CVs grouped by the specified variable.
    """

    files = glob.glob(folder + "/*.xlsx")
    # order files based on the number at the end of the file name
    files = sorted(files, key=lambda x: int(os.path.splitext(x)[0].split("_")[-1]))

    CV_dataframe_list = []
    # if sqrt_n_measurements is not an array than make an array of length files from sqrt_n_measurements
    if not isinstance(sqrt_n_measurements, list):
        sqrt_n_measurements = [sqrt_n_measurements] * len(files)
    if not isinstance(neg_control_num, list):
        neg_control_num = [neg_control_num] * len(files)
    for file, sqrt_n_mes, neg_ctrl_num in zip(
        files, sqrt_n_measurements, neg_control_num
    ):
        df = load_floc_data(file)
        CV_dataframe = results_from_df(df, sqrt_n_mes, neg_ctrl_num, map_file)
        CV_dataframe_list.append(CV_dataframe)
    results = pd.concat(CV_dataframe_list)
    # groupby but dont sort
    if groupby == "Strain":
        final_results = results.groupby("Strain", sort=False).mean()
        final_results["sem"] = results.groupby("Strain").sem()
    elif groupby == "Position":

        final_results = results.groupby("Position", sort=False).mean()
        final_results["sem"] = results.groupby("Position").sem()
    # else return error
    else:
        print("groupby must be Strain or Position")
        return

    return final_results


def heatmap_from_df(df):
    """
    Create a heatmap from a DataFrame of CV values.

    Args:
        df (pandas.DataFrame): DataFrame containing the CV values.

    Returns:
        tuple: Figure and axis objects of the heatmap plot.
    """

    # CV column to array
    array = df["CV"].to_numpy()

    array = array.reshape(8, 12)
    fig, ax = plt.subplots()
    im = ax.imshow(array, cmap="viridis")
    ax.set_xticks(
        np.arange(len(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]))
    )
    ax.set_yticks(np.arange(len(["A", "B", "C", "D", "E", "F", "G", "H"])))
    ax.set_yticklabels(["A", "B", "C", "D", "E", "F", "G", "H"])
    ax.set_xticklabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    # make sure to show all ticks

    # rotate the tick labels and set their alignment
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    # create colorbar
    cbar = ax.figure.colorbar(im, ax=ax)

    return fig, ax


def barchart_from_df(df):
    """
    Create a bar chart from a DataFrame of CV values.

    Args:
        df (pandas.DataFrame): DataFrame containing the CV values.

    Returns:
        tuple: Figure and axis objects of the bar chart plot.
    """
    fig, ax = plt.subplots(figsize=(20, 10))
    ax.bar(df.index, df["CV"], yerr=df["sem"])
    ax.set_xlabel("Name")
    ax.set_ylabel("CV")
    # twist the x-axis labels
    ax.set_xticklabels(df.index, rotation=90)
