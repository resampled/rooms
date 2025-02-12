from django.test import TestCase
from .models import Room, Message
from .misc import elist_find
from . import namekeys

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

class NameKeysTest(TestCase):
    name_valid1 = 'abcdefg'
    name_invalid1 = 'abcd#efg'
    name_invalid2 = 'foo\x06bar'
    key_valid1 = '123456789'
    key_invalid1 = '12345\x066789'    
    nk_valid1 = 'abcdefg#1234567'
    nk_to_hash = 'foo#bar'
    def test_name_and_key_to_nk_valid(self):
        self.assertEqual(namekeys.generate_nk_combo(self.name_valid1,self.key_valid1),'abcdefg#123456789')
    def test_name_and_key_to_nk_invalid1(self):
        self.assertEqual(namekeys.generate_nk_combo(self.name_invalid1,self.key_valid1),'0')
    def test_name_and_key_to_nk_invalid2(self):
        self.assertEqual(namekeys.generate_nk_combo(self.name_invalid2,self.key_valid1),'0')
    def test_name_and_key_to_nk_invalid3(self):
        self.assertEqual(namekeys.generate_nk_combo(self.name_valid1,self.key_invalid1),'0')
    def test_decouple_nk_to_name(self):
        self.assertEqual(namekeys.decouple_nk_to_name(self.nk_valid1),'abcdefg')
    def test_hash_nk_full(self):
        self.assertEqual(namekeys.hash_nk(self.nk_to_hash),'88DFx2E7RbuBfq_ze_8hxjKu5QlZ2QTmGqn0RAWXFZQ=')
    def test_hash_nk_trunc(self):
        self.assertEqual(namekeys.hash_nk_trunc(self.nk_to_hash),'88DFx2E7Rb..')




