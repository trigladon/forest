import time

from configuration import (
    settings
)
from application.utils import mail

from application.sites.olx import Pages as OLXPages
from application.sites.allegro import Pages as AllegroPages

from application.manager.items import ItemsManager
from application.models.item import Item
from application.models import constants

from configuration.logger import get_logger

logger = get_logger(__name__)


def get_items():
    pages = (
        OLXPages.parse(settings.OLX_URL),
        AllegroPages.parse(settings.ALEGRO_URL),
    )

    items = []

    for site_pages in pages:
        for page in site_pages.pages:
            for item in page.items:
                if settings.PRICE_FROM <= item.price:
                    items.append(Item.parse(item))
    print(len(items))
    return items


def filter_items(items):
    result = {
        constants.STATE_NEW: [],
        constants.STATE_UPDATED: [],
        constants.STATE_OLD: []
    }

    ItemsManager.delete_removed_items(items)
    db_items = ItemsManager.fetch_all()
    for item in items:
        for db_item in db_items:
            if item.is_same(db_item):
                if item.has_updates(db_item):
                    item.update(db_item)
                else:
                    item.update_old(db_item)
                break

    for item in items:
        ItemsManager.save(item)
        result[item.state].append(item)

    return result


def send_email(sort_items):
    if sort_items.get(constants.STATE_NEW) or sort_items.get(constants.STATE_UPDATED):
        logger.info('Build email')

        emails = [
            settings.EMAIL_TO,
        ]
        for email in emails:
            mail.send(
                email_from=settings.EMAIL_FROM,
                email_to=email,
                subject="\"Wirex\" cтанки с allegro.pl и olx.pl",
                template='mails/index.html',
                variables={
                    'states': constants.STATES,
                    'states_labels': constants.STATES_LABELS,
                    'items': sort_items
                }
            )
    else:
        logger.info('Not found new or updated items')


def main():
    try:
        while True:
            logger.info('-' * 100)
            logger.info('Start parsing data from sites')
            items = get_items()
            logger.info('Filtering results from sites')
            result = filter_items(items)
            send_email(result)
            time.sleep(600)
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
