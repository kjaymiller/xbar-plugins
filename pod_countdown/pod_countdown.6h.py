#!/bin/zsh /Users/kjaymiller/.asdf/shims/python
#  <xbar.title>PodChecker/xbar.title>
#  <xbar.version>v1.0</xbar.version>
#  <xbar.author>Jay Miller</xbar.author>
#  <xbar.author.github>kjaymiller</xbar.author.github>
#  <xbar.image>https://github.com/kjaymiller/xbar-plugins/blob/main/pod_countdown/images/status-good.png?raw=true</xbar.image>
#  <xbar.desc>Checks Date of Latest Podcast Episode and Alerts you when you should record or publish.</xbar.desc>
#  <xbar.abouturl>https://github.com/kjaymiller/xbar-plugins/tree/main/pod_countdown</xbar.abouturl>

# Variables become preferences in the app:
# <xbar.var>string(PODCAST_URL=""): RSS Feed URL for Podcast.</xbar.var>
# <xbar.var>number(RECORDING_DAYS_AFTER=0): (optional) Number of days to warn before recording episode.</xbar.var>
# <xbar.var>string(RECORDING_ACTION=""): (optional) URL to run on click.</xbar.var>
# <xbar.var>number(PUBLISH_DAYS_AFTER=0): (optional) Number of days to warn before publishing episode.</xbar.var>
# <xbar.var>string(PUBLISH_ACTION=""): (optional) URL to run on click.</xbar.var>


import feedparser
import os
from datetime import datetime, time, timedelta
from time import mktime


def get_latest_episode(pod_url: str) -> str:
    """Gets the Latest Episode from pod_url"""
    feed = feedparser.parse(pod_url)
    days_since = (datetime.now() - datetime.fromtimestamp(mktime(feed.entries[0]['published_parsed']))).days 
    return (feed.feed['title'], days_since, feed.entries[0]['title'], feed.entries[0]['link'])


def check_date(*, title: str, current_days: int, action_check: str, message_icon: str, status:str, color: str) -> str:
    """Checks the days_check against the days and returns a string to display"""
    message = f"{message_icon}{status}: {title} | font=SFPro-Bold\n---\n{title}: {days} days since last episode | font=SFPro-Bold | color={color}"

    if publish_action:
        message += f" | href={publish_action}"

    return message


if __name__ == "__main__":
    podcast_title, days, episode_title, link = get_latest_episode(os.environ.get('PODCAST_URL'))
    publish_days = int(os.environ.get('PUBLISH_DAYS_AFTER', 0))
    publish_action = os.environ.get('PUBLISH_ACTION', '')
    recording_days = int(os.environ.get('RECORDING_DAYS_AFTER', 0))
    recording_action = os.environ.get('RECORDING_ACTION', '')
    
    if publish_days and publish_days <= days:
        print(check_date(
                title=podcast_title,
                current_days=days,
                action_check=publish_action,
                message_icon=":bangbang:",
                status="Publish",
                color="#0256DD",
                ))

    elif recording_days and recording_days <= days:
        print(check_date(
                title=podcast_title,
                current_days=days,
                action_check=recording_action,
                message_icon=":red_circle:",
                status="Record",
                color="#B91514",
                ))


    elif recording_days:
        days_left =  recording_days - days
        print(f":white_check_mark: {podcast_title}\n---\n{days_left} days until next {podcast_title} recording | font=SFPro-Bold")

    print(f"Latest Episode: {episode_title} | href={link}")