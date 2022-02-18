#!/bin/zsh /Users/kjaymiller/.asdf/shims/python
#  <xbar.title>PodChecker/xbar.title>
#  <xbar.version>v1.0</xbar.version>
#  <xbar.author>Jay Miller</xbar.author>
#  <xbar.author.github>kjaymiller</xbar.author.github>
#  <xbar.desc>Checks Date of Latest Podcast Episode.</xbar.desc>
# 
# Variables become preferences in the app:
# <xbar.var>string(POD_URL="https://www.relay.fm/conduit/feed"): API key to get access to remote data.</xbar.var>
# <xbar.var>number(RECORDING_DAYS_AFTER=0): Number of days to warn before recording episode. Skip if Empty</xbar.var>
# <xbar.var>number(PUBLISH_DAYS_AFTER=0): Number of days to warn before publishing episode. Skip if Empty</xbar.var>

import feedparser
import os
from datetime import datetime, time, timedelta
from time import mktime


def get_latest_episode(pod_url: str) -> str:
    """Gets the Latest Episode from pod_url"""
    feed = feedparser.parse(pod_url)
    days_since = (datetime.fromtimestamp(mktime(feed.entries[0]['published_parsed'])) -  datetime.now()).days
    return (feed.feed['title'], days_since)

if __name__ == "__main__":
    title, days = get_latest_episode(os.environ.get('POD_URL'))
    publish_days = -int(os.environ.get('PUBLISH_DAYS_AFTER', 0))
    recording_days = -int(os.environ.get('RECORDING_DAYS_AFTER', 0))

    if publish_days and publish_days >= days:
        print(f":bangbang: Publish {title}")
        print('---')
        print(f"{title}: {days} days since last episode")

    elif recording_days and recording_days >= days:
        print(f":red_circle: Record {title}")
        print('---')
        print(f"{title}: {days} days since last episode")

    elif recording_days:
        days_left = days - recording_days
        print(f":white_check_mark: {title}\n---\n{days_left} days until next {title} recording")