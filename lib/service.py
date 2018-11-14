"""
Main module for daemon
"""

import os
import time
import traceback

import redis
import gtts

class Daemon(object):
    """
    Main class for daemon
    """

    def __init__(self):

        self.node = os.environ['K8S_NODE']
        self.redis = redis.StrictRedis(host=os.environ['REDIS_HOST'], port=os.environ['REDIS_PORT'])
        self.channel = os.environ['REDIS_CHANNEL']
        self.speech_file = os.environ['SPEECH_FILE']

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

        tts = gtts.gTTS(text, lang=language)
        tts.save(self.speech_file )
        os.system(f"omxplayer {self.speech_file}")

    def process(self, start):
        """
        Processes a message from the channel if later than the daemons start time
        """

        message = json.loads(self.pubsub.get_message()['data'])

        if message["timestamp"] < start:
            continue

        if "node" not in message or message["node"] == self.node:
            self.speak(message["text"], ("language" in message ? message["language"] : None))
            
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
                print(traceback.format_exc())
