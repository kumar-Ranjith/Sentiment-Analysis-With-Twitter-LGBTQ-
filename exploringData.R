library(ggplot2)
library(ggrepel)
library(data.table)
library(tidyverse)

crimes = fread('lgbtcrimes.csv', header=TRUE, select = c('data_year', 'state_name', 'bias_desc'))
keyword_tweets = fread('tweets.csv', header=TRUE)


crimes_2015 = crimes[crimes$data_year == 2015,]
crimes_2019 = crimes[crimes$data_year == 2019,]

##### Creating bubble plot for 2015 ##### 

count2015 = aggregate(x = crimes_2015$data_year, by = list(crimes_2015$bias_desc, crimes_2015$state_name), FUN = length)
count2015$Group.1[count2015$Group.1  == "Anti-Gay (Male)"] = 'gay'
count2015$Group.1[count2015$Group.1  == "Anti-Lesbian (Female)"] = 'lesbian'
count2015$Group.1[count2015$Group.1  == "Anti-Bisexual"] = 'bisexual'
count2015$Group.1[count2015$Group.1  == "Anti-Lesbian, Gay, Bisexual, or Transgender (Mixed Group)"] = 'lgbt'
count2015$Group.1[count2015$Group.1  == "Anti-Transgender"] = 'transgender'

ktweets_2015 = keyword_tweets[substr(keyword_tweets$create_at, 1, 4)  == 2015,]
ktweets_2015 = ktweets_2015[, c(3,5)]
KTcount2015 = aggregate(x = ktweets_2015$`geo_tag-stateName`, by = list(ktweets_2015$`geo_tag-stateName`, ktweets_2015$kword), FUN = length)

colnames(KTcount2015)[1] = 'state_name'
colnames(count2015)[2] = 'state_name'
colnames(KTcount2015)[2] = 'keyword'
colnames(count2015)[1] = 'keyword'

ktweet_merge_2015 = merge(KTcount2015,count2015,by=c('keyword', 'state_name'))
colnames(ktweet_merge_2015)[4] = 'num_crimes'
colnames(ktweet_merge_2015)[3] = 'num_tweets'

ktweet_merge_2015 %>% 
  ggplot(aes(x=reorder(state_name, num_tweets), y=keyword, size=num_tweets, color=num_crimes)) + 
  ggtitle("Frequency of Hate Crimes and Keyword Usage in 2015") +
  scale_size(range=c(2,12)) +
  geom_point() +
  xlab("U.S. State") +
  ylab("Tweet Keyword") +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1, size=12),
        axis.text.y = element_text(size = 12), axis.title=element_text(size=12,face="bold")) +
  labs(size="Number of tweets", colour="Number of crimes") +
  scale_color_gradientn(colours =c('#a51a49', '#00ccff', '#00bbb1',
                                   '#00cc00', '#bef0b0', '#ffff66',
                                   '#ff9900', '#ff0033', '#ff0033'))



##### Creating bubble plot for 2019 ##### 

count2019 = aggregate(x = crimes_2019$data_year, by = list(crimes_2019$bias_desc, crimes_2019$state_name), FUN = length)
count2019$Group.1[count2019$Group.1  == "Anti-Gay (Male)"] = 'gay'
count2019$Group.1[count2019$Group.1  == "Anti-Lesbian (Female)"] = 'lesbian'
count2019$Group.1[count2019$Group.1  == "Anti-Bisexual"] = 'bisexual'
count2019$Group.1[count2019$Group.1  == "Anti-Lesbian, Gay, Bisexual, or Transgender (Mixed Group)"] = 'lgbt'
count2019$Group.1[count2019$Group.1  == "Anti-Transgender"] = 'transgender'

ktweets_2019 = keyword_tweets[substr(keyword_tweets$create_at, 1, 4)  == 2019,]
ktweets_2019 = ktweets_2019[, c(3,5)]
KTcount2019 = aggregate(x = ktweets_2019$`geo_tag-stateName`, by = list(ktweets_2019$`geo_tag-stateName`, ktweets_2019$kword), FUN = length)

colnames(KTcount2019)[1] = 'state_name'
colnames(count2019)[2] = 'state_name'
colnames(KTcount2019)[2] = 'keyword'
colnames(count2019)[1] = 'keyword'

ktweet_merge_2019 = merge(KTcount2019,count2019,by=c('keyword', 'state_name'))
colnames(ktweet_merge_2019)[4] = 'num_crimes'
colnames(ktweet_merge_2019)[3] = 'num_tweets'

ktweet_merge_2019 %>% 
  ggplot(aes(x=reorder(state_name, num_tweets), y=keyword, size=num_tweets, color=num_crimes)) + 
  ggtitle("Frequency of Hate Crimes and Keyword Usage in 2019") +
  scale_size(range=c(2,12)) +
  geom_point() +
  xlab("U.S. State") +
  ylab("Tweet Keyword") +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1, size=12),
        axis.text.y = element_text(size = 12), axis.title=element_text(size=12,face="bold")) +
  labs(size="Number of tweets", colour="Number of crimes") +
  scale_color_gradientn(colours =c('#a51a49', '#00ccff', '#00bbb1',
                                   '#00cc00', '#bef0b0', '#ffff66',
                                   '#ff9900', '#ff0033', '#ff0033'))



