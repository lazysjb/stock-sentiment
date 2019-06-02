import json
import os
import pytz

import arrow
import GetOldTweets3 as got
import pandas as pd

from data_collect.config import TWEET_DATA_INGEST_DIRECTORY, TWEET_CASHTAG_LIST


TWEET_TAGS = [
    'author_id',
    'date',
    'favorites',
#     'formatted_date',
    'geo',
    'hashtags',
    'id',
    'mentions',
    'permalink',
    'replies',
    'retweets',
    'text',
    'to',
    'urls',
    'username'
]


def get_parsed_tweets_for_date(query,
                               date_str,
                               save=False,
                               save_dir=TWEET_DATA_INGEST_DIRECTORY):
    tweets = get_tweets_for_query_and_date(query, date_str)
    parsed_result = []

    for tweet in tweets:
        parsed_result.append(_parse_tweet_object(tweet))

    tweet_df = pd.DataFrame(parsed_result)

    if save:
        out_path = os.path.join(save_dir, 'tweets_{}_{}.json'.format(date_str, query))
        print('Saving output to {}'.format(out_path))
        with open(out_path, 'w') as f:
            json.dump(parsed_result, f, indent=4)

    return tweet_df


def get_tweets_for_query_and_date(query, date_str):
    next_date = arrow.get(date_str).shift(days=1).strftime('%Y-%m-%d')

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query) \
        .setSince(date_str) \
        .setUntil(next_date)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    return tweets


def _format_date_to_str(utc_datetime_object):
    utc_date_str = utc_datetime_object.strftime('%Y-%m-%d, %H:%M')
    est_date_str = utc_datetime_object.astimezone(
        pytz.timezone('US/Eastern')).strftime('%Y-%m-%d, %H:%M')

    return utc_date_str, est_date_str


def _parse_tweet_object(tweet_object):
    parsed = dict()

    for tag in TWEET_TAGS:
        tag_value = getattr(tweet_object, tag)

        if tag == 'date':
            utc_date, est_date = _format_date_to_str(tag_value)
            parsed['UTC_date'] = utc_date
            parsed['EST_date'] = est_date
        else:
            parsed[tag] = tag_value

    return parsed


def ingest_twitter_for_date(date_str,
                            query_list=TWEET_CASHTAG_LIST):
    for q in query_list:
        _ = get_parsed_tweets_for_date(q,
                                       date_str,
                                       save=True,
                                       save_dir=TWEET_DATA_INGEST_DIRECTORY)
    return
