import methods as mt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import GridSearchCV
import os.path

def Data_Loading_Pass():
    testData = mt.load("Data/baselineMovies.csv")
    actualData = pd.read_csv("Data/baselineMovies.csv")
