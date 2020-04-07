def test(x = "The methods.py module has loaded successfully"):
    print(x)
    

#Method that returns the number of each unique catogory when a dataframe column is passed in    
def count_cats(dataframe_column):
    counts = dataframe_column.value_counts()
    return counts
    
