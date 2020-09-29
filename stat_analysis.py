"""
Edited on Sun September 28 9:58:33 2020

@author: sklucioni

Statistical Analysis Tool.
"""
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np

STOPWORDS = set(stopwords.words('english'))

# Source: https://stackoverflow.com/questions/42658252/how-to-create-a-qq-plot-between-two-samples-of-different-size-in-python
def qqplot(data1, data2, data_sorted_flag=False):
    """
    Compare the distributions of `data1` and `data2` through a Q-Q plot. If the
        distributions are equal, the Q-Q plot follows the line y = x.
    :param data1, List of values to compare to `data2`
    :param data2, List of values to compare to `data1`
    :param data_sorted_flag (optional), Whether or not the data is already
        sorted

    Prints a Q-Q plot and the Pearson correlation coefficient.
    """
    plt.figure(figsize=(12, 7))

    if not data_sorted_flag:
        data1 = sorted(data1)
        data2 = sorted(data2)

    sorted_len_data_pairs = sorted([(len(data1), data1), (len(data2), data2)])
    # Calculate the quantile levels
    quantile_levels_smaller = np.arange(sorted_len_data_pairs[0][0],dtype=float) / sorted_len_data_pairs[0][0]
    quantile_levels_larger = np.arange(sorted_len_data_pairs[1][0],dtype=float) / sorted_len_data_pairs[1][0]

    # Find the quantiles of the larger dataset by linear interpolation
    quantiles_larger = np.interp(quantile_levels_smaller, quantile_levels_larger, sorted_len_data_pairs[1][1])

    # Plot the quantiles
    plt.scatter(quantiles_larger, sorted_len_data_pairs[0][1])

    # Add a reference line
    max_val = max(data1[-1], data2[-1])
    min_val = min(data1[0], data2[0])
    plt.plot([min_val, max_val], [min_val, max_val], 'k-', color='red')

    plt.show()

    print("Pearson correlation coeff: ", pearsonr(quantiles_larger, sorted_len_data_pairs[0][1])[0])


def get_stopword_trackers(obj_lst):
    '''
    Finds the number of tweets, the number of stopwords per tweet, the
        proportion of stopwords per tweet, and the wordcount per tweet.
    :param obj_lst, A list of thinned tweet objects.

    :return n_obs, stopwords_tracker, stopwords_prop_tracker, wordcount_tracker
    '''
    n_obs = 0

    # number of stopwords per tweet
    stopwords_tracker = []
    # avg proportion of stopwords per tweet
    stopwords_prop_tracker = []
    wordcount_tracker = []
    for thin_obj in obj_lst:
        n_obs += 1
        if thin_obj.is_retweet:
            # Reassign the thin_obj so that we look at the retweet's text
            thin_obj = thin_obj.retweet

        word_tokens = word_tokenize(thin_obj.text)
        stopword_count = 0
        for w in word_tokens:
            w = w.lower()
            if w in STOPWORDS:
                stopword_count += 1
        stopwords_tracker.append(stopword_count)
        num_words = len(word_tokens)

        stopwords_prop_tracker.append(stopword_count / num_words if num_words else 0)
        wordcount_tracker.append(num_words)

    return n_obs, stopwords_tracker, stopwords_prop_tracker, wordcount_tracker


def print_qqplots_from_obj_lst(obj_lst1, obj_lst2):
    '''
    Prints three relevant Q-Q plots from `obj_lst1` compared to `obj_lst2`.
    :param obj_lst1, A list of thinned tweet objects.
    :param obj_lst2, A second list of thinned tweet objects.
    '''
    n_obs1, stopwords_tracker1, stopwords_prop_tracker1, wordcount_tracker1 = get_stopword_trackers(obj_lst1)
    n_obs2, stopwords_tracker2, stopwords_prop_tracker2, wordcount_tracker2 = get_stopword_trackers(obj_lst2)

    print_qqplots_from_trackers(stopwords_tracker1, stopwords_prop_tracker1, wordcount_tracker1, stopwords_prop_tracker2, stopwords_prop2, wordcount_tracker2)


def print_qqplots_from_trackers(stopwords1, stopwords_prop1, wordcount1, stopwords2, stopwords_prop2, wordcount2):
    '''
    Prints three relevant Q-Q plots from data calculated from the thinned tweet
        obj list.
    :param stopwords1, A list of stopwords per tweet.
    :param stopwords_prop1, A list of proportions of stopwords per tweet.
    :param wordcount1, A list of wordcount per tweet.
    :param stopwords2, A list of stopwords per tweet.
    :param stopwords_prop2, A list of proportions of stopwords per tweet.
    :param wordcount2, A list of wordcount per tweet.
    '''
    print(f"Stopwords QQ-Plot")
    qqplot(stopwords1, stopwords2)

    print(f"\nStopword Proportion QQ-Plot")
    qqplot(stopwords_prop1, stopwords_prop2)

    print(f"\nWordcount QQ-Plot")
    qqplot(wordcount1, wordcount2)
