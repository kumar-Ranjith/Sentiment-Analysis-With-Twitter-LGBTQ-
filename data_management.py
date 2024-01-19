import pandas as pd
tweets = pd.read_csv('scored_tweets_vectorization.csv', lineterminator='\n')
crimes = pd.read_csv('lgbt_crimes.csv')
#crimes_per_day = pd.read_csv("hate_crimes_per_day.csv")
#crimes_per_month = pd.read_csv("crimes_per_month.csv")

tweets.dropna(inplace = True)

# find the month of each date
tweets['year-month'] = tweets.apply(lambda x: x["Date"].split("-")[0] +"-" +
                                              x["Date"].split("-")[1], axis=1)
crimes['year-month'] = crimes.apply(lambda x: x["incident_date"].split("-")[0] +"-" +
                                              x["incident_date"].split("-")[1], axis=1)

# These Lines calculate the amount of crimes per day and per month, respectively
crimes_per_day = crimes.groupby(['incident_date'])['incident_date'].count()
crimes_per_month = crimes.groupby(['year-month'])['year-month'].count()
# confession: I renamed the "count columns to "n" maanually in the csv file since
# I couldn't figure how to do it in pandas

# saves as csv files fpr later
#crimes_per_month.to_csv("crimes_per_month.csv")
#crimes_per_day.to_csv("hate_crimes_per_day.csv")

def get_num_crimes_day(date):
    if (crimes_per_day['incident_date'] == date).any():
        return crimes_per_day.loc[crimes_per_day['incident_date'] == date, "n"].iloc[0]
    else:
        return None

def get_num_crimes_month(month):
    if (crimes_per_month['year-month'] == month).any():
        return crimes_per_month.loc[crimes_per_month['year-month'] == month, "n"].iloc[0]
    else:
        return None

# combine tweets and crime per month tables
#tweets["num_crimes_per_month"] = tweets["year-month"].apply(get_num_crimes_month)
#tweets.to_csv("tweets_num_crimes_per_month.csv")

# combine tweets and crimes per day tables
#tweets["num_crimes_per_day"] = tweets["Date"].apply(get_num_crimes_day)
#tweets.to_csv("tweets_num_crimes.csv")



