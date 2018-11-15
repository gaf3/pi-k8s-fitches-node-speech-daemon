"""
Main module for daemon
"""

import os
import time
import traceback

import json
import redis
import gtts

class Daemon(object):
    """
    Main class for daemon
    """

    def __init__(self):

        self.node = os.environ['K8S_NODE']
        self.redis = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=int(os.environ['REDIS_PORT']))
        self.channel = os.environ['REDIS_CHANNEL']
        self.speech_file = os.environ['SPEECH_FILE']
        self.sleep = int(os.environ['SLEEP'])

        self.pubsub = None
        self.tts = None

    def subscribe(self):
        """
        Subscribes to the channel on Redis
        """

        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(self.channel) 

    def speak(self, text, language=None):
        """
        Speaks the text in the language
        """

        self.tts = gtts.gTTS(text, lang=language)
        self.tts.save(self.speech_file)
        os.system("omxplayer %s" % self.speech_file)

    def process(self, start):
        """
        Processes a message from the channel if later than the daemons start time
        """

        message = json.loads(self.pubsub.get_message())['data']

        if message["timestamp"] < start:
            return

        if "node" not in message or message["node"] == self.node:
            self.speak(message["text"], (message["language"] if "language" in message else None))
            
    def run(self):
        """
        Runs the daemon
        """

        start = time.time()
        self.subscribe()

        while True:
            try:
                self.process(start)
                time.sleep(self.sleep)
            except Exception as exception:
                print(exception)
                print(traceback.format_exc())
