import asyncio
from .database import Database

db = Database.shared()


async def main(speed, interval, num_of_tags):
    await asyncio.sleep(speed * 10)
    min_speed = 0.01
    old_speed = speed * interval
    cycle = 1
    while True:
        chosen_tags = []
        if old_speed < min_speed:
            await asyncio.sleep(min_speed)
        else:
            await asyncio.sleep(old_speed)
        for x in db.rates:
            if len(chosen_tags) == num_of_tags:
                break
            elif len(x) < 2:
                continue
            rates = x[::-1]

            """
            Simplified summary:
            1. Grab the array of rates for 1 tag.
            2. Flip it for easier time
            3. Use linear regression vs exponential regression.
            4. If exponential regression's r^2 higher than linear, then store it's r^2 and tag in separate arrays
            5. Else, skip.
            6. Use num_of_tags to break out of loop
            
            TODO:
            1. Need to only analyze the latest rates, with the condition that exponential is better than linear.
            2. We can also use logistic regression to check that it's actually trending now rather than before.
            """
        print("Cycle ", cycle, ":")
        if len(chosen_tags) < num_of_tags:
            print("There were only ", len(chosen_tags), " out of the needed ", num_of_tags,
                  " tags that could be chosen as trending. Recommendation: choose multiple posts from the top ",
                  num_of_tags-len(chosen_tags), ".")
        print("Tags selected: ")
        for x in chosen_tags:
            print(x, " (rate before: ", ", rate after:", ", number of posts in tag: ", ")")
        cycle += 1
