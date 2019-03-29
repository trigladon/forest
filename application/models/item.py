import attr

from datetime import datetime

from ..sites.base import Item as SiteItem
from . import constants


@attr.s
class Item:
    site_id: id = attr.ib()
    title: str = attr.ib()
    site: str = attr.ib()
    price: float = attr.ib()
    image: str = attr.ib()
    url: str = attr.ib()
    update_date: str = attr.ib()
    create_date: str = attr.ib()
    id: id = attr.ib(default=None)
    state: str = attr.ib(default=constants.STATE_NEW)

    @staticmethod
    def table_name():
        return 'items'

    @classmethod
    def db_parse(cls, data):
        result = cls(
            id=data[0],
            title=data[1],
            site=data[2],
            price=data[3],
            site_id=data[4],
            url=data[5],
            image=data[6],
            create_date=data[7],
            update_date=data[8],
            state=constants.STATE_OLD
        )
        return result

    @classmethod
    def parse(cls, item: SiteItem):
        datetime_today = datetime.today().isoformat()
        result = cls(
            site_id=item.id,
            title=item.title,
            site=item.site,
            price=item.price,
            url=item.url,
            image=item.image,
            create_date=datetime_today,
            update_date=datetime_today,
            state=constants.STATE_NEW
        )
        return result

    def update(self, item):
        datetime_today = datetime.today().isoformat()
        self.id = item.id
        self.update_date = datetime_today
        self.state = constants.STATE_UPDATED

    def update_old(self, item):
        self.id = item.id
        self.state = constants.STATE_OLD

    def has_updates(self, item):
        return self.title != item.title or \
               self.price != item.price

    def is_same(self, item):
        return self.site_id == item.site_id and \
               self.site == item.site
