import os
import views
import unittest
import tempfile


class ViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, views.app.config['DATABASE'] = tempfile.mkstemp()
        views.app.testing = True
        self.app = views.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(views.app.config['DATABASE'])

    def test_main(self):
        rv = self.app.get('/')
        assert rv.status_code == 200
        rv = self.app.post('/')
        assert rv.status_code == 405

    def test_get_data_from_mongo(self):
        data = self.app.get('/get_data')
        assert data.status_code == 200
        data = self.app.post('/get_data')
        assert data.status_code == 405
        data = self.app.get('/get_dta')
        print(data.status_code)
        assert data.status_code == 404


if __name__ == '__main__':
    unittest.main()