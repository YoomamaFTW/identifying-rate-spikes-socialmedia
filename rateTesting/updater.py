from .database import Database
db = Database.shared()


def update_rate(prevPostCount, index, new=False):
    if new:
        current = db.numOfPosts[index]
        new_rate = current - prevPostCount
        (db.rates[index]).append(new_rate)
    else:
        db.rates.append([1])
