import tweepy
import tweepy_auth

auth = tweepy.OAuthHandler(tweepy_auth.CONSUMER_KEY, tweepy_auth.CONSUMER_SECRET)
auth.set_access_token(tweepy_auth.ACCESS_TOKEN, tweepy_auth.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
api.direct_messages()
cricTweet = tweepy.Cursor(api.search, q='#cricket').items(10)

for tweet in cricTweet:
    print tweet.text

listener = StreamMonitor(epd, image, draw, name_font, message_font)
stream = tweepy.Stream(auth, listener)
setTerms = argv
# stream.sample()   # low bandwidth public stream
stream.filter(track=setTerms)


class StreamMonitor(tweepy.StreamListener):
    """class to receive twitter message"""

    def __init__(self, epd, image, draw, name_font, message_font, *args$
        super(StreamMonitor, self).__init__(*args, **kwargs)
        self._epd = epd
        self._image = image
        self._draw = draw
        self._name_font = name_font
        self._message_font = message_font

    def on_status(self, status):
        screen_name = status.user.screen_name.encode('utf-8')
        text = status.text.encode('utf-8')
        print('@{u:s} Said:  {m:s}'.format(u=screen_name, m=text))

        w, h = self._image.size
        self._draw.rectangle((0, 0, w, h), fill=WHITE, outline=WHITE)
        self._draw.text((20, 0), '@' + status.user.screen_name, fill=BLACK, font=self._name_font)
        y = 18
        for line in textwrap.wrap(status.text, 24):   # tweet(140) / 24 => 6 lines
            self._draw.text((0, y), line, fill=BLACK, font=self._message_font)
            y = y + 12

        # display image on the panel
        self._epd.display(self._image)
        self._epd.update()


    def on_error(self, error):
        print("error = {e:d}".format(e=error))
        time.sleep(5)
        # continue reading stream even after error
        return True

    def on_timeout(self):
        print("timeout occurred")
        # continue reading stream even after timeout
        return True