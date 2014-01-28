#!/usr/bin/python
# Do:
# Compute: People in your twitter followers list who follow large quantity of people that follow you: X
# Compute: People in your twitter followers list that are followed by people that follow your current followers but not yourself: Y.
# Compute: People not in your twitter followers list who follow a large quantity of people that follow you: Z.
# For each of these calculate useful information on their account.

import json, pprint
from twitter import Twitter, OAuth, TwitterHTTPError

def load_config(file_name):
    with open(file_name) as config_string:
        config = json.load(config_string)
    return config

def get_following(t):
    # Who am I following?
    # https://dev.twitter.com/docs/api/1.1/get/friends/list
    following, current_cursor = [], -1
    next_cursor_is_not_zero = True
    while next_cursor_is_not_zero:
        _next_following = t.friends.list(skip_status=False, cursor=current_cursor, count=200)
        current_cursor = _next_following['next_cursor']
        next_cursor_is_not_zero = current_cursor is not 0
        following.extend(_next_following['users'])

    return sorted([(f['screen_name'], f['friends_count']) for f in following], key=lambda f: f[1])

def get_followers(t):
    # Who are my followers?
    # https://dev.twitter.com/docs/api/1.1/get/followers/list
    followers, current_cursor = [], -1
    next_cursor_is_not_zero = True
    while next_cursor_is_not_zero:
        _next_followers = t.followers.list(skip_status=False, cursor=current_cursor, count=200)
        current_cursor = _next_followers['next_cursor']
        next_cursor_is_not_zero = current_cursor is not 0
        followers.extend(_next_followers['users'])

    return sorted([(f['screen_name'], f['friends_count']) for f in followers], key=lambda f: f[1])

if __name__ == "__main__":
    config = load_config('config.json')
    t = Twitter(
        auth=OAuth(config['OAUTH_TOKEN'], config['OAUTH_SECRET'],
                   config['CONSUMER_KEY'], config['CONSUMER_SECRET'])
    )
    print "following:"
    pprint.pprint(get_following(t))
    print "followers:"
    pprint.pprint(get_followers(t))
