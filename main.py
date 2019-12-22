"""
Starting main.py with defaults is like starting a new platform from scratch with MINIMAL, not non-existent, user base.

Starts ML algorithm to start determining which tags to choose from.
    - Does not determine which post to choose. Use DLA LIWC for method of choosing safely.
    - Prints the tag chosen
Starts generators

Options:
- timeSpeed: (where 2 = 2 virtual hours / 1 real second)
    - Simulator Speed or Simulator Speed-Up/Slow-Down
- interval: Wait a certain interval of time before choosing another tag (where 1 = 1 virtual hour / 1 real second)
- maxPopulation: Max number of users
"""

from rateTesting.database import Database
from rateTesting.generator import generate_humans, generate_tags, increase_post_count_per_tag
from rateTesting.chooser import main as chooser_run
from time import sleep
import asyncio

# Settings
timeSpeed = 1  # 1 virtual hour / 1 real second. Default: 1
interval = 0.5  # Choosing tag(s) at 30 virtual minutes / 1 real second. Default: 0.5
maxPopulation = 1000000000  # Max population of site. Default: 1,000,000,000
number_of_tags_to_choose = 1  # The number of tags the chooser should select. Default: 1

# Run
if __name__ == "__main__":
    try:
        Database()
    except Exception:
        print("DB already initialized.")
    db = Database.shared()
    print("Starting ML")
    asyncio.run(chooser_run(timeSpeed, interval, number_of_tags_to_choose))
    print("Starting Generators and Updaters")
    while True:
        db.time += timeSpeed
        sleep(timeSpeed)
        asyncio.run(generate_humans(maxPopulation))
        asyncio.run(generate_tags())
        asyncio.run(increase_post_count_per_tag())
