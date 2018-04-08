# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 17:32:47 2018

@author: daq11
"""
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

def transcribe_gcs(gcs_uri):
    """Transcribes the audio file specified by the gcs_uri."""

    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code='en-US')

    response = client.recognize(config, audio)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print('Transcript: {}'.format(result.alternatives[0].transcript))
        
transcribe_gcs('sample.mp3')