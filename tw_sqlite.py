#!/usr/bin/env python

""" Database handling object for twit_follower. """

from __future__ import print_function
from builtins import input

import os.path
import sys

import sqlite3

__author__ = "Markus Koskinen"
__license__ = "BSD"

class TwDB:
    conn = None
    c = None

    def __init__(self, db_file):
        self.connect(db_file)
        self.create_tables()

    def create_tables(self):
        sql_t1 = "CREATE TABLE IF NOT EXISTS tw_users(" \
                "user_id INTEGER PRIMARY KEY, " \
                "user_name TEXT);\n"

        sql_t2 = "CREATE TABLE IF NOT EXISTS tw_user_sighting(" \
                "id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                "user_id INT, " \
                "sighting_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
        self.c.execute(sql_t1)
        self.c.execute(sql_t2)
        self.conn.commit()

    def connect(self, db_file):
        if not os.path.isfile(db_file):
            create_new_db = input("Can't find your DB '%s', create a new one [Y/n]:" % db_file)
            if create_new_db.lower() not in ('y', '', 'yes'):
                print("OK. Exiting.")
                sys.exit(1)

        self.conn = sqlite3.connect(db_file)
        self.c = self.conn.cursor()

    def query_sighting_count(self):
        self.c.execute("SELECT COUNT(*) FROM tw_user_sighting")
        self.conn.commit()
        return self.c.fetchone()

    def add_sightings(self, twitter_ids):
        """ Add a list of twitter_ids to tw_user_sighting table. """
        if twitter_ids in (None, []):
            return 0

        self.c.executemany("""
                INSERT INTO tw_user_sighting('user_id') VALUES (?)
                """, zip(twitter_ids))
        self.conn.commit()
        return self.c.rowcount
