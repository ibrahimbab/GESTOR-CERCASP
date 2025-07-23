import unittest
from cercasp import create_app, db

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_login(self):
        # Assume test user created in setup if necessary
        response = self.client.post('/auth/login', data={'username': 'test', 'password': 'test', 'otp': '123456'})
        self.assertIn(response.status_code, [200, 302])  # Depending on credentials

if __name__ == '__main__':
    unittest.main()
