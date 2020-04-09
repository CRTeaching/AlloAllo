import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
import os.path

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
def load(debug = False):
    global location
    global label
    global descriptor
    # If this isn't in debug mode
    if debug == False:
        
        while True:
            location = input("What is the location of the csv file you wish to import?")
            if os.path.exists(location):
                break
            else:
                print("That file doesn't exist, please try again")
                
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