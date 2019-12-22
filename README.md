# Identifying Rate Spikes with Machine Learning

The purpose of this algorithm is to find a better way to identify trending posts on social media sites that have tags included.

Table of Contents:
- Why Should You Implement It + Example
- How it works
- Who Should and How to Integrate
- License: Apache 2.0

----
## Why Should You Implement It with Example
The original intent was to demonstrate how Trending sections of social media apps could work in a primative machine learning style. The code is not limited to social media apps; for example, other use cases include: 

----
## How It Works
I will be using these two terms: 
1. Tags which are like the hashtags of Twitter
2. Posts which are the online texts that are linked together relationship-wise through tags

The algorithm works by constantly updating the rate of a certain tag. That rate, in this case, will be the number of added-posts/minute of a tag.

Once a "rate spike" is identified, a break/tick will be made, identifying the name of the tag, the usual rate, the number of posts, and the mean of the spiked rates. The algorithm successfully identified the tag which would contain a number of posts that can be selected from (not included in this library, of course).

----
## Who Should and How to Integrate
Those who should integrate this methodology are users who have a continuous flow of information/data.

----
## License
The code is licensed under the MIT License, copyleft without need for attribution. Let me know if you use this!
