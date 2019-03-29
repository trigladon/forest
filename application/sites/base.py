import attr
import requests
from typing import List
from urllib import parse as urllib_parse
from urllib.parse import urlencode

from .exceptions import StopUrlIteration
from .helper import (
    parse_message,
    to_number
)


@attr.s
class Pagination:
    url: str = attr.ib()

    first_page: int = attr.ib()
    last_page: int = attr.ib()

    current_page: int = attr.ib()

    PATTERN = ()

    PAGE_PREFIX = 'p'

    @classmethod
    def parse(cls, html, url):
        data = parse_message(cls.PATTERN, html)

        first_page = to_number(data.get('first_page'))
        last_page = to_number(data.get('last_page'))
        current_page = first_page

        result = cls(
            url=url,
            first_page=first_page,
            last_page=last_page,
            current_page=current_page
        )

        return result

    def get_current_url(self):
        return self._get_url(self.current_page)

    def get_next_url(self):
        self.build_next_url()
        return self.get_current_url()

    def build_next_url(self):
        self.current_page += 1
        if self.current_page > self.last_page:
            raise StopUrlIteration()

    def _get_url(self, page):
        if page != 1:
            url_data = list(urllib_parse.urlparse(self.url))
            query_param = {key: value[0] for key, value in urllib_parse.parse_qs(url_data[4]).items()}
            query_param.update({self.PAGE_PREFIX: page})
            url_data[4] = urlencode(query_param)
            url = urllib_parse.urlunparse(url_data)
        else:
            url = self.url
        return url


@attr.s
class Item:
    id: id = attr.ib()
    title: str = attr.ib()
    url: str = attr.ib()
    price: float = attr.ib()
    site: str = attr.ib()
    image: str = attr.ib(default='')

    @classmethod
    def parse(cls, data):
        raise NotImplementedError()


@attr.s
class Page:
    number: int = attr.ib()
    items: List[Item] = attr.ib()

    PATTERN = ""

    @classmethod
    def parse(cls, html, number):
        raise NotImplementedError()


@attr.s
class Pages:
    pages: List[Page] = attr.ib()

    @classmethod
    def parse(cls, url):
        raise NotImplementedError()

    @classmethod
    def _get_pages(cls, url):
        raise NotImplementedError()

    @classmethod
    def _get_pagination(cls, url):
        html = cls._get_html(url)
        return Pagination.parse(html, url)

    @classmethod
    def _get_html(cls, url):
        response = requests.get(url)
        return response.content.decode("utf-8")
