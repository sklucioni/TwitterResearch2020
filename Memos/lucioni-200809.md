**Memo lucioni-200809.md**

This memo corresponds with `PythonNotebooks/thinned_data_statistical_analysis.ipynb`.

*Thinned Data Statistical Analysis*

We started collecting about 20x fewer tweets in the middle of 06/25 in order to reduce file size and clumsiness. The original data only captures about 1% of Twitter traffic. We want to test and see if the reduced files are statistically different from the larger data set.

In order to do so, we have a few options for statistical tests. Two common tests that we want to run are:
1. **ANOVA Test** - Analysis of variance test. This test analyzes the difference between the means of more than two groups.
2. **Independent Samples t-test** - This test analyzes the difference between the population means of two groups.

The difference between tests exists in how we define a "group" of data. It makes sense to define two groups: full data vs. reduced data which suggests a t-test. However, we could create more groups for an ANOVA test by separating by day. Therefore, group 1 could be 06/24 full data, group 2 could be 06/26 reduced data, group 3 - 06/27 reduced data, etc.

We want to test a few dependent variables in order to really check for statistical difference. I propose the following set of dependent variables:
- ratio of tweets vs. (retweets, quotes, replies)
- ratio of retweets vs. (tweets, quotes, replies)
- ratio of quotes vs. (tweets, retweets, replies)
- ratio of replies vs. (tweets, retweets, quotes)
- ratio of common stop words vs. all other words
- ratio of selected keywords (Trump, Biden) vs. all other words ratio

Our thinned tweets do not include the tweet's timestamp. Therefore, I plan to split each day of data into data points by grouping by a certain size. Ideally I would like > 30 tweets in a chunk to assume normality by the Central Limit Theorem.

We can assume independent samples because our data will be examined from different days. Therefore, they will be different tweets. We also have a random sample due to how Twitter allows us to collect data.

For the t-test, our null and alternative hypotheses are as follows:
$$H_0 : \mu_1 = \mu_2$$
$$H_1 : \mu_1 \neq \mu_2$$
The null states that the population means are equal, and the alternative states that the population means are different.

*Constructing Subgroups*

First, we need to construct subgroups for each day of data. For now, we will construct approximately 1440 groups which correlates to about one group a minute. I don't think this is a satisfactory criteria because we do not have the timestamps for tweets. We should determine how to partition a day into meaningful subgroups.

**Note:** The analysis done in this section of the notebook uncovers an error with the `is_reply` field. It is always returning TRUE.

*Performing t-tests*

We run X t-tests in this section. First, we look at the ratio of different types of tweets. This includes: retweets, replies, and quotes. The replies t-test is not meaningful due to the `is_reply` field error. Otherwise, we can conclude that the ratio of retweets are not statistically different between the reduced and larger data (this is good!). We do reject the null for the ratio of quotes, instead, concluding that the ratio of quotes are statistically different between the reduced and larger data (this is not great, but remember that our subgrouping isn't chosen very wisely). When we re-run the t-test's with fewer subgroups, we find that with groups = 181, we can accept the null in all cases.

Now, let's look at the actual words in a tweet to determine if the data is statistically different. First, we will examine the ratio of stopwords. Stopwords are English words that occur frequently such as 'the,' 'and,' 'a,' etc. We would like to see a similar ratio of stopwords between the reduced and larger data because this can help us conclude that the actual tweets are statistically similar. We will also examine how many times a Trump or Biden related word appears as well as the ratio of tweets that mention Trump or Biden. While the number of times a Trump or Biden word may not be a great indicator of statistical similarity, the number of tweets that mention either candidate may be useful. This measure will allow us to glance at the virality of each candidate and will help us determine if the data that we wish to study about the tweets is statistically similar.

We can conclude that the ratio of stopwords are not statistically different between the reduced and larger data (this is good!). This may be a good metric to determine that the tweets themselves are not statistically different. However, notice that we reject the null for the ratio of times Trump related words appear and tweets that mention Trump, concluding that these are statistically different between the reduced and larger data. We also conclude that the ratio of times Biden related words appear and the ratio of tweets that mention Biden are statistically different between the reduced and larger data.
If we reduce the amount of groups (increasing the number of tweets per group), we do not reject the null and can then claim that the data is not statistically different. This raises a question on how we wish to determine subgroups. Specifically, with groups = 45, we can accept the null in all cases.

*Conclusion*

After performing several t-tests to compare the reduced and larger data sets of combined, thinned tweets, we can make several conclusions. First, we can accept the null hypothesis and conclude that the data sets are not statistically different for the ratio of retweets. We must reject this conclusion for the ratio of quotes. We cannot make any conclusion for the ratio of replies due to an error with the is_reply field. It would be worthwhile to rerun the t-tests with a more thoughtful choice for subgroups.

The ratio of stopwords are not statistically different between the reduced and larger data. This may be a good metric to determine that the tweets themselves are not statistically different since stopwords are common words between English statements.

However, using the current subgroup size of 1440, we reject the null for all other scenarios, concluding that the tweets are statistically different between the reduced and larger data. If we reduce the amount of groups (increasing the number of tweets per group), we do not reject the null and can then claim that the data is not statistically different. This raises a question on how we wish to determine subgroups.

It is a little surprisingly to see the lack of mentions to Trump and Biden. Even more so, Biden is mentioned 5x as frequently as Trump. This raises questions on how we can determine whether a tweet is about Trump or Biden. We should establish a robust criteria and re-run the above t-tests.

**Future considerations:**
- Determine a smarter criteria for subgroup size
- Establish a robust criteria to determine a Trump or Biden related tweet
- Model the retweet vs. reply vs. quote as a multinomial distribution
