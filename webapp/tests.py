from django.test import TestCase
from .models import Room, Message
from .misc import elist_find

class RoomFieldsTest(TestCase):
    def setUp(self):
        Room.objects.create(
            id='test0001',
            edit_code='000111222333444555',
            description='description',
            public_list=False,
            passworded=False,
            password='',
            banned_nk='abc#11223344\x06def#55667788\x06ghi#99001122'
        )
    def test_find_banned_nk_1(self):
        testroom = Room.objects.get(id='test0001')
        self.assertEqual(elist_find(testroom.banned_nk,'abc#11223344'),True)
    def test_find_banned_nk_2(self):
        testroom = Room.objects.get(id='test0001')
        self.assertEqual(elist_find(testroom.banned_nk,'def#55667788'),True)
    def test_find_banned_nk_3(self):
        testroom = Room.objects.get(id='test0001')
        self.assertEqual(elist_find(testroom.banned_nk,'ghi#99001122'),True)
    def test_find_banned_nk_4(self):
        testroom = Room.objects.get(id='test0001')
        self.assertEqual(elist_find(testroom.banned_nk,'jkl#33445566'),False)

