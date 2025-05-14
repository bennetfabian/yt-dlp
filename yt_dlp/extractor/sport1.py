from .common import InfoExtractor
from ..utils import (
    extract_attributes,
    get_element_html_by_attribute,
    get_element_html_by_id,
    get_element_by_id,
    traverse_obj
)

from datetime import datetime
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
        display_id = self._match_id(url).split('__')[0]
        webpage = self._download_webpage(url, display_id)

        data = traverse_obj(json.loads(get_element_by_id('__NEXT_DATA__', webpage)), ('props', 'pageProps', 'layoutData'))

        transformations = data.get('transformations')
        meta = {item['key']: item['value'] for item in traverse_obj(data, ('meta', 'tracking'))}

        upload_datetime = datetime.strptime(f"{meta.get('page_publishing_date')} {meta.get('page_publishing_time')}", "%Y-%m-%d %H:%M:%S")
        published_datetime = datetime.strptime(f"{meta.get('video_publishing_date')} {meta.get('video_publishing_time')}", "%Y-%m-%d %H:%M:%S")
        modified_datetime = datetime.strptime(f"{meta.get('page_updated_date')} {meta.get('page_updated_time')}", "%Y-%m-%d %H:%M:%S")

        minutes, seconds = map(int, meta.get('video_duration').split(":"))
        duration_seconds = minutes * 60 + seconds

        tags_object = data.get('tags')

        return {
            'id': data.get('id'),
            'title': data.get('seoTitle'),
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
            'alt_title': data.get('title'),
            'description': data.get('description'),
            'display_id': display_id,
            'uploader': 'Sport1',
            'thumbnail': traverse_obj(data, ('layoutData', 'imageUrl')).replace(':width', '1200').replace(':height', '800'),
            'timestamp': int(upload_datetime.timestamp()),
            'upload_date': upload_datetime.strftime("%Y%m%d"),
            'release_timestamp': int(published_datetime.timestamp()),
            'release_date': published_datetime.strftime("%Y%m%d"),
            'release_year': published_datetime.strftime("%Y"),
            'modified_timestamp': int(modified_datetime.timestamp()),
            'modified_date': modified_datetime.strftime("%Y%m%d"),
            'duration': duration_seconds,
            'duration_string': meta.get('video_duration'),
            'media_type': meta.get('content_type'),
            'tags': [item["title"] for item in tags_object] + [item["parent"]["title"] for item in tags_object if "parent" in item]
        }
