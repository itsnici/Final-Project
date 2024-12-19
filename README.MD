# Abstract

This study analyzes public discussions on Reddit regarding ten prominent American politicians across gender and party lines. Through the analysis of 34,283 comments collected from October to December 2024, we employed sentiment analysis and word frequency methods to explore how gender and party affiliation influence public discourse. The results revealed that party affiliation had a stronger impact than gender: Democratic politicians received more positive sentiment scores (0.059) compared to Republican politicians (-0.000071, p < 0.001). When examining gender-party interactions, Democratic female politicians received the highest positive sentiment (0.084), while Republican male politicians showed slightly negative sentiment (-0.006). Notably, the use of gender-related terms was similar between male (0.51%) and female (0.49%) politicians, suggesting that Reddit's community moderation system might filter out overtly biased content. These findings provide insights into how platform characteristics might influence political discussions in digital spaces.

# Tips

For collect the data, you need to get the Reddit API credentials from [Reddit](https://www.reddit.com/prefs/apps).
After replace the credentials in `.env` file, you can run `crawlDataReddit.py` to collect the data.