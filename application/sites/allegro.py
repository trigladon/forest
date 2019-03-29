import attr
import json

from urllib import parse as urllib_parse

from configuration.logger import get_logger
from .exceptions import StopUrlIteration
from application.models import constants

from .helper import (
    parse_message,
    to_number
)
from . import base


logger = get_logger(__name__)


@attr.s
class Item(base.Item):

    @classmethod
    def parse(cls, data):
        image = ''

        if data.get('thumbnails') and data.get('thumbnails').get('s128'):
            image = data.get('thumbnails').get('s128')

        return cls(
            id=to_number(data.get('id')),
            url=data.get('url'),
            title=data.get('title').get('text'),
            price=to_number(data.get('price').get('normal').get('amount')),
            image=image,
            site=constants.ITEM_SITE_ALLEGRO
        )


@attr.s
class Pagination(base.Pagination):
    PATTERN = (
        r"window\[\'__listing_StoreState_base\'\]\s*=\s*(?P<json>\{.*?\});"
    )

    @classmethod
    def parse(cls, html, url):
        data = parse_message(cls.PATTERN, html)
        query_param = urllib_parse.parse_qs(urllib_parse.urlparse(url).query)
        j_data = json.loads(data.get('json'))
        search_data = j_data.get('items').get('searchMeta')

        if search_data:
            first_page = 1
            page = query_param.get('p', 1)
            current_page = to_number(page[0] if isinstance(page, list) else 1)
            last_page = to_number(search_data.get('lastAvailablePage'))
        else:
            first_page = current_page = last_page = 1

        result = cls(
            url=url,
            first_page=first_page,
            last_page=last_page,
            current_page=current_page
        )

        return result


@attr.s
class Page(base.Page):
    PATTERN = (
        r"window\[\'__listing_StoreState_base\'\]\s*=\s*(?P<json>\{.*?\});"
    )

    @classmethod
    def parse(cls, html, number):
        data = parse_message(cls.PATTERN, html)
        j_items = json.loads(data.get('json'))
        items = []
        if j_items:
            try:
                items_groups = j_items.get('items').get('itemsGroups')
                for group in items_groups:
                    t_items = group.get('items')
                    for t_item in t_items:
                        item = Item.parse(t_item)
                        items.append(item)
            except (KeyError, IndexError) as e:
                logger.exception(e)

        result = cls(
            number=number,
            items=items
        )

        return result


class Pages(base.Pages):

    @classmethod
    def parse(cls, url):
        pages = cls._get_pages(url)
        result = cls(
            pages=pages
        )
        return result

    @classmethod
    def _get_page(cls, url, number):
        html = cls._get_html(url)
        return Page.parse(html, number)

    @classmethod
    def _get_pages(cls, url):
        pagination = cls._get_pagination(url)
        pages = []
        while True:
            try:
                logger.info(f'Parse page {url}')
                url = pagination.get_current_url()
                page = cls._get_page(url, pagination.current_page)
                pages.append(page)
                pagination.build_next_url()
            except StopUrlIteration:
                break

        return pages

    @classmethod
    def _get_pagination(cls, url):
        html = cls._get_html(url)
        return Pagination.parse(html, url)



