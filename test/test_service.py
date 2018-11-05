import unittest

import service

class TestService(unittest.TestCase):

    def setUp(self):

        self.api = service.api().app.test_client()

    def test_item_list(self):

        self.assertEqual(self.api.get("/item").json, service.ITEMS)

    def test_item_retrieve(self):

        self.assertEqual(self.api.get("/item/1").json, service.ITEMS[0])