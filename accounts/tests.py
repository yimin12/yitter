import sre_parse

from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

LOGIN_URL = '/api/accounts/login/'
LOGOUT_URL = '/api/accounts/logout'
SIGNUP_URL = '/api/accounts/signup'
LOGIN_STATUS_URL = '/api/accounts/login_status/'

# Create your tests here.
class AccountApiTests(TestCase):

    def setUp(self):
        ## set up in unit test
        self.client = APIClient()
        self.user = self.createUser(
            username='admin',
            email='admin@yitter.com',
            password='admin',
        )

    def createUser(self, username, email, password):
        ## Could not use User.objects.create() directly, we should encrypt password and do normalization
        return User.objects.create_user(username, email, password)

    ## every test method's name should start with test_
    def test_login(self):
        # test get rather than post, get 400
        response = self.client.get(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password',
        })
        # assert fail, 405 = METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, 405)
        # test post with wrong password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'wrong password',
        })
        self.assertEqual(response.status_code, 400)
        # validate not login
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)
        # validate the correct password
        response = self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': 'correct password',
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['user'], None)
        self.assertEqual(response.data['user']['email'], "admin@yitter.com")
        ## validate that has logined
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)

    def test_logout(self):
        # login first
        self.client.post(LOGIN_URL, {
            'username': self.user.username,
            'password': self.user.password,
        })
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)
        # test get rather than post
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 405)
        # test post
        response = self.client.post(LOGIN_URL)
        self.assertEqual(response.status_code, 200)
        # test user that is logout
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], False)

    def test_signup(self):
        data = {
            'username': 'someone',
            'email': 'someone@jiuzhang.com',
            'password': 'any password',
        }
        # test get failure
        response = self.client.get(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 405)

        # try wrong email
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'not a correct email',
            'password': 'any password'
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # test password that is too short
        response = self.client.post(SIGNUP_URL, {
            'username': 'someone',
            'email': 'someone@jiuzhang.com',
            'password': '123',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        #  test password that is too long
        response = self.client.post(SIGNUP_URL, {
            'username': 'username is tooooooooooooooooo loooooooong',
            'email': 'someone@jiuzhang.com',
            'password': 'any password',
        })
        # print(response.data)
        self.assertEqual(response.status_code, 400)

        # test register successfully
        response = self.client.post(SIGNUP_URL, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['user']['username'], 'someone')
        # validate login successfully
        response = self.client.get(LOGIN_STATUS_URL)
        self.assertEqual(response.data['has_logged_in'], True)