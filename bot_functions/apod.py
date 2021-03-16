import os
import requests
from dotenv import load_dotenv
from helpers import *
from constants import TABLES
from discord import Embed

# Set up environment variables
load_dotenv()


class Apod:
    def __init__(self, date=today()):
        self.NASA_API_KEY = os.getenv('NASA_API_KEY')
        self.result = None
        self.response_msg = None
        self.date = date

    def fetch(self):
        """
        Fetch NASA's Astronomical Picture of the Day with the image/video
        and its description
        """
        cached_result = get_from_cache(TABLES["APOD"], 'date', self.date)

        if cached_result:
            self.result = cached_result
            print("apod(): Retrieved from cache")
        else:
            print("apod(): Cache not found. Freshly fetched")
            try:
                r = requests.get("https://api.nasa.gov/planetary/apod", params={
                    'api_key': self.NASA_API_KEY,
                    'thumbs': True
                })
                r_json = r.json()
                self.result = r_json
                write_to_cache(TABLES['APOD'], self.result, 'date')
            except Exception as e:
                print("apod(): Exception: ", e)

    def parse_result(self):
        """
        Convert the fetched result into discord message format
        with text content and an embed
        """
        if self.result:
            self.response_msg = {'content': self.result['explanation']}
            # Youtube URL
            if is_youtube_url(self.result['url']):
                yt_url = yt_embed_to_playable(self.result['url'])
                self.response_msg['content'] += f'\n{yt_url}'
                return
            embed = Embed(title=self.result['title'], url=self.result['url'], type="rich")
            # Non-YouTube Video URL
            if self.result['media_type'] == 'video':
                embed.set_image(url=self.result['thumbnail_url'])
            # Image URL
            else:
                embed.set_image(url=self.result['url'])
            self.response_msg['embed'] = embed

    def response(self):
        """
        Fetch, Parse and return the response message
        :return: dict
        """
        self.fetch()
        self.parse_result()
        return self.response_msg
