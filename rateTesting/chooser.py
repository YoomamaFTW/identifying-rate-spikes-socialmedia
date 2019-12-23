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
            log_reg = logistic_regression(data_points)
            lin_reg = linear_regression(data_points)
            exp_reg = exponential_regression(data_points)

            # Logic
            if log_reg > lin_reg or log_reg > exp_reg:
                continue

            # We need to take a deeper look at the linear model to determine if it's actually linear or is there
            # more to it that shows exponential increase.
            numberOfPosts = db.numOfPosts[x]
            latest_posts = 4
            if numberOfPosts > 100:
                latest_posts = int(latest_posts / 3)
            latest_exp_reg = exponential_regression(data_points[:latest_posts])
            latest_lin_reg = linear_regression(data_points[:latest_posts])
            if latest_exp_reg > 85 and latest_exp_reg > latest_lin_reg:
                chosen_tags.append(db.tags[x])
            """
            TODO:
            - We can also use logistic regression to check that it's actually trending now rather than before.
            - Advised to use Shapiro-Wilk test if n=numofposts=2000
            """
        print("Cycle ", cycle, ":")
        if len(chosen_tags) < num_of_tags:
            print("There were only ", len(chosen_tags), " out of the needed ", num_of_tags,
                  " tags that could be chosen as trending. Recommendation: choose multiple posts from the top ",
                  num_of_tags-len(chosen_tags), ".")
        print("Tags selected: ")
        for x in chosen_tags:
            print(x, " (rate before: ", ", rate after:", ", number of posts in tag: ", ")\n")
        cycle += 1


def calculate_score(r_squared, residual_std):
    # return residual_std / r_squared
    return r_squared


def linear_regression(dp):
    n = len(dp)
    xs = [x[0] for x in dp]
    ys = [y[1] for y in dp]
    meanofxs = mean(xs)
    meanofys = mean(ys)

    # regression for residual
    blah = 0
    for i, j in enumerate(xs):
        blah += i * ys[j]
    SS_xy = blah - (n * meanofxs * meanofys)
    blah = 0
    for i, j in enumerate(xs):
        blah += i**2
    SS_xx = blah - n * meanofxs**2
    slope = SS_xy / SS_xx
    yint = meanofys - slope * meanofxs

    # y = mx + b. To get residuals, you need expected - observed, find the stddev

    # r-squared
    sx = stdev(xs, meanofxs)
    sy = stdev(ys, meanofys)
    summation = 0
    for i in dp:
        summation += (i[0] - meanofxs) * (i[1] - meanofys)
    r_sqr = (summation / sx / sy / (n-1)) ** 2
    return calculate_score(r_sqr, 1)


def exponential_regression(dp):
    # Calculating r^2 isn't good for nonlinear, so we'll only be using the residual plot.
    xs = [x[0] for x in dp]
    ys = [log10(y[0]) for y in dp]
    return 1


def logistic_regression(dp):
    # This is different from the other two
    # https://statisticalhorizons.com/wp-content/uploads/GOFForLogisticRegression-Paper.pdf
    # https://en.wikipedia.org/wiki/Pearson%27s_chi-squared_test#Calculating_the_test-statistic
    return 1