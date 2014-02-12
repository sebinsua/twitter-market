#!/usr/bin/python

import json, pprint
from twitter import Twitter, OAuth, TwitterHTTPError

import operator

class SpriggTwitter(object):

    def __init__(self, config_path='config.json'):
        config = self.load_config(config_path)
        self.client = Twitter(
            auth=OAuth(config['OAUTH_TOKEN'], config['OAUTH_SECRET'],
                       config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
        )

    def load_config(self, file_name):
        with open(file_name) as config_string:
            config = json.load(config_string)
            return config

    def get_current_account(self):
        # What's my own account information?
        account_details = self.client.account.verify_credentials()
        return account_details

    def get_following(self, screen_name=None):
        # Who am I following?
        # https://dev.twitter.com/docs/api/1.1/get/friends/list
        friends_list_api_call = self.client.friends.list
        friends = [f for f in self.get_all(friends_list_api_call, kwargs)]

        return self._sort_by_friends_count(friends)

    def get_followers(self):
        # Who are my followers?
        # https://dev.twitter.com/docs/api/1.1/get/followers/list
        followers_list_api_call = self.client.followers.list
        followers = [f for f in self.get_all(followers_list_api_call)]

        return self._sort_by_friends_count(followers)

    def get_all(self, api_call, extra_http_arguments={}, response_key='users'):
        current_cursor = -1
        next_cursor_is_not_zero = True
        while next_cursor_is_not_zero:
            http_arguments = {
                'skip_status': False,
                'cursor': current_cursor,
                'count': 200
            }
            http_arguments.update(extra_http_arguments)

            _next_list = api_call(**http_arguments)
            current_cursor = _next_list['next_cursor']
            next_cursor_is_not_zero = current_cursor is not 0
            for f in _next_list[response_key]:
                yield f

    def _sort_by_friends_count(self, tweeters):
        return sorted(tweeters, key=lambda d: d.get('friends_count'))

def get_current_easy_to_influence_followers(t):
    # Compute: People already in your twitter followers list who follow a large quantity of people that follow you.
    my_followers = t.get_followers()
    influenceable = []
    for follower in my_followers:
        # 1. get their following list.
        follower_is_following = t.get_following(follower['screen_name'])
        # @todo: The internet is too slow here to see if this is even working...
        # print follower_is_following
        # 2. count how many of the my_followers list appear in their following list.
        # intersect two lists of dictionaries where a dict key-value is the same.
        pass
    return influenceable

def _get_intersection_of_tweeters(a, b):
    tweeters_intersection = []
    pass

def get_prospects_that_follow_current_influencable_followers(t):
    # Compute: People not already in your twitter followers list who follow your easiest to influence followers.
    pass

def generate_table():
    # Calculate useful information on their account.
    # @todo: https://github.com/kennethreitz/clint
    # @todo: And pandas to print the tables.
    pass

if __name__ == "__main__":
    t = SpriggTwitter()

    current_account = t.get_current_account()
    print "Account: " + current_account['screen_name']
    print "Description: " + current_account['description']

    people_likely_to_be_easier_to_influence = get_current_easy_to_influence_followers(t)
    # prospects_connected_to_your_followers = get_prospects_that_follow_current_influencable_followers(t)


