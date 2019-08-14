# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 09:44:40 2019

@author: LAING3
"""
# imports
import pandas as pd
import os
import sys
from fuzzywuzzy import fuzz
from tqdm import tqdm


def select_file():
    """
    Asks the user to select an Excel file from the files in the current directory.
    Then, asks the user input parameters for these files:
        - How many rows to skip,
        - Which columns contain dates
    
    Returns a dictionary containing:
        - filepath : filepath of the selected file,
        - skiprows : number of rows to skip at the beginning of the file,
        - fuzzycolumn : column index (1-indexed) of the column to use for fuzzy-lookup
    """
    
    print("Here are the .xlsx files in the current directory:")
    xlsx_files = [x for x in os.listdir() if x.endswith('.xlsx')]
    if len(xlsx_files) == 0:
        print("The current directory must contain at least 1 .xlsx file!")
        print("Please copy the files you want to perform a Fuzzy Lookup on within the same directory as this program.")
        print("Exiting...")
        sys.exit(0)
              
    for i, file in enumerate(xlsx_files):
        print("{}: {}".format(i, file))
    file_selected = False
    while not file_selected:
        # ask for user selection of the file to process
        file_idx = input("Please select a file (use the index number / exit with 'q'): ")
        print("\n")
        if file_idx == "q":
            sys.exit(0)
        # ask for user input for heading row skip
        header_row_input = input("Please provide the row number where the header is located (1-indexed): (exit with 'q'):")
        print("\n")
        if header_row_input == "q":
            sys.exit(0)
     
        try:
            file_idx = int(file_idx)
            filepath_str = xlsx_files[file_idx]
            file_selected = True
            return dict(filepath=filepath_str, header_row=int(header_row_input))
        
        except ValueError:
            print("You must enter a valid index number!")
        except IndexError:
            print("This number does not point to an existing file!")


def read_file_for_fuzzy(filepath, header_row):
    """
    """
    print("Loading {}, please wait...".format(filepath))
    
    df = pd.read_excel(filepath, header=header_row-1)
    print("{} loaded successfully!".format(filepath))
    return df


def select_fuzzy_column(filename, df):  
    """
    Allows for user selection of the column to use for Fuzzy Lookup within a pandas dataframe
    
    Returns the 0-index value of the selected column
    """
    
    print("Here are the columns found in {}:".format(filename))
    for idx, col in enumerate(df.columns):
        print("{}: {}".format(idx, col))
    
    fuzzy_column_selected = False
    while fuzzy_column_selected == False:
        fuzzy_column_idx = input("Please select a column to use for the fuzzy match (use the index number / exit with 'q'): ")
        if fuzzy_column_idx == "q":
                sys.exit(0)
        try:
            fuzzy_column_idx = int(fuzzy_column_idx)
            fuzzy_column_selected = True
        except ValueError:
            print("You must enter a valid number!")
        except IndexError:
            print("This number does not point to an existing column!")
    
    print("Column '{}' selected.".format(df.columns[fuzzy_column_idx]))
    print("\n")
    return fuzzy_column_idx


def set_fuzzy_parameters():
    """
    Asks the user for two fuzzy lookup parameters:
        - result_limit: Number of results to return per match
        - score_threshold: Score threshold to use (integer between 0 and 100) (all match scores below the threshold won't be kept)
        
    Returns a dictionary with the selected values for each key. The score threshold is divided by 100 before the output.
    """
    # Ask for number of results to return per item
    result_limit_selected = False
    while result_limit_selected == False:
        result_limit = input("How many results do you want to retrieve for each item (the more results, the longer this will take / exit with 'q'): ")
        if result_limit == "q":
            sys.exit(0)
        try:
            result_limit = int(result_limit)
            result_limit_selected = True
        except ValueError:
            print("You must enter a valid integer!")
    
    # Ask for score threshold
    score_threshold_selected = False
    while score_threshold_selected == False:
        score_threshold = input("What matching score threshold should be used? (0-100; recommended: 85) (exit with 'q'): ")
        if score_threshold == "q":
            sys.exit(0)
        try:
            score_threshold = int(score_threshold)
            score_threshold_selected = True
        except ValueError:
            print("You must enter a valid integer from 0 to 100!")
   
    return (result_limit, score_threshold)


# Main thread
def main():
    # Startup
    print("------------------------------------")
    print(" ______ _    _ ______________     __",
          "|  ____| |  | |___  /___  /\ \   / /",
          "| |__  | |  | |  / /   / /  \ \_/ / ",
          "|  __| | |  | | / /   / /    \   /  ",
          "| |    | |__| |/ /__ / /__    | |   ",
          "|_|     \____//_____/_____|   |_|   ", sep="\n")
    print("------------------------------------")

    
    # Setting input files parameters
    print("\n")
    print("STEP 1: SELECT A FILE WITH THE VALUES TO MATCH")
    first_file = select_file()
    print("\n")
    print("STEP 2: SELECT A FILE WITH THE VALUES TO BE MATCHED AGAINST")
    second_file = select_file()
    
    # Reading files as pandas dataframes
    first_fuzzydf = read_file_for_fuzzy(first_file['filepath'], first_file['header_row'])
    print("\n")
    second_fuzzydf = read_file_for_fuzzy(second_file['filepath'], second_file['header_row'])
    
    print("\n")
    print("STEP 3: SELECT THE COLUMNS TO MATCH")
    # Select columns to match:
    first_fuzzycolumn = select_fuzzy_column(first_file['filepath'], first_fuzzydf)
    print("\n")
    second_fuzzycolumn = select_fuzzy_column(second_file['filepath'], second_fuzzydf)
    
    # Slice dataframes so they only contain the columns to match:
    first_fuzzydf = first_fuzzydf.iloc[: , first_fuzzycolumn]
    second_fuzzydf = second_fuzzydf.iloc[: , second_fuzzycolumn]
    
    print("\n")
    print("STEP 4: SET FUZZY MATCH PARAMETERS")
    # Setting fuzzy parameters
    result_limit, score_threshold = set_fuzzy_parameters()
    
    print("\n")
    print("SETUP COMPLETE")
    
    # Pandas implementation:
    print("Preparing Match Index, please wait...")
    first_col = first_file['filepath'] + ',' + first_fuzzydf.name
    second_col = second_file['filepath'] + ',' + second_fuzzydf.name
    
    output_index = pd.MultiIndex.from_product([first_fuzzydf.unique(), second_fuzzydf.unique()], 
                                               names = [first_col, second_col] 
                                               )
    output_df = pd.DataFrame(index=output_index).reset_index()
    
    # Performing Fuzzy
    print("Performing Fuzzy Match, please wait...")
    tqdm.pandas()
    output_df['Token_Sort_Ratio'] = output_df.progress_apply(lambda row: fuzz.token_sort_ratio(row[first_col], row[second_col]), axis=1)
    output_df = output_df[output_df['Token_Sort_Ratio'] >= score_threshold]
    
    output_df.to_csv('fuzzy_match_output.csv')
    open_file = input("Fuzzy Match Complete! File 'fuzzy_match_output.csv' written to disk. Do you wish to open it (y/n)?")
    if open_file == 'y':
        os.system('start fuzzy_match_output.csv')
    else:
        pass
    
    # Dask implementation:
    ## Setting output Dataframe
    #output_df = pd.DataFrame(columns=[first_fuzzydf.name, second_fuzzydf.name, 'match'], dtype='object')
    #output_df['match'] = output_df['match'].astype('float')
    #dmaster = dd.from_pandas(first_fuzzydf, npartitions = int(mp.cpu_count()))
    #dmaster['match'] = dmaster.apply(lambda x: helper(x, second_fuzzydf), axis=1, meta=output_df)

    
if __name__ == "__main__":
    main()
    
