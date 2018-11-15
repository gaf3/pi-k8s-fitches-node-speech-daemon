import unittest
import mock

import os
import json

import service

class MockRedis(object):

    def __init__(self, host, port):

        self.host = host
        self.port = port
        self.channel = None
        self.message = None

    def pubsub(self):

        return self

    def subscribe(self, channel):

        self.channel = channel

    def get_message(self):

        return self.message


class MockgTTS(object):

    def __init__(self, text, lang=None):

        self.text = text
        self.lang = lang
        self.saved = None

    def save(self, file_name):

        self.saved = file_name


class TestService(unittest.TestCase):

    @mock.patch.dict(os.environ, {
        "K8S_NODE": "noisy",
        "REDIS_HOST": "data.com",
        "REDIS_PORT": "667",
        "REDIS_CHANNEL": "stuff",
        "SPEECH_FILE": "blah.mp3",
        "SLEEP": "7"
    })
    @mock.patch("redis.StrictRedis", MockRedis)
    def setUp(self):

        self.daemon = service.Daemon()

    @mock.patch.dict(os.environ, {
        "K8S_NODE": "noisy",
        "REDIS_HOST": "data.com",
        "REDIS_PORT": "667",
        "REDIS_CHANNEL": "stuff",
        "SPEECH_FILE": "blah.mp3",
        "SLEEP": "7"
    })
    @mock.patch("redis.StrictRedis", MockRedis)
    def test___init___(self):

        daemon = service.Daemon()

        self.assertEqual(daemon.node, "noisy")
        self.assertEqual(daemon.redis.host, "data.com")
        self.assertEqual(daemon.redis.port, 667)
        self.assertEqual(daemon.channel, "stuff")
        self.assertEqual(daemon.speech_file, "blah.mp3")
        self.assertEqual(daemon.sleep, 7)
        self.assertIsNone(daemon.pubsub)

    def test_subscribe(self):

        self.daemon.subscribe()

        self.assertEqual(self.daemon.redis, self.daemon.pubsub)
        self.assertEqual(self.daemon.redis.channel, "stuff")

    @mock.patch("gtts.gTTS", MockgTTS)
    @mock.patch("os.system")
    def test_speak(self, mock_system):

        self.daemon.speak("hey", "murican")

        self.assertEqual(self.daemon.tts.text, "hey")
        self.assertEqual(self.daemon.tts.lang, "murican")
        self.assertEqual(self.daemon.tts.saved, "blah.mp3")
        mock_system.assert_called_once_with("omxplayer blah.mp3")

    @mock.patch("gtts.gTTS", MockgTTS)
    @mock.patch("os.system")
    def test_process(self, mock_system):

        self.daemon.subscribe()

        self.daemon.redis.message = json.dumps({
            "data": {
                "timestamp": 7
            }
        })
        self.daemon.process(8)
        self.assertIsNone(self.daemon.tts)

        self.daemon.redis.message = json.dumps({
            "data": {
                "timestamp": 7,
                "text": "hey"
            }
        })
        self.daemon.process(6)
        self.assertEqual(self.daemon.tts.text, "hey")
        self.assertIsNone(self.daemon.tts.lang)

        self.daemon.redis.message = json.dumps({
            "data": {
                "timestamp": 7,
                "text": "hey",
                "language": "murican"
            }
        })
        self.daemon.process(6)
        self.assertEqual(self.daemon.tts.text, "hey")
        self.assertEqual(self.daemon.tts.lang, "murican")




