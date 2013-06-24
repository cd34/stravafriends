import unittest

from pyramid import testing

class ViewTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_index(self):
        from .views import index
        request = testing.DummyRequest()
        info = index(request)
        self.assertIn('<form\n  id="deform"\n  action=""\n  method="POST"\n  enctype="multipart/form-data"\n  accept-charset="utf-8" class="deform">', info['form'])

    def test_friends(self):
        from .views import friends
        request = testing.DummyRequest()
        request.matchdict['id'] = 1
        info = friends(request)
        self.assertEquals(info['id'], 1)
