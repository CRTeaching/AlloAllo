import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
import os.path

testing = False
location = ""
label = ""
descriptor = ""

def test(x = "The methods.py module has loaded successfully"):
    print(x)


#Method that returns the number of each unique catogory when a dataframe column is passed in
def count_cats(dataframe_column):
    counts = dataframe_column.value_counts()
    return counts

# Prompts a user for the file location (if debug = false) and then loads that file (if it exists)
def load(providedlocation = "", providedlabel = "", provideddescriptor = ""):
    global location
    global label
    global descriptor
    # If this isn't in debug mode
    if providedlocation != "":
        while True:
            if os.path.exists(providedlocation):
                location = providedlocation
                break
            else:
                if testing == True:
                    return -1
                
                print("That file doesn't exist, please try again")
                location = input()
                
        if testing == True:
            label = "name"
            descriptor = "overview"
            label = providedlabel if providedlabel != "" else label
            descriptor = provideddescriptor if provideddescriptor != "" else label
        else:
            label = input("What is the title (or index) of the column containing label data?")
            descriptor = input("What is the title (or index) of the column containing the test data?")

    else:
        location = "Data/baselineMovies.csv"
        label = "name"
        descriptor = "overview"
        
    data = pd.read_csv(location)

    if isinstance(label, int):
        label = data.columns[int(label)]

    if isinstance(descriptor, int):
        descriptor = data.columns[int(descriptor)]

    return data

def strip(data, evalColumn):
    data_clean = data[pd.notnull(data[descriptor])]
    templist = []
    loopvariable = data_clean.genres

    return [eval(y)[0][label]for y in data_clean[evalColumn]]





def test():
    global testing
    testing = True
    Data_Loading()
    Column_Load()

def Data_Loading():
    results = 0
    # If the data loaded (Success)
    if Data_Loading_Pass() == True:
        results += 1
    
    # If the data failed to load (Success)
    if Data_Loading_Fail() == True:
        results += 2
    
    # If the data failed to load after continuous attempts
    rangeTestFail = False
    for i in range(10):
        if Data_Loading_Fail() == False:
            rangeTestFail = True
    if rangeTestFail == True:
        results -= 2
    
    # If everything failed, except loading data that exists
    if results == 1:
        print("The was an error with the data loading fail method; it returned a value other than false. Fetching data that exists passes the test")
    
    # If everything failed except the error for loading data that doesn't exist
    if results == 2:
        print("There was an error with loading data that exists. Fetching data that doesn't exist passes the test")
    
    # If all tests were a sucess
    if results == 3:
        print("There were no errors with loading the data")

def Data_Loading_Pass():
    testData = load("Data/baselineMovies.csv")
    actualData = pd.read_csv("Data/baselineMovies.csv")
    
    return True if testData.equals(actualData) else False
    
def Data_Loading_Fail():
    testData = load("Data/dataThatDoesn'tExist.csv")
    
    if testData == -1:
        return True
    else:
        return False
    
def Column_Load():
    results = 0
    # If the column was retrieved (Success)
    if Column_Load_Pass() == True:
        results += 1
        
    if Column_Load_Fail() == True:
        results += 2
        
    if results == 1:
        print("")
        
        
def Column_Load_Pass():
    # Load the test data
    testData = load("Data/baselineMovies.csv")
    df_moviesclean = testData[pd.notnull(testData.overview)]
    y_genres = strip(testData, "genres")
    
    return True if len(y_genres) == 13507 else False
        
def Column_Load_Fail():
    testData = load("Data/baselineMovies.csv", "non-existing label", "non-existing descriptor")
    df_moviesclean = testData[pd.notnull(data.overview)]
    y_genres = strip(testData, "genres")
    print(len(y_genres))
    return True if len(y_genres) == 0 else False