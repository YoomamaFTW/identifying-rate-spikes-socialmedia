"""
database.py
Instead of a DB like SQLite (one conn) or setting up one (PostgreSQL),
this will instead use a singleton method.
https://www.tutorialspoint.com/python_design_patterns/python_design_patterns_singleton.htm
"""
# TODO Is a singleton even necessary?
# Maybe too much frontend programming + Django apps influenced me


class Database:
    __instance = None
    time = 0
    userCount = 0
    tags = []  # [String]
    tagCount = 0

    # Index of tag -> Index of Posts = Num of Posts for tag
    # E.g. index 0 of tags is "abc". Index 0 of numOfPosts is 10, the number of posts for the tag abc
    numOfPosts = []

    # Rates in posts/1 virtual hour Check example below
    rates = []

    def __init__(self):
        # Virtual private constructor
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Database.__instance = self

    @staticmethod
    def shared():
        # Static access method
        if Database.__instance is None:
            Database()
        return Database.__instance

    # TODO Add method for backing up the data generated from generator by running async task to insert into a SQLite db


# Example of how rates array will work
# Similar to numOfPosts except, instead of a number, there is an array that matches with every 1 virtual hour
rates1 = [[1,2,4,4,3,4,2,1,0], [1,3,3,3,6,7,6,7,6,9], [1, 3, 7, 7, 7]]
rates2 = [[1,2,4,4,3,4,2,1,0,9,10,12,16], [1,3,3,3,6,7,6,7,6,9,7,7,8], [], [], [], [], []]  # Of course, etc.
# In rates 2, you'll see that the array at index 0 shows what is considered a "trending" tag.
