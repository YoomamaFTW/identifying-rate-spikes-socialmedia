"""
generator.py
Generates the user base, posts, tags, and posts connected to tags.
User base is demonstrated by logistics growth model
"""
from .database import Database
from .updater import update_rate
from math import e as eulers_num
from random import randint, random
from uuid import uuid4

db = Database.shared()
bc = -.000000002  # -.004 * 0.00000005


def generate_humans(max_pop):
    # Generates users logistically
    db.userCount = max_pop / (1 + 99999 * (eulers_num ** (bc * db.time)))


def generate_tags():
    # Generate tags multiplicatively then linearly, kinda
    if db.tagCount < 15000:
        newCount = int(db.tagCount * 1.185 + 1)
        difference = newCount - db.tagCount
        for x in range(difference):
            db.tags.append(str(uuid4()))
        db.tagCount = newCount
    else:
        difference = randint(0, 7)
        for x in range(difference):
            db.tags.append(str(uuid4()))
        db.tagCount += difference


def increase_post_count_per_tag():
    for x in range(db.tagCount):
        prevPostCount = 1
        try:
            prevPostCount = db.numOfPosts[x]
            # TODO Need better generator for randomness
            db.numOfPosts[x] = int(db.numOfPosts[x] * (db.userCount / db.tagCount * (random() + 1) ))
            update_rate(prevPostCount, x)
        except IndexError:
            db.numOfPosts.append(1)
            update_rate(prevPostCount, x, True)
