#!/usr/bin/env python

"""
A script for fetching a user's twitter followers and following their
existance.
"""

from __future__ import print_function

import sys
import time

import twitter

import tw_sqlite

from local_settings import *

_DEBUG = False

__author__ = "Markus Koskinen"
__license__ = "BSD"

def syntax(execname):
    print("Syntax: %s" % execname)
    sys.exit(1)

def auth():
    api = twitter.Api(consumer_key = CONSUMER_KEY,
              consumer_secret = CONSUMER_SECRET,
              access_token_key = ACCESS_TOKEN_KEY,
              access_token_secret = ACCESS_TOKEN_SECRET)

    try:
        creds = api.VerifyCredentials()
        if _DEBUG:
            print("%s" % creds)
    except Exception as e:
        print("Authentication error: %s" % e)
        exit(1)
    else:
        return api

def fetch_followers(api):
    success = False

    # Note: python-twitter's GetFollowerIDs self-throttles pages
    while not success:
        try:
            followers = api.GetFollowerIDs(screen_name=USER_NAME, stringify_ids=False)
        except Exception as e:
            print("Rate limited. Sleeping 60s. (%s)" % e);
            time.sleep(60)
        else:
            success = True;
    return followers

def main():
    api = auth()

    followers = fetch_followers(api)

    print("Result: %s" % followers)
    print("Result count: %d" % len(followers))

    db = tw_sqlite.TwDB('twdb.db')
    print("Current sighting count: %d" % db.query_sighting_count())
    rows_affected = db.add_sightings(followers)
    print("Added sightings (rows affected): %d" % rows_affected)
    return

if __name__ == "__main__":
   if len(sys.argv) != 1:
      syntax(sys.argv[0])

   main()
