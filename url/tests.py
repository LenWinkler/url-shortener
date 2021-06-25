from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from account.models import Account

class URLTestCases(APITestCase):

    def test_create_url(self):
        account = Account.objects.create(
            username = 'testuser',
            email = 'test@testing.com',
            password = 'testinguser',
        )
        token = Token.objects.get(user=account)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            "raw": ("https://realpython.com/pypi-publish-python-package/"
                   "#preparing-your-package-for-publication")
            }
        response = client.post('/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_url_no_auth(self):
        data = {
            "raw": ("https://realpython.com/pypi-publish-python-package/"
                   "#preparing-your-package-for-publication")
            }
        response = self.client.post('/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_custom_url(self):
        account = Account.objects.create(
            username = 'testuser',
            email = 'test@testing.com',
            password = 'testinguser',
        )
        token = Token.objects.get(user=account)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            "raw": ("https://realpython.com/pypi-publish-python-package/"
                   "#preparing-your-package-for-publication"),
            "custom": "custom25"
            }
        response = client.post('/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_custom_url_no_auth(self):
        data = {
            "raw": ("https://realpython.com/pypi-publish-python-package/"
                   "#preparing-your-package-for-publication"),
            "custom": "custom25"
            }
        response = self.client.post('/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_visit_url(self):
        account = Account.objects.create(
            username = 'testuser',
            email = 'test@testing.com',
            password = 'testinguser',
        )
        token = Token.objects.get(user=account)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            "raw": "https://rich.readthedocs.io/en/latest/text.html"
            }
        POST_response = client.post('/', data)
        short_url = POST_response.data['short']
        GET_response = self.client.get(short_url)
        self.assertEqual(GET_response.status_code,
                         status.HTTP_301_MOVED_PERMANENTLY)

    def test_no_raw_key(self):
        account = Account.objects.create(
            username = 'testuser',
            email = 'test@testing.com',
            password = 'testinguser',
        )
        token = Token.objects.get(user=account)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            "foo": "https://rich.readthedocs.io/en/latest/text.html"
            }
        response = client.post('/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_existing_url(self):
        account = Account.objects.create(
            username = 'testuser',
            email = 'test@testing.com',
            password = 'testinguser',
        )
        token = Token.objects.get(user=account)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            "raw": ("https://genius.com/"
                   "Gregory-alan-isakov-if-i-go-im-goin-lyrics")
            }
        client.post('/', data)
        second_response = client.post('/', data)
        self.assertIn('Error', second_response.data)

    def test_create_existing_custom_url(self):
        account = Account.objects.create(
            username = 'testuser',
            email = 'test@testing.com',
            password = 'testinguser',
        )
        token = Token.objects.get(user=account)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            "raw": ("https://genius.com/"
                   "The-mountain-goats-game-shows-touch-our-lives-lyrics"),
                   "custom": "gameshow"
            }
        client.post('/', data)
        second_response = client.post('/', data)
        self.assertEqual(second_response.status_code, status.HTTP_409_CONFLICT)

    def test_create_invalid_custom_url(self):
        account = Account.objects.create(
            username = 'testuser',
            email = 'test@testing.com',
            password = 'testinguser',
        )
        token = Token.objects.get(user=account)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        data = {
            "raw": ("https://genius.com/"
                   "Led-zeppelin-going-to-california-lyrics"),
                   "custom": "ThisURLIsTooLong"
            }
        response = client.post('/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    