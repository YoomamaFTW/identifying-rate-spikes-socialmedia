import asyncio
from .database import Database
from statistics import mean

db = Database.shared()


async def main(speed, interval, num_of_tags, posts_threshold=15):
    await asyncio.sleep(speed * 10)
    min_speed = 0.001
    old_speed = speed * interval
    cycle = 1
    while True:
        if old_speed < min_speed:
            await asyncio.sleep(min_speed)
        else:
            await asyncio.sleep(old_speed)
        cycle_start_time = db.time

        tags_rates = {}
        for x in db.rates:
            # Setting up data points
            if len(tags_rates) == num_of_tags:
                break
            elif len(x) < 10 or db.numOfPosts[x] < posts_threshold:
                # If the number of rates is less than a certain number
                # or if the number of posts for a tag is less than post_threshold,
                # then continue
                continue
            rates = x[::-1]
            xs = []
            ys = []
            current_time = db.time
            for i, j in enumerate(rates):
                xs.append(current_time-i)
                ys.append(j)
            """
            Time to do the tests
            1. Collected data points are used inside a linear regression model
            2. We will attain a slope and r^2
            
            Might delete r^2 because it could take up too much time.
            Additionally, I'm not sure how useful this would actually be.
            For now, not implementing
            3. If r^2 for a model is less than 67%, then cancel its candidacy
            
            4. If the slope is less than 0, then cancel its candidacy
            5. All eligible candidates are put into a dict (name: slope).
            6. Order the dict by val largest -> smallest.
            7. Choose however many you want using num_of_tags
            """
            mean_of_xs = mean(xs)
            squared_xs = []
            for a in xs:
                squared_xs.append(a**2)
            combined_xs_ys = []
            for i, a in enumerate(xs):
                combined_xs_ys.append(a * ys[i])
            m = ((mean_of_xs * mean(ys)) - mean(combined_xs_ys)) / \
                (mean_of_xs**2 - mean(squared_xs))
            if m >= 0:
                tags_rates[db.tags[x]] = m
        # Ordered from greatest slope to least
        chosen_tags = sorted(tags_rates, key=tags_rates.get, reverse=True)
        now_time = db.time
        print("Cycle ", cycle, ":\nAt time ", cycle_start_time, ", but it is ", now_time, " time:")
        if len(chosen_tags) < num_of_tags:  # If couldn't get enough tags to = num_of_tags
            print("There were only ", len(chosen_tags), " out of the needed ", num_of_tags,
                  " tags that could be chosen as trending. Recommendation: choose multiple posts from the top ",
                  num_of_tags-len(chosen_tags), ".")
        print("Tags selected:\n")
        for x in chosen_tags:
            print(x, " (rate before: ", ", rate after:", ", number of posts in tag: ", ")\n")
        cycle += 1
