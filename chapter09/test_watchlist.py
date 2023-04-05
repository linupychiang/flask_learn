import unittest
from app import app, User, Movie


class WatchListTestCase(unittest.TestCase):

    def setUp(self):
        """
        测试固件，在每个测试方法执行前被调用
        """
        app.config.update({
            'TESTING': True,
            'MONGODB_SETTINGS': {
                'host':
                'mongodb://admin:q12345678@localhost:27017/flask_test?authSource=admin'
            }
        })

        # 创建数据库和表
        user = User(name='test')
        user.set_password('test')
        user.save()
        movie = Movie(title='test_movie', year=2023)
        movie.save()

        # 创建测试客户端、创建测试命令执行器
        self.client = app.test_client()
        self.runner = app.test_cli_runner()

    def tearDown(self):
        """
        测试固件，在每个测试方法执行后被调用
        """
        User.objects(name='test').delete()
        Movie.objects(title='test_movie').delete()
        pass

    def test_app_exist(self):
        """
        测试程序实例是否存在
        """
        self.assertIsNotNone(app)

    def test_app_test(self):
        self.assertTrue(app.config['TESTING'])

    def test_404_page(self):
        response = self.client.get('/no')
        data = response.get_data(as_text=True)
        self.assertIn('page not found', data)
        self.assertIn('go back', data)
        self.assertTrue(response.status_code, 404)

    def test_index_page(self):
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('\'s watchlist', data)
        self.assertEqual(response.status_code, 200)

    # todo: more testcases


if __name__ == "__main__":
    unittest.main()
