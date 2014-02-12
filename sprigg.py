#!/usr/bin/python
# Do:
# Compute: People in your twitter followers list who follow large quantity of people that follow you: X
# Compute: People in your twitter followers list that are followed by people that follow your current followers but not yourself: Y.
# Compute: People not in your twitter followers list who follow a large quantity of people that follow you: Z.
# For each of these calculate useful information on their account.

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

    def get_following(self):
        # Who am I following?
        # https://dev.twitter.com/docs/api/1.1/get/friends/list
        friends_list_api_call = self.client.friends.list
        friends = [f for f in self.get_all(friends_list_api_call)]

        return self._sort_by_friends_count(friends)

    def get_followers(self):
        # Who are my followers?
        # https://dev.twitter.com/docs/api/1.1/get/followers/list
        followers_list_api_call = self.client.followers.list
        followers = [f for f in self.get_all(followers_list_api_call)]

        return self._sort_by_friends_count(followers)

    def get_all(self, api_call, response_key='users'):
        current_cursor = -1
        next_cursor_is_not_zero = True
        while next_cursor_is_not_zero:
            _next_list = api_call(skip_status=False, cursor=current_cursor, count=200)
            current_cursor = _next_list['next_cursor']
            next_cursor_is_not_zero = current_cursor is not 0
            for f in _next_list[response_key]:
                yield f

    def _sort_by_friends_count(self, tweeters):
        pprint.pprint(tweeters)
        return sorted(tweeters, key=lambda d: d.get('friends_count'))

if __name__ == "__main__":
    t = SpriggTwitter()
    print "followers:"
    pprint.pprint(t.get_followers())
