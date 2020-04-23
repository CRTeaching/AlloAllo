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
                providedlocation = input()
                
        if testing == True:
            label = "name"
            descriptor = "overview"
            
            if providedlabel != "":
                label = providedlabel
              
            if provideddescriptor != "":
                descriptor = provideddescriptor
        else:
            label = input("What is the title (or index) of the column containing label data?")
            descriptor = input("What is the title (or index) of the column containing the test data?")

    else:
        location = "Data/baselineMovies.csv"
        label = "name"
        descriptor = "overview"
        
    data = pd.read_csv(location)

    if isinstance(descriptor, int):
        descriptor = data.columns[int(descriptor)]

    return data

def strip(data, evalColumn):
    data_clean = data[pd.notnull(data[descriptor])]
    templist = []
    loopvariable = data_clean.genres

    return [eval(y)[0][label]for y in data_clean[evalColumn]]


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
    
def Column_Load(useStr = False):
    result = ""
    # If the column was retrieved (Success)
    if Column_Load_Pass(useStr) == True:
        result += "Column_Load_Pass performs as expected. "
    else:
        result += "Column_Load_Pass does not perform as expected. "
        
    if Column_Load_Fail(useStr) == True:
        result += "Column_Load_Fail performs as expected. "
    else:
        result += "Column_Load_Fail does not perform as expected. "
        
    print(result)
        
        
def Column_Load_Pass(useStr):
    if useStr == True:
        # Load the test data
        testData = load("Data/baselineMovies.csv")
        df_moviesclean = testData[pd.notnull(testData.overview)]
        y_genres = strip(testData, "genres")

        return True if len(y_genres) == 13507 else False
    else:
        # Load the test data
        testData = load("Data/baselineMovies.csv", "name", 9)
        df_moviesclean = testData[pd.notnull(testData.overview)]
        y_genres = strip(testData, "genres")

        return True if len(y_genres) == 13507 else False
        
def Column_Load_Fail(useStr):
    if useStr == True:
        try:
            testData = load("Data/baselineMovies.csv", "non-existing label", "non-existing descriptor")
            df_moviesclean = testData[pd.notnull(testData.overview)]
            y_genres = strip(testData, "genres")
            return True
        except:
            return False
    else:
        try:
            testData = load("Data/baselineMovies.csv", 50, 55)
            df_moviesclean = testData[pd.notnull(testData.overview)]
            y_genres = strip(testData, "genres")
            return True
        except:
            return False
    
def Test_GridSearch():
    result = ""
    
    if GridSearch_Pass() == True:
        result += "GridSearch_Pass performs as expected. "
    else:
        result += "GridSearch_Pass does'nt perform as expected. "
        
    if GridSearch_Fail() == True:
        result += "GridSearch_Pass performs as expected. "
    else:
        result += "GridSearch_Fail doesn't perform as expected. "
    
    print(result)
    
def GridSearch_Pass():
    testData = load("Data/baselineMovies.csv")
    df_moviesclean = testData[pd.notnull(testData.overview)]
    y_genres = strip(testData, "genres")
    X_train, X_test, y_train, y_test = train_test_split(df_moviesclean.overview, y_genres, test_size=0.2, random_state = 0)
    
    text_pipe = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),])

    grid_params ={
        'vect__stop_words': ('english', None),
        'vect__strip_accents': ('ascii', 'unicode', None),
        'tfidf__use_idf': (True, False),
        'tfidf__smooth_idf': (True, False),
        'tfidf__sublinear_tf': (True, False),
        'tfidf__norm': ('l1', 'l2', None),
        }

    search = GridSearchCV(text_pipe, grid_params)
    search.fit(X_train, y_train)

    predict_text = ["April 6th, 1917. As a regiment assembles to wage war deep in enemy territory, two soldiers are assigned to race against time and deliver a message that will stop 1,600 men from walking straight into a deadly trap."]

    return search.predict(predict_text)[0] == "Action"

def GridSearch_Fail():
    try:
        testData = load("Data/baselineMovies.csv")
        df_moviesclean = testData[pd.notnull(testData.overview)]
        y_genres = strip(testData, "genres")
        X_train, X_test, y_train, y_test = train_test_split(df_moviesclean.overview, y_genres, test_size=0.2, random_state = 0)

        text_pipe = Pipeline([
            ('vect', CountVectorizer()),
            ('tidf', TfidfTransformer()),
            ('clf', MultinomialNB()),])

        grid_params ={
            'vect__stop_words': ('english', None),
            'vect__strip_accents': ('ascii', 'unicode', None),
            'tfidf_use_idf': (True, False),
            'tfidf__smooth_idf': (True, False),
            'tfidf__sublinear_tf': (True, False),
            'tfidf__norm': ('l1', 'l2', None),
            }

        search = GridSearchCV(text_pipe, grid_params)
        search.fit(X_train, y_train)
        return True
    except:
        return False

def Test_Predict():
    result = ""
    if Predict_Pass() == True:
        result += "Predict_Pass performs as expected. " 
    else:
        result += "Predict_Pass doesn't perform as expected. "
        
    if Predict_Test() == True:
        result += "Predict_Test performs as expected. "
    else:
        result += "Predict_Test doesn't perform as expected. "
    
    if Predict_Fail() == True:
        result += "Predict_Fail performs as expected. "
    else:
        result += "Predict_Fail doesn't perform as expected. "

    print(result)


def Predict_Pass():
    testData = load("Data/baselineMovies.csv")
    df_moviesclean = testData[pd.notnull(testData.overview)]
    y_genres = strip(testData, "genres")
    X_train, X_test, y_train, y_test = train_test_split(df_moviesclean.overview, y_genres, test_size=0.2, random_state = 0)
    
    text_pipe = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),])

    grid_params ={
        'vect__stop_words': ('english', None),
        'vect__strip_accents': ('ascii', 'unicode', None),
        'tfidf__use_idf': (True, False),
        'tfidf__smooth_idf': (True, False),
        'tfidf__sublinear_tf': (True, False),
        'tfidf__norm': ('l1', 'l2', None),
        }

    search = GridSearchCV(text_pipe, grid_params)
    search.fit(X_train, y_train)
    predict_text = ["Two astronauts work together to survive after an accident leaves them stranded in space."]

    return search.predict(predict_text)[0] == "Science Fiction"
    
    
def Predict_Test():
    testData = load("Data/baselineMovies.csv")
    df_moviesclean = testData[pd.notnull(testData.overview)]
    y_genres = strip(testData, "genres")
    X_train, X_test, y_train, y_test = train_test_split(df_moviesclean.overview, y_genres, test_size=0.2, random_state = 0)
    
    text_pipe = Pipeline([
        ('vect', CountVectorizer()),
        ('tfidf', TfidfTransformer()),
        ('clf', MultinomialNB()),])

    grid_params ={
        'vect__stop_words': ('english', None),
        'vect__strip_accents': ('ascii', 'unicode', None),
        'tfidf__use_idf': (True, False),
        'tfidf__smooth_idf': (True, False),
        'tfidf__sublinear_tf': (True, False),
        'tfidf__norm': ('l1', 'l2', None),
        }

    search = GridSearchCV(text_pipe, grid_params)
    search.fit(X_train, y_train)
    
    predict_text = ["April 6th, 1917. As a regiment assembles to wage war deep in enemy territory, two soldiers are assigned to race against time and deliver a message that will stop 1,600 men from walking straight into a deadly trap."]

    return search.predict(predict_text)[0] == "Action"
    
    
def Predict_Fail():
    try:
        testData = load("Data/baselineMovies.csv")
        df_moviesclean = testData[pd.notnull(testData.overview)]
        y_genres = strip(testData, "genres")
        X_train, X_test, y_train, y_test = train_test_split(df_moviesclean.overview, y_genres, test_size=0.2, random_state = 0)

        text_pipe = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf', MultinomialNB()),])

        grid_params ={
            'vect__stop_words': ('english', None),
            'vect__strip_accents': ('ascii', 'unicode', None),
            'tfidf__use_idf': (True, False),
            'tfidf__smooth_idf': (True, False),
            'tfidf__sublinear_tf': (True, False),
            'tfidf__norm': ('l1', 'l2', None),
            }

        search = GridSearchCV(text_pipe, grid_params)
        search.fit(X_train, y_train)

        predict_text = ["Chloroxylenol is the active ingredient in Dettol. It comprises 4.8% of Dettol's total admixture, with the rest made up by pine oil, isopropanol, castor oil, soap and water."]
        return True    
    except:
        return False
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    