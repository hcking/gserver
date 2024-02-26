# coding=utf8

import time
import unittest
import pymysql

from data.card import (
    Role,
    Role_MailList,
)

dbconfig = {
    "host": "172.16.16.59",
    "port": 3306,
    "user": "root",
    "passwd": "zhengtu#123.com",
    "db": "atm_test_tzz",
}


class MyConnect(object):
    def __init__(self, host, port, user, passwd, db):
        self.connect = pymysql.connect(host=host, user=user, port=port, db=db, passwd=passwd)
        self.connect.connect()

    def query(self, sql):
        assert isinstance(sql, str)
        with self.connect.cursor() as cur:
            cur.execute(sql)
            res = cur.fetchall()
        return res

    def getAutoIncrement(self, tbl):
        findIndex = 0
        sql = 'show table status where name="{}";'.format(tbl)
        with self.connect.cursor() as cur:
            cur.execute(sql)
            for index, val in enumerate(cur.description):
                if val[0].lower() == "auto_increment":
                    findIndex = index
                    break
            if not findIndex:
                raise ValueError('getAutoIncrement error', tbl)
            res = cur.fetchone()
        return res[findIndex]

    def close(self):
        self.connect.close()
        return


class CattyTest(unittest.TestCase):
    conn = MyConnect(**dbconfig)

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def test_load(self):
        role_id = 204680010  # exist
        res = Role.load(self.conn, role_id=role_id)
        self.assertEqual(res, None, 'load not return')
        role = Role.get('Role_Id_Idx', role_id=role_id)
        if role:
            print('test_load ok')
        # self.assertTrue(role.role_id == role_id)
        return

    def test_change(self):
        role = Role.new(
        )
        role.lv = 20
        self.assertEqual(role.lv, 20)
        with self.assertRaises(Exception):
            role._unknown = 1

        with self.assertRaises(Exception):
            role.role_id = 1

        return

    def test_new(self):
        Role_MailList.load(self.conn, mail_id=137860010)
        nowTime = int(time.time())
        m = Role_MailList.new(
            mail_id=0,
            type=1,
            content="test",
            stime=nowTime,
        )
        self.assertTrue(m)
        self.assertTrue(m.mail_id > 0)
        self.assertEqual(m.type, 1)
        self.assertEqual(m.stime, nowTime)
        self.assertEqual(m.sender_roleid, 0)
        return


if __name__ == '__main__':
    unittest.main()