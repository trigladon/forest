from configuration.db import cursor, conn
from application.models.item import Item


class ItemsManager:

    @staticmethod
    def fetch_all():
        sql = f'SELECT * FROM {Item.table_name()}'
        data = ()
        return ItemsManager._fetch_all(sql, data)

    @staticmethod
    def fetch_by_id(id: int):
        sql = f'SELECT * FROM {Item.table_name()} WHERE `id`=?'
        data = (id,)
        return ItemsManager._fetch_one(sql, data)

    @staticmethod
    def fetch_by_site_id(site_id, site: str):
        sql = f'SELECT * FROM {Item.table_name()} WHERE `site_id`=? AND `site`=?'
        data = (site_id, site)
        return ItemsManager._fetch_one(sql, data)

    @staticmethod
    def _fetch_all(sql, data):
        cursor.execute(sql, data)
        result = []
        for data in cursor.fetchall():
            result.append(Item.db_parse(data))
        return result

    @staticmethod
    def _fetch_one(sql, data):
        cursor.execute(sql, data)
        result = None
        data = cursor.fetchone()
        if data:
            result = Item.db_parse(data)
        return result

    @staticmethod
    def save(item: Item):

        if item.id is not None:
            sql = f"UPDATE {Item.table_name()} SET " \
                  f"`title`=?, site_id=?, site=?, price=?, image=?, url=?, update_date=? " \
                  f"WHERE `id`=?"
            data = (
                item.title,
                item.site_id,
                item.site,
                item.price,
                item.image,
                item.url,
                item.update_date,
                item.id
            )
        else:
            sql = f"INSERT INTO {Item.table_name()} " \
                  f"(`title`, `site_id`, `site`, `price`, `image`, `url`, `create_date`, `update_date`)" \
                  f" VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            data = (
                item.title,
                item.site_id,
                item.site,
                item.price,
                item.image,
                item.url,
                item.create_date,
                item.update_date
            )

        ItemsManager._execute_commit(sql, data)

    @staticmethod
    def delete(id):
        sql = f"DELETE FROM {Item.table_name()} WHERE id=?"
        data = (id,)
        ItemsManager._execute_commit(sql, data)

    @staticmethod
    def delete_removed_items(items):
        sql = f"DELETE FROM {Item.table_name()}"
        data = []
        where_sql = ''
        if items:
            where_sql = []
            for item in items:
                where_sql.append(f'(`site_id`!=? AND `site`!=?)')
                data.append(item.site_id)
                data.append(item.site)

            where_sql = " WHERE " + " AND ".join(where_sql)
        sql += where_sql

        ItemsManager._execute_commit(sql, data)

    @staticmethod
    def _execute_commit(sql, data):
        cursor.execute(sql, data)
        conn.commit()

    @staticmethod
    def _execute_many_commit(sql, data):
        cursor.executemany(sql, data)
        conn.commit()
