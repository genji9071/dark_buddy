# coding=utf-8
import os

from PIL import Image

from lib.ImportLib import lazy_import

WIDTH = 500
HEIGHT = 500

wordcloud, __getattr__ = lazy_import(__name__, {'WordCloud'})

def make_word_cloud(word_frequencies={}):
    """ make_word_cloud(word_frequencies={"热词":99,"冷词":1}) """
    from wordcloud import WordCloud
    cloud = WordCloud(
        font_path=os.path.dirname(__file__) + "/fontsSourceHanSansCN-Bold.otf",
        width=WIDTH,
        height=HEIGHT,
        background_color=0xffffff,
    )
    return cloud.generate_from_frequencies(word_frequencies)


def make_word_cloud_to_image(word_frequencies={}):
    return make_word_cloud(word_frequencies).to_image()


def make_image_from_bytes(data):
    return Image.frombytes(data=data, size=(WIDTH, HEIGHT), mode="RGB")
