from .common import InfoExtractor
from ..utils import (
    extract_attributes,
    get_element_html_by_attribute,
    get_element_html_by_id,
    get_element_html_by_class,
    get_element_by_class,
    get_element_by_id,
    traverse_obj
)

from datetime import datetime
import json

class HSVtvIE(InfoExtractor):
    _VALID_URL = r'https?://tv.hsv.de/detail/game/(?P<id>[\w\-\=\?]+)'
    _TESTS = [{
         'url': 'https://tv.hsv.de/detail/game/dn48rspg2qedtinh5f65xugwk?videoId=18475',
         # 'info_dict': {
         #     'id': '97ED907D-7537-4301-BC0E-9BF5F13D4D73',
         #     'ext': 'mp4',
         #     'title': 'md5:62791d1750cfdedb6bc335c09d446a0f',
         #     'description': 'Jahn Regensburg steigt aus der 2. Bundesliga ab. Ein Unentschieden gegen den Karlsruher SC besiegelt Platz 18.',
         #     'display_id': 'jahn-regensburg-karlsruher-sc-2-2-tore-highlights-2-bundesliga__97ED907D-7537-4301-BC0E-9BF5F13D4D73'
         # }
    }]

    def _real_extract(self, url):
        display_id = self._match_id(url).split('__')[0]
        webpage = self._download_webpage(url, display_id)

        return {
            'id': display_id,
            'title': str(get_element_by_class('title', webpage)).split('</span>')[1].replace(r'[<＜][\/\⧸]?[a-zA-Z]{1,15}[>＞]', ''),
            'description': str(get_element_by_class('description', webpage)).replace(r'[<＜][\/\⧸]?[a-zA-Z]{1,15}[>＞]', ''),
            'uploader': 'HSVtv',
            'media_type': str(get_element_by_class('subtitle', webpage)).split(' ')[1].replace(r'[<＜][\/\⧸]?[a-zA-Z]{1,15}[>＞]', ''),
        }
