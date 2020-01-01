import asyncio
from .database import Database
from statistics import mean, stdev
from math import log10

db = Database.shared()


async def main(speed, interval, num_of_tags, posts_threshold=15):
    await asyncio.sleep(speed * 10)
    min_speed = 0.001
    old_speed = speed * interval
    cycle = 1
    while True:
        chosen_tags = []
        if old_speed < min_speed:
            await asyncio.sleep(min_speed)
        else:
            await asyncio.sleep(old_speed)
        cycle_start_time = db.time
        for x in db.rates:
            if len(chosen_tags) == num_of_tags:
                break
            elif len(x) < 2 or db.numOfPosts[x] < posts_threshold:
                continue
            rates = x[::-1]
            data_points = []
            current_time = db.time
            for i, j in enumerate(rates):
                data_points.append((current_time-i, j))

            """
            Ok, so instead of comparing three regression models, I need to constantly use an exponential regression
            in different spots of data (overall last 250, and last 50).
            
            We just need to analyze it in different methods, such as coefficient of determination and residuals
            """
        now_time = db.time
        print("Cycle ", cycle, ":\nAt time ", cycle_start_time, ", but it is ", now_time, " time:")
        if len(chosen_tags) < num_of_tags:
            print("There were only ", len(chosen_tags), " out of the needed ", num_of_tags,
                  " tags that could be chosen as trending. Recommendation: choose multiple posts from the top ",
                  num_of_tags-len(chosen_tags), ".")
        print("Tags selected: ")
        for x in chosen_tags:
            print(x, " (rate before: ", ", rate after:", ", number of posts in tag: ", ")\n")
        cycle += 1
