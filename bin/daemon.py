#!/usr/bin/env python

import os

from gtts import gTTS

tts = gTTS('Hey Joren, get your ass out of bed! Sweet Jesus you smell bad!')
tts.save('/tmp/speech.mp3')

os.system("omxplayer /tmp/speech.mp3")