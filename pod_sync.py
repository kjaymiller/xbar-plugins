import feedparser

pod_url = "https://www.relay.fm/conduit/feed"
site_url = "https://kjaymiller.com/blog.rss.xml"

def get_latest_episode() -> str:
    """Gets the Latest Episode from pod_url"""
    feed = feedparser.get(pod_url)
    for entry in feed.items():
        print(entry)


if __name__ == "__main__":
    get_latest_episode()