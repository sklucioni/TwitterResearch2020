**Memo lucioni-200916.md**

This memo takes another look at the statistical analysis of our data and proposes two new methods to determine statistical similarity.

# Background

After putting more thought into the original statistical analysis of our data, I realized that the t-test is not the best choice for a few reasons. First, I used the t-test to compare two different proportions (e.g. %retweets, %quotes, %replies). This forced me to create nonsensical groupings throughout a day of data in order to have data points to compare. However, this is inherently flawed because I was looking at proportions, and therefore, I should have used a 2-sample proportion z-test. While applying this z-test to the appropriate proportions, I further questioned whether the 2-sample proportion z-test was a good choice. So I looked into hypothesis testing (especially with big data), how to determine dataset similarity, and what was used to determine the reliability of the 1% Twitter stream.

In this section, I will touch more on the current flaws in our analysis, the challenges that our data present, and what research has been done in the field of dataset comparison. First, let's define some terminology and outline the problem.

## Terminology

### What does our data look like?
One "dataset" is a day's worth of Tweets that are collected with a filtering scheme (solely based on handles *right now* - we might decide to add some hashtags as well). Each tweet object has been thinned to reduce the data size. We keep relevant fields (look at `thinned_tweet_obj.py` to see what we keep).

Currently, we have three "varieties" of datasets. They are all collected with the same filtering scheme, but they have various random sleeps implemented in order to throttle the daily sample size. We will name these three varieties as follows:
1. **Large**
  - No sleep implemented
  - About 1% of Twitter's daily stream (roughly 5 million tweets)
  - Days: 06/24
2. **Small**
  - 1 minute - 1 hour sleep
  - About 0.06% of Twitter's daily stream (roughly 300,000 tweets)
    - About 6% of the **large** sample size
  - Days: 08/26 - present
3. **Micro**
  - 1 minute - 2 hours sleep
  - About 0.03% of Twitter's daily stream (roughly 150,000 tweets)
  - Days: 06/26 - 08/25

### What's the goal?
We want to examine whether or not the **small** and **micro** datasets are statistically similar to the **large** dataset. Due to prior research (see *Brief Literature Review* section), we conclude that the 1% stream (our **large** dataset) is representative (statistically similar) of the full, 100% daily Twitter stream. Now, we want to see if our *even smaller* datasets are also representative.

Theoretically, since we are taking a simple random sample of data, the **small** and **micro** datasets should be representative of the 1% Twitter stream (and therefore, the 100% stream). This statistical analysis aims to confirm this hypothesis.

## Flaws in Original Analysis and Challenges

**tl;dr:** Original statistical analysis applied the wrong test for proportions. Since we have such a large sample size, we should reduce our choice for ![alpha](https://latex.codecogs.com/svg.latex?%5Calpha). We expect to see a fluctuation in amount of retweets/replies/quotes from day to day because that shows how users are interacting and reacting to current events.

In my original statistical analysis of the data, I used a 2 sample t-test to compare two groups. While this is a good idea for quantitative variables, I was also using the t-test to compare qualitative variables. So the first flaw is *using the wrong test*. Instead, I should have used a 2 sample proportions z-test which is used to compare proportions. However, even considering and applying the z-test raises some other issues.

First, with such a large sample size, we should really restrict our Type I error rate (![alpha](https://latex.codecogs.com/svg.latex?%5Calpha)) to less than the typical 0.05. We could probably reduce ![alpha](https://latex.codecogs.com/svg.latex?%5Calpha) to 0.00001 or even smaller. Otherwise, our hypothesis test will not be meaningful or useful. Furthermore, these hypothesis tests can only tell us if we find a statistical difference (which would be the case if we reject the null that the population statistics are the same). If we don't reject the null, we cannot go and "accept" the null. The power in hypothesis testing comes from rejecting the null. Otherwise, our test doesn't really produce meaningful results.

Even disregarding these considerations, our tests resulted in rejections of the null. If we think about our data and what we are comparing, these rejections make sense! We are comparing data from ![day i](https://latex.codecogs.com/svg.latex?%5Ctext%7Bday%7D_i) to ![day j](https://latex.codecogs.com/svg.latex?%5Ctext%7Bday%7D_j) where i != j. The quantities that we are comparing are proportion of retweets, replies, and quotes. These values judge how people interact and react to what is going on in the world (which is why we want to use them to determine sentiment!), and what is going on in the world changes *daily* so it makes sense that these values would be different from day to day. Therefore, we would either want to create a summary statistic averaging across a number of days OR compare a different stat that we don't expect to change daily OR compare the different sample sizes for the *same day*. With the data that we have, the most straight forward approach is comparing a different statistic that we don't expect to change daily.

I also looked into applying a chi-squared for homogeneity which can be used to test if the frequency counts of one categorical variable is distributed identically across two or more different populations. I think this is an okay choice because we are looking at different populations and we are testing for identical distribution. Yet, the problem still arises with the Type I error rate and the fact that we expect certain values to fluctuate from day to day.

Overall, this pointed me to look into new methods for determining similarity between datasets.

## Brief Literature Review

In Andrew's thesis, he referenced [Kalev Leetaru's article](https://www.forbes.com/sites/kalevleetaru/2019/02/27/is-twitters-spritzer-stream-really-a-nearly-perfect-1-sample-of-its-firehose/#27e2cf715401) on examining the similarity between the 100% and 1% Twitter streams. Leetaru doesn't explicitly outline his methods, but he gives a general overview and concludes that the 1% sample is a fairly accurate representation of the full 100% stream.

Leetaru takes each day as a data point in the range of January 2012 - October 2018. He compares the number of the appearance of 3 keywords/topics. He looks at one common topic that should appear often ("climate change"), a second medium/small topic ("global warming"), and a final micro topic ("IPCC"). He then tests to see if a positive correlation exists between the number of keyword mentions in the 1% sample to the 100% stream (there should be a strong, positive correlation if the 1% sample is representative). He finds that all three topics have strong, positive correlations. Unsurprisingly, the micro topic does not have as strong a correlation as the common and small topics.

It makes sense to mimic Leetaru's analysis, but we do not have as much data as he does (three different sized samples for every day). From this analysis, we can assume that our one day of 1% sampling is representative of the full stream (in other words, the 1% sample is representative of a true day on Twitter). We want to know if our small and micro samples is representative of the 1% (which we can then carry over to say is representative of a full day). (The conclusion that the 1% sample is representative of the population will be useful in a Bootstrap application.)

# New Methods to Compare Data Distributions

After thinking through the flaws and variety of approaches, I propose the following two statistical analyses.

## Q-Q Plot and Pearson's R (Quantitative Variables)

A Quantile-Quantile Plot ([Q-Q Plot](https://en.wikipedia.org/wiki/Q–Q_plot)) is a graphical method to compare two distributions. To form the Q-Q plot, we plot the quantiles from each sample against one another. If the sample sizes are not equal, then we linearly interpolate the values so that we have an equal amount of quantiles. (Basically, we sort the data in each sample from smallest to largest and plot new data points where the ![x i](https://latex.codecogs.com/svg.latex?x_i)'s are from one sample and the ![y i](https://latex.codecogs.com/svg.latex?y_i)'s are from the other sample.) If the distributions are equal, the Q-Q plot follows the line y = x.

**How can we use this?**

For each of the quantitative measures (such as avg. tweet wordcount, avg. number of stopwords/tweet, avg. number of Biden/Trump keywords/tweet), we can construct a Q-Q plot between the different samples. Then, we can interpret the graph and look at the correlation coefficient (how close it is to 1).

If we look at the distribution of these metrics between the large, small, and micro datasets (e.g. through a boxplot), we notice that they look pretty similar, so we expect to find pretty linear Q-Q plots. This would be good news and we could conclude similarity!

This is a similar approach to Leetaru's correlation test, but modified for the data we have. I think this is a solid choice to test our data similarity.

## Bootstrap and Pearson's R (Qualitative / Categorical Variables)

Since proportion tests and hypothesis tests in general are very sensitive to our large data, I think we should stay away from conclusions based on hypothesis tests. I also think this approach is less legitimate in comparison to the Q-Q plot, and I think we should mainly use the Q-Q plot analysis. However, I will lay out my idea for testing the qualitative variables.

Leetaru's analysis looks at three data points a day (number of appearances of his large, small, and micro keywords) and compares them all over the course of 6 years. In order to mimic this range of data, we can construct our own data through resampling. I propose creating x > 30 bootstrapped samples *per* large, small, and micro datasets for each day of data that we have. So for one day of data, we would draw 3x bootstrapped samples of size n_large, n_small, and n_micro and calculate the desired proportions for each sample. Let each of the x proportions make up a sample called "sample_[large/small/micro]_[day]". After doing this for all *D* days, join all of the samples into "sample_[large/small/micro]". We can now plot samples_small vs. samples_large and samples_micro vs. samples_large. Then, we will calculate the correlation coefficient. If it is close to 1, we can conclude that there is a positive correlation between the two compared sizes. If the correlation coefficient is close to 1, we can conclude that the datasets are similar.

I am hesitant to use this method because we are basically constructing our data so that it is correlated. Also, bootstrap samples are typically equal to the original sample size or smaller. It is not usually larger so we would have to be suspicious of our conclusions.

# Conclusion

In order to conclude that our data is representative of the larger sample, we will look at Q-Q plots comparing the distribution of the following quantitative variables:
- tweet **wordcount**
- number of **stopwords** per tweet
- **proportion of stopwords** per tweet
- number of **political** related words per tweet
  - words such as "Biden", "Trump", and campaign related words.

I will run this analysis on the data we have collected thus far as well as create a Q-Q plot analysis tool.
