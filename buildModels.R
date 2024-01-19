library(ggplot2)
library(data.table)

scored = fread('tweets.csv', header=TRUE, select = c('Year', 'sentiment'))

##### Create bar plot for negative and positive tweet counts #####

aggScored = aggregate(x = scored$Year, by = list(scored$sentiment, scored$Year), FUN = length)

ggplot(data=aggScored_to2019, aes(x=Group.2, y=x, fill=Group.1)) +
  geom_bar(stat="identity", position=position_dodge(.75), width=0.7) +
  labs(title="Counts of Negative and Positive Tweets from 2015-2019",
       x ="Year", y = "Count", fill = "Sentiment") +
  theme(axis.text.x = element_text(size=12),
        axis.text.y = element_text(size = 12), axis.title=element_text(size=12,face="bold")) +
  scale_y_continuous(breaks = scales::pretty_breaks(n = 7))


##### Create linear regression model for hate crimes vs. negative and positive tweets #####

lm_model_data = fread('tweets.csv', header=TRUE, select = c('Year', 'geo_tag-stateName', 'sentiment'))

aggLM = aggregate(x = lm_model_data$Year, by = list(lm_model_data$`geo_tag-stateName`, lm_model_data$sentiment), FUN = length)
PosNegCrimes = aggLM[c(1:48),]

vec = PosNegCrimes$x
PosNegCrimes$negative = vec

PosNegCrimes = subset(PosNegCrimes, select = -c(Group.2, x))

PosNegLM = lm(hate_crimes ~ negative + positive, data=PosNegCrimes)
summary(PosNegLM)

