import sqlite3
import os
import logging
import datetime
from nonebot import logger

DB_PATH = os.path.expanduser('~/.madao/bot.dao')


class BaseDao(object):
    def __init__(self, table, columns, fields):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._dbpath = DB_PATH
        self._table = table
        self._columns = columns
        self._fields = fields
        self._create_table()

    def _create_table(self):
        sql = "CREATE TABLE IF NOT EXISTS {0} ({1})".format(self._table, self._fields)
        with self._connect() as conn:
            conn.execute(sql)

    def _connect(self):
        return sqlite3.connect(self._dbpath, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)


class UserDao(BaseDao):
    def __init__(self):
        super().__init__(
            table='user',
            columns='uid, name, gli, is_sign',
            fields='''
            uid INT NOT NULL,
            name TEXT NOT NULL,
            gli INT NOT NULL,
            is_sign BOOLEAN NOT NULL,
            PRIMARY KEY (uid)
            ''')

    @staticmethod
    def row2item(r):
        return {'uid': r[0], 'name': r[1], 'gli': r[2], 'is_sign': r[3]} if r else None

    def add(self, user):
        with self._connect() as conn:
            try:
                conn.execute('''
                    INSERT INTO {0} ({1}) VALUES (?, ?, ?, ?, ?)
                    '''.format(self._table, self._columns),
                             (user['uid'], user['name'], user['gli'], user['is_sign']))
            except sqlite3.DatabaseError as e:
                logger.error(f'[UserDao.add] {e}')

    def delete(self, uid):
        with self._connect() as conn:
            try:
                conn.execute('''
                    DELETE FROM {0} WHERE uid=?
                    '''.format(self._table),
                             uid)
            except sqlite3.DatabaseError as e:
                logger.error(f'[UserDao.delete] {e}')

    def modify(self, user):
        with self._connect() as conn:
            try:
                conn.execute('''
                    UPDATE {0} SET name=?, gli=?, is_sign=? WHERE uid=?
                    '''.format(self._table),
                             (user['name'], user['gli'], user['is_sign'], user['uid']))
            except sqlite3.DatabaseError as e:
                logger.error(f'[UserDao.modify] {e}')

    def find_one(self, uid):
        with self._connect() as conn:
            try:
                ret = conn.execute('''
                    SELECT {1} FROM {0} WHERE uid=?
                    '''.format(self._table, self._columns),
                                   uid).fetchone()
                return self.row2item(ret)
            except sqlite3.DatabaseError as e:
                logger.error(f'[UserDao.find_one] {e}')

    def find_all(self):
        with self._connect() as conn:
            try:
                ret = conn.execute('''
                    SELECT {1} FROM {0}
                    '''.format(self._table, self._columns),
                                   ).fetchall()
                return [self.row2item(r) for r in ret]
            except sqlite3.DatabaseError as e:
                logger.error(f'[UserDao.find_all] {e}')

    def find_by(self, gli=None, is_sign=None, uid=None):
        cond_str = []
        cond_tup = []
        if gli is not None:
            cond_str.append('gid=?')
            cond_tup.append(gli)
        if is_sign is not None:
            cond_str.append('cid=?')
            cond_tup.append(is_sign)
        if uid is not None:
            cond_str.append('uid=?')
            cond_tup.append(uid)

        if 0 == len(cond_tup):
            return self.find_all()

        cond_str = " AND ".join(cond_str)

        with self._connect() as conn:
            try:
                ret = conn.execute('''
                    SELECT {1} FROM {0} WHERE {2}
                    '''.format(self._table, self._columns, cond_str),
                                   cond_tup).fetchall()
                return [self.row2item(r) for r in ret]
            except sqlite3.DatabaseError as e:
                logger.error(f'[UserDao.find_by] {e}')

    def delete_by(self, gli=None, is_sign=None, uid=None):
        cond_str = []
        cond_tup = []
        if gli is not None:
            cond_str.append('gid=?')
            cond_tup.append(gli)
        if is_sign is not None:
            cond_str.append('cid=?')
            cond_tup.append(is_sign)
        if uid is not None:
            cond_str.append('uid=?')
            cond_tup.append(uid)

        if 0 == len(cond_tup):
            logger.error(f'[UserDao.delete_by] {"wrong condition to del"}')
            return 0

        cond_str = " AND ".join(cond_str)

        with self._connect() as conn:
            try:
                cur = conn.execute('''
                    DELETE FROM {0} WHERE {1}
                    '''.format(self._table, cond_str),
                                   cond_tup)
                return cur.rowcount
            except sqlite3.DatabaseError as e:
                logger.error(f'[UserDao.delete_by] {e}')


class GroupDao(BaseDao):
    def __init__(self):
        super().__init__(
            table='group',
            columns='gid, dcommand, weibo',
            fields='''
            gid INT NOT NULL,
            dcommand TEXT NOT NULL,
            weibo TEXT NOT NULL,
            PRIMARY KEY (gid)
            ''')

    @staticmethod
    def row2item(r):
        return {'gid': r[0], 'dcommand': r[1], 'weibo': r[2]} if r else None

    def add(self, group):
        with self._connect() as conn:
            try:
                conn.execute('''
                    INSERT INTO {0} ({1}) VALUES (?, ?, ?, ?, ?)
                    '''.format(self._table, self._columns),
                             (group['gid'], group['dcommand'], group['weibo']))
            except sqlite3.DatabaseError as e:
                logger.error(f'[GroupDao.add] {e}')

    def delete(self, gid):
        with self._connect() as conn:
            try:
                conn.execute('''
                    DELETE FROM {0} WHERE gid=?
                    '''.format(self._table),
                             gid)
            except sqlite3.DatabaseError as e:
                logger.error(f'[GroupDao.delete] {e}')

    def modify(self, group):
        with self._connect() as conn:
            try:
                conn.execute('''
                    UPDATE {0} SET dcommand=?, weibo=? WHERE gid=?
                    '''.format(self._table),
                             (group['dcommand'], group['weibo'], group['gid']))
            except sqlite3.DatabaseError as e:
                logger.error(f'[GroupDao.modify] {e}')

    def find_one(self, gid):
        with self._connect() as conn:
            try:
                ret = conn.execute('''
                    SELECT {1} FROM {0} WHERE gid=?
                    '''.format(self._table, self._columns),
                                   gid).fetchone()
                return self.row2item(ret)
            except sqlite3.DatabaseError as e:
                logger.error(f'[GroupDao.find_one] {e}')

    def find_all(self):
        with self._connect() as conn:
            try:
                ret = conn.execute('''
                    SELECT {1} FROM {0}
                    '''.format(self._table, self._columns),
                                   ).fetchall()
                return [self.row2item(r) for r in ret]
            except sqlite3.DatabaseError as e:
                logger.error(f'[GroupDao.find_all] {e}')

    def find_by_blogger(self, blogger):
        with self._connect() as conn:
            try:
                ret = conn.execute('''
                SELECT {1} FROM {0} WHERE weibo LIKE '%{2}%';
                '''.format(self._table, self._columns, blogger),
                                   ).fetchall()
                return [self.row2item(r)['gid'] for r in ret]
            except sqlite3.DatabaseError as e:
                logger.error(f'[GroupDao.find_by_blogger] {e}')
