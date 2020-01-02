import asyncio
from statistics import mean
from time import sleep
from math import e as eulers_num
from random import randint, random
from uuid import uuid4


class Database:
    __instance = None
    time = 0
    userCount = 0
    tags = []  # [String]
    tagCount = 0
    numOfPosts = []
    rates = []

    def __init__(self):
        # Virtual private constructor
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self

    @staticmethod
    def shared():
        if Database.__instance is None:
            Database()
        return Database.__instance


db = Database.shared()


async def chooser_run(speed, interval, num_of_tags, posts_threshold=15):
    await asyncio.sleep(speed * 10)
    min_speed = 0.001
    old_speed = speed * interval
    while True:
        if old_speed < min_speed:
            await asyncio.sleep(min_speed)
        else:
            await asyncio.sleep(old_speed)

        tags_rates = {}
        for x in db.rates:
            min_rates_needed = 4
            if len(tags_rates) == num_of_tags:
                break
            elif len(x) < min_rates_needed or db.numOfPosts[x] < posts_threshold:
                continue
            rates = x[:min_rates_needed:-1]
            xs = []
            ys = []
            current_time = db.time
            for i, j in enumerate(rates):
                xs.append(current_time - i)
                ys.append(j)
            mean_of_xs = mean(xs)
            squared_xs = []
            for a in xs:
                squared_xs.append(a ** 2)
            combined_xs_ys = []
            for i, a in enumerate(xs):
                combined_xs_ys.append(a * ys[i])
            m = ((mean_of_xs * mean(ys)) - mean(combined_xs_ys)) / \
                (mean_of_xs ** 2 - mean(squared_xs))
            if m >= 0:
                tags_rates[db.tags[x]] = m
        chosen_tags = sorted(tags_rates, key=tags_rates.get, reverse=True)
        print("Tags selected:\n", chosen_tags)


async def generate_humans(max_pop):
    db.userCount = max_pop / (1 + 99999 * (eulers_num ** (-.000000002 * db.time)))


async def generate_tags():
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


def update_rate(prevPostCount, index, new=False):
    if new:
        current = db.numOfPosts[index]
        new_rate = current - prevPostCount
        (db.rates[index]).append(new_rate)
    else:
        db.rates.append([1])


async def increase_post_count_per_tag():
    for x in range(db.tagCount):
        prevPostCount = 1
        try:
            prevPostCount = db.numOfPosts[x]
            db.numOfPosts[x] = int(db.numOfPosts[x] * (db.userCount / db.tagCount * (random() + 1) ))
            update_rate(prevPostCount, x)
        except IndexError:
            db.numOfPosts.append(1)
            update_rate(prevPostCount, x, True)


if __name__ == "__main__":
    try:
        Database()
    except Exception:
        print("DB already initialized.")
    timeSpeed = 1
    interval = 0.5
    maxPopulation = 1000000000
    number_of_tags_to_choose = 1
    asyncio.run(chooser_run(timeSpeed, interval, number_of_tags_to_choose))
    while True:
        db.time += timeSpeed
        sleep(timeSpeed)
        asyncio.run(generate_humans(maxPopulation))
        asyncio.run(generate_tags())
        asyncio.run(increase_post_count_per_tag())
