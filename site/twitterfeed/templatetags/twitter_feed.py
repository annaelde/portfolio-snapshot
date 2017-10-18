import twitter
from datetime import datetime

from django.conf import settings
from django import template
from django.views.decorators.cache import cache_page
from django.core.cache import cache

"""
Register template tag in library and create API object
for constant reuse.
"""
register = template.Library()
api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER,
                  consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                  access_token_key=settings.TWITTER_ACCESS,
                  access_token_secret=settings.TWITTER_ACCESS_SECRET)

@register.inclusion_tag('twitterfeed/base.html')
def tweets():
    """
    Gets latest tweet(s) from my timeline, including
    name, timestamp, and text. Returns tweets in iterable object.
    Caches the result for fifteen minutes.
    """
    cache_key = 'twitterfeed'
    cache_time = (60 * 15)
    context = cache.get(cache_key)
    # If there's no fresh tweet in the cache, request it again
    if not context:
        # Try to connect to Twitter API
        try:
            timeline = api.GetUserTimeline(879910574737457153, count=1, exclude_replies=True)
        except:
            context = dict()
            return context
        # Init feed and context
        feed = list()
        context = dict()
        # Iterate through each status received
        for status in timeline:
            text = status.text
            # Replace URLs with URLs in anchor tags
            for url in status.urls:
                path = url.url
                text = text.replace(path, '<a href="' + path + '">' + path + '</a>')
            # Replace hashtags with hashtags in anchor tags
            for hashtag in status.hashtags:
                tag = hashtag.text
                text = text.replace('#' + tag, '<a href="https://twitter.com/hashtag/' + tag + '">#' + tag + '</a>')
            # Add tweet to a list
            feed.append({'user': status.user.screen_name,
                         'time': datetime.strptime(status.created_at, '%a %b %d %H:%M:%S %z %Y'),
                         'text': text, 'id': status.id})
        # Add the twitter feed to the context
        context['tweets'] = feed
        # Update the cache
        cache.set(cache_key, context, cache_time)
    # Return context to the template
    return context
