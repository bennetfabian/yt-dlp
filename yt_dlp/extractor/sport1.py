from .common import InfoExtractor
from ..utils import (
    extract_attributes,
    get_element_html_by_attribute,
    get_element_html_by_id,
    get_element_by_id,
)

import json

class Sport1IE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?sport1\.de/tv-video/video/(?P<id>[\w-]+)'
    _TESTS = [{
         'url': 'https://www.sport1.de/tv-video/video/jahn-regensburg-karlsruher-sc-2-2-tore-highlights-2-bundesliga__97ED907D-7537-4301-BC0E-9BF5F13D4D73',
         'info_dict': {
             'id': 'jahn-regensburg-karlsruher-sc-2-2-tore-highlights-2-bundesliga__97ED907D-7537-4301-BC0E-9BF5F13D4D73',
             'ext': 'mp4',
             'title': 'md5:5f0cabf75dae35179cf5675ba8f1f885',
             'description': 'Jahn Regensburg steigt aus der 2. Bundesliga ab. Ein Unentschieden gegen den Karlsruher SC besiegelt Platz 18.',
             'display_id': 'jahn-regensburg-karlsruher-sc-2-2-tore-highlights-2-bundesliga__97ED907D-7537-4301-BC0E-9BF5F13D4D73'
         },
         'params': {'skip_download': 'm3u8'},
    }]

    def _real_extract(self, url):
        display_id = self._match_id(url)
        webpage = self._download_webpage(url, display_id)

        # video_title = extract_attributes(get_element_html_by_attribute('data-testid', 'video-title', webpage)["data-testid"] or '')
        # video_description = extract_attributes(get_element_html_by_attribute('data-testid', 'video-description', webpage)["data-testid"] or '')

        # data = json.loads(get_element_by_id('__NEXT_DATA__', webpage))
        print(get_element_html_by_id('__NEXT_DATA__', webpage))

        return {
            'id': 'jahn-regensburg-karlsruher-sc-2-2-tore-highlights-2-bundesliga__97ED907D-7537-4301-BC0E-9BF5F13D4D73',
            'title': 'Unentschieden besiegelt Regensburgs Platz 18',
            'description': 'Jahn Regensburg steigt aus der 2. Bundesliga ab. Ein Unentschieden gegen den Karlsruher SC besiegelt Platz 18.',
            'ext': 'mp4',
            'display_id': 'jahn-regensburg-karlsruher-sc-2-2-tore-highlights-2-bundesliga__97ED907D-7537-4301-BC0E-9BF5F13D4D73'
        }
