import tornado.testing
import tornado_asunc_serv
import unittest


class TestTornadoApp(tornado.testing.AsyncHTTPSTestCase):
    def get_app(self):
        return tornado_asunc_serv.application

    @tornado.testing.gen_test
    def test_homepage_linc(self):
        client = tornado.testing.AsyncHTTPClient(self.io_loop)
        response = yield client.fetch('/', method='GET')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, 'Hello')
        response = yield client.fetch('/', method='POST')
        self.assertEqual(response.code, 405)

    @tornado.testing.gen_test
    def test_data_linc(self):
        client = tornado.testing.AsyncHTTPClient(self.io_loop)
        response = yield client.fetch('/get_data', method='GET')
        self.assertEqual(response.code, 200)
        response = yield client.fetch('/get_data', method='POST')
        self.assertEqual(response.code, 405)
        response = yield client.fetch('/get_dat', method='GET')
        self.assertEqual(response.code, 404)


if __name__ == '__main__':
    unittest.main()