from .common import InfoExtractor
from ..utils import (
    extract_attributes,
    get_element_html_by_attribute,
    get_element_html_by_id,
    get_element_by_id,
    traverse_obj
)

import json

class Sport1IE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?sport1\.de/tv-video/video/(?P<id>[\w-]+)'
    _TESTS = [{
         'url': 'https://www.sport1.de/tv-video/video/jahn-regensburg-karlsruher-sc-2-2-tore-highlights-2-bundesliga__97ED907D-7537-4301-BC0E-9BF5F13D4D73',
         'info_dict': {
             'id': '97ED907D-7537-4301-BC0E-9BF5F13D4D73',
             'ext': 'mp4',
             'title': 'md5:62791d1750cfdedb6bc335c09d446a0f',
             'description': 'Jahn Regensburg steigt aus der 2. Bundesliga ab. Ein Unentschieden gegen den Karlsruher SC besiegelt Platz 18.',
             'display_id': 'jahn-regensburg-karlsruher-sc-2-2-tore-highlights-2-bundesliga__97ED907D-7537-4301-BC0E-9BF5F13D4D73'
         }
    }]

    def _real_extract(self, url):
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)

        data = traverse_obj(json.loads(get_element_by_id('__NEXT_DATA__', webpage)), ('props', 'pageProps'))

        transformations = traverse_obj(data, ('layoutData', 'transformations'))
        meta = {item['key']: item['value'] for item in traverse_obj(data, ('layoutData', 'meta', 'tracking'))}
        print(meta)

        return {
            'id': traverse_obj(data, ('layoutData', 'id')),
            'title': traverse_obj(data, ('layoutData', 'seoTitle')),
            'formats':[
                {
                    'format_id': fmt,
                    'url': props['url'],
                    'filesize': props['size'],
                    'width': props['width'],
                    'height': props['height'],
                    'http_headers': {
                        'Referer': url
                    }
                }
                for fmt, props in transformations.items()
            ],
            'description': traverse_obj(data, ('layoutData', 'description')),
            'alt_title': traverse_obj(data, ('layoutData', 'title')),
            'display_id': display_id,
            'uploader': 'Sport1',
            'thumbnail': traverse_obj(data, ('layoutData', 'imageUrl')).replace(':width', '1200').replace(':height', '800'),
            'upload_date': meta.get('page_publishing_date').replace('-', '')
        }
