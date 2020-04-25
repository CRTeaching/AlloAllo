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

#Method that returns the number of each unique catogory when a dataframe column is passed in
def count_cats(dataframe_column):
    counts = dataframe_column.value_counts()
    return counts

# Prompts a user for the file location (if debug = false) and then loads that file (if it exists)
def load(location = ""):
    # If this isn't in debug mode
    if location != "":
        while True:
            if os.path.exists(location):
                break
            else:
                if testing == True:
                    return -1

                print("That file doesn't exist, please try again")
                providedlocation = input()
    else:
        location = "Data/baselineMovies.csv"

    return pd.read_csv(location)

def get_column(data, columnlocation = ""):
    if(columnlocation == ""):
        columnlocation = input("What is the colum header (or index) you wish to access?")

    if isinstance(columnlocation, int):
        columnlocation = data.columns[int(columnlocation)]

    if(columnlocation in data):
        return data[columnlocation]
    return []

def strip(data, name, overview, evalColumn):
    data_clean = data[pd.notnull(overview)]
    templist = []
    loopvariable = data_clean[evalColumn]

    return [eval(y)[0][name]for y in data_clean[evalColumn]]

def search_and_fit (x_train, y_train, search):
    print("Searching for the best paramaters and fitting the data....This may take a few minutes")
    try:
        trained_model = search.fit(x_train, y_train)
        return trained_model
    except:
        return None



##################################################################################
## Testing
##################################################################################


def test():
    global testing
    testing = True

    Data_Loading()
    Column_Load()
    Column_Load(True)
    Test_GridSearch()
    #Test_Predict()

    testing = False

def Data_Loading():
    result = ""
    # If the data loaded (Success)
    if Data_Loading_Pass() == True:
        result += "Data_Loading_Pass performed as expected. "
    else:
        result += "Data_Loading_Pass didn't perform as expected. "

    # If the data failed to load (Success)
    if Data_Loading_Fail() == True:
        result += "Data_Loading_Fail performed as expected. "
    else:
        result += "Data_Loading_Fail didn't perform as expected. "

    # If the data failed to load after continuous attempts
    rangeTestFail = False
    for i in range(10):
        if Data_Loading_Fail() == False:
            rangeTestFail = True

    if rangeTestFail == False:
        result += "Data_Loading_Fail looped performed as expected. "
    else:
        result += "Data_Loading_Fail looped didn't perform as expected. "
    print(result)

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

def Column_Load(with_str = True):
    response = ""
    if(with_str):
        if len(Column_Load_Pass()) == 0:
            response += "Column_Load_Pass didn't perform as expected. "
        else:
            response += "Column_Load_Pass performed as expected. "

        if len(Column_Load_Fail()) == 0:
            response += "Column_Load_Fail performed as expected. "
        else:
            response += "Column_Load_Fail didn't perform as expected. "

    print(response)

def Column_Load_Pass():
    testData = load("Data/baselineMovies.csv")
    return get_column(testData, "overview")

def Column_Load_Fail():
    testData = load("Data/baselineMovies.csv")
    return get_column(testData, "ooverview")

def Test_GridSearch():
    result = ""

    if GridSearch_Pass() == True:
        result += "GridSearch_Pass performs as expected. "
    else:
        result += "GridSearch_Pass does'nt perform as expected. "

    if GridSearch_Fail() == True:
        result += "GridSearch_Fail performs as expected. "
    else:
        result += "GridSearch_Fail doesn't perform as expected. "

    print(result)

def GridSearch_Pass():
    testData = load("Data/baselineMovies.csv")
    testDataClean = testData[pd.notnull(get_column(testData,"overview"))]
    y_genres = strip(testData, "name", get_column(testData, "overview"), "genres")
    X_train, X_test, y_train, y_test = train_test_split(testDataClean.overview, y_genres, test_size=0.2, random_state = 0)
    text_pipe = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),
    ])

    grid_params ={
        'vect__stop_words': ('english', None),
        'vect__strip_accents': ('ascii', 'unicode', None),
        'tfidf__use_idf': (True, False),
        'tfidf__smooth_idf': (True, False),
        'tfidf__sublinear_tf': (True, False),
        'tfidf__norm': ('l1', 'l2', None),
        }
    search = GridSearchCV(text_pipe, grid_params)
    trained_model = search_and_fit(X_train, y_train, search)

    predict_text = ["April 6th, 1917. As a regiment assembles to wage war deep in enemy territory, two soldiers are assigned to race against time and deliver a message that will stop 1,600 men from walking straight into a deadly trap."]

    return search.predict(predict_text)[0] == "Action"

def GridSearch_Fail():
    try:
        testData = load("Data/baselineMovies.csv")
        testDataClean = testData[pd.notnull(get_column(testData,"overview"))]
        y_genres = strip(testData, "name", get_column(testData, "overview"), "genres")
        X_train, X_test, y_train, y_test = train_test_split(testDataClean.overview, y_genres, test_size=0.2, random_state = 0)
        text_pipe = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', MultinomialNB()),
        ])

        grid_params ={
            'vect__stop_words': ('a language that does not exist', None),
            'vect__strip_accents': ('ascii', 'unicode', None),
            'something typed wrong': (True, False),
            'tfidf__smooth_idf': (True, False),
            'tfidf__sublinear_tf': (True, False),
            'tfidf__norm': ('l1', 'l2', None),
            }
        search = GridSearchCV(text_pipe, grid_params)
        trained_model = search_and_fit(X_train, y_train, search)
        return True
    except:
        return False
