# imports main dataset and adds "Date" and "Year" columns

import pandas as pd
'''
df = pd.read_csv('tweetsLGBT.csv')
df["Date"] = df.apply(lambda x: x["create_at"].split("T")[0], axis=1)
df["Year"] = df.apply(lambda x: x["create_at"].split("-")[0], axis=1)
#print(df)
#df2 = df.groupby('Date').count().sort_values(by = ["Date"], ascending=True)
df = df.dropna()

# subsets the dataframe into 50 tweets from each day, and write to file
df2 = df.groupby('Date').apply(lambda x: x.sample(n = min(50, x.shape[0]), random_state = 170).reset_index(drop=True))
#df2.to_csv("sampled_tweets.csv")
'''


hatecrimesdf = pd.read_csv("hate_crime.csv")
lgbt = ["Anti-Bisexual", "Anti-Gay (Male)","Anti-Heterosexual","Anti-Lesbian",
        "Anti-Lesbian, Gay, Bisexual, or Transgender (Mixed Group)", "Anti-Transgender",
        "Anti-Gender Non-Conforming"]
years = [2015, 2016, 2017, 2018, 2019]

lgbt_crimes = hatecrimesdf[hatecrimesdf['data_year'].isin(years)]
lgbt_crimes2 = lgbt_crimes[lgbt_crimes['bias_desc'].isin(lgbt)]

#lgbt_crimes.to_csv("lgbt_crimes.csv")
#lgbt_crimes2.to_csv("lgbt_crimes2.csv")





#df3 = df.groupby('Year').apply(lambda x: x.sample(n = min(400, x.shape[0])).reset_index(drop=True))
#df3.to_csv("bot_training.csv")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
