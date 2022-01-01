import pandas as pd
import matplotlib.pyplot as plt

def test_run():
    """Function called by Test Run."""
	# http://pandas.pydata.org/pandas-docs/stable/generated/pandas.read_csv.html
    df = pd.read_csv("data/AAPL.csv") # optional args include delimiter, header, names, etc
	print df # prints all rows
	
	# http://pandas.pydata.org/pandas-docs/stable/api.html#dataframe
	print df.head() # prints first 5 rows
	print df.head(10) # prints first 10 rows
	print df.tail() # prints last 5 rows
	print df[10:21] # 10 to 20
	print df["Close"].max()
    print df["Volume"].mean()
	
	df["High"].plot()
	plt.show()
	
	df[["Close", "Adj Close"]].plot()
	plt.show()

if __name__ == "__main__":
    test_run()
