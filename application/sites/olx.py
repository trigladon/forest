import attr
import json
import re

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
class Pagination(base.Pagination):

    PATTERN = (
        r"var\s+trackingData\s*=\s*JSON\.parse\(\'(?P<json>\{.*?\})\'\);"
    )

    PAGE_PREFIX = 'page'

    @classmethod
    def parse(cls, html, url):
        data = parse_message(cls.PATTERN, html)
        json_str = data.get('json')
        if json_str:
            j_data = json.loads(json_str)
            search_data = j_data.get('pageView')
            if search_data:
                first_page = 1
                current_page = to_number(search_data.get('page_nb'))
                last_page = to_number(search_data.get('page_count'))
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
class Item(base.Item):

    @classmethod
    def parse(cls, data):
        id = to_number(data[0])
        url = data[1]
        image = data[3]
        title = data[4]
        price = to_number(data[5])

        result = cls(
            id=id,
            url=url,
            title=title,
            price=price,
            image=image,
            site=constants.ITEM_SITE_OLX
        )

        return result


@attr.s
class Page(base.Page):
    PATTERN = (
        r"<div class=\"offer-wrapper\">\s*<table[^>]+data\-id=\"(?P<id>[\d]+)\">\s*<tbody>\s*<tr>\s*<td[^>]*>\s*<a[^>]*href=\"(?P<url>[^\"]+)\"[^>]*>\s*(<img[^>]*src=\"(?P<imgurl>[^\"]*)\"[^>]*>|)\s*[^>]*>[^>]*>[^>]*>[^>]*>[^>]*>[^>]*>\s*[^>]*>*[^>]*>*[^>]*>*<strong[^>]*>(?P<title>[^<]*)[^>]*>[^>]*>*[^>]*>*[^>]*>*[^>]*>*[^>]*>*[^>]*>*[^>]*>*[^>]*>*[^>]*>*[^>]*>*\s*<strong[^>]*>(?P<price>[\d\ ]+)[^>]*>"
    )

    @classmethod
    def parse(cls, html, number):
        t_items = re.findall(cls.PATTERN, html)
        items = []

        if t_items:
            for t_item in t_items:
                item = Item.parse(t_item)
                items.append(item)

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



