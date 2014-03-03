#!/usr/bin/python

import json, pprint
from twitter import Twitter, OAuth, TwitterHTTPError

import operator

# @todo: Find some way of handling the stupid number of twitter API requests
#        that I want to make.
#        What's the progress of them? Can I log: "Part 1: prospect (count: 1/N)"

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
    MIN_TWEETERS = 1

    # Compute: People already in your twitter followers list who follow a large quantity of people that follow you.
    my_followers = t.get_followers()
    influenceable = []
    for follower in my_followers:
        follower_name = follower['screen_name']
        # 1. get their following list.
        follower_is_following = t.get_following(follower_name)

        # 2. count how many of the my_followers list appear in their following list.
        # intersect two lists of dictionaries where a dict key-value is the same.
        intersected_tweeters = _get_intersection_of_tweeters(my_followers, follower_is_following)
        if len(intersected_tweeters) > MIN_TWEETERS:
            influencee = {
              "follower_name": follower_name,
              "intersected": [tweeter['screen_name'] for tweeter in intersected_tweeters]
            }
            influenceable.append(influencee)

    return influenceable

def _get_intersection_of_tweeters(a, b):
    tweeters_intersection = []
    # @todo: not pythonic at all!
    for tweeter_a in a:
      for tweeter_b in b:
        if tweeter_a['screen_name'] == tweeter_b['screen_name']:
          tweeters_intersection.append(tweeter_b)
    return tweeters_intersection

def get_prospects_that_follow_current_influencable_followers(t):
    MIN_TWEETERS = 1
    # Compute: People not already in your twitter followers list who follow your easiest to influence followers.

    my_followers = t.get_followers()
    influenceable = []
    for follower in my_followers:
        follower_name = follower['screen_name']

        # 1. get their followers list.
        followers_of_follower = t.get_followers(follower_name)

        for prospect in followers_of_follower:
          prospect_name = prospect['screen_name']

          # 2. get who they already follow.
          prospect_is_following = t.get_following(prospect_name)

          # 3. count how many of the my_followers list appear in the prospects following list.
          # intersect two lists of dictionaries where a dict key-value is the same.
          intersected_tweeters = _get_intersection_of_tweeters(my_followers, prospect_is_following)
          if len(intersected_tweeters) > MIN_TWEETERS:
              influencee = {
                "follower_name": prospect_name,
                "intersected": [tweeter['screen_name'] for tweeter in intersected_tweeters]
              }
              influenceable.append(influencee)

    return influenceable

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
    print people_likely_to_be_easier_to_influence

    prospects_connected_to_your_followers = get_prospects_that_follow_current_influencable_followers(t)
    print prospects_connected_to_your_followers

    # Get some backing: https://github.com/coleifer/peewee
