from rest_framework.test import APITestCase
from rest_framework import status

class URLTestCases(APITestCase):

    def test_create_url(self):
        data = {
            "raw": "https://realpython.com/pypi-publish-python-package/" \
                   "#preparing-your-package-for-publication"
            }
        response = self.client.post('/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_custom_url(self):
        data = {
            "raw": "https://realpython.com/pypi-publish-python-package/" \
                   "#preparing-your-package-for-publication",
            "custom": "custom25"
            }
        response = self.client.post('/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_visit_url(self):
        data = {
            "raw": "https://rich.readthedocs.io/en/latest/text.html"
            }
        POST_response = self.client.post('/', data)
        short_url = POST_response.data['short']
        GET_response = self.client.get(short_url)
        self.assertEqual(GET_response.status_code,
                         status.HTTP_301_MOVED_PERMANENTLY)

    def test_no_raw_key(self):
        data = {
            "foo": "https://rich.readthedocs.io/en/latest/text.html"
            }
        response = self.client.post('/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_existing_url(self):
        data = {
            "raw": "https://genius.com/" \
                   "Gregory-alan-isakov-if-i-go-im-goin-lyrics"
            }
        first_response = self.client.post('/', data)
        second_response = self.client.post('/', data)
        self.assertIn('already_exists', second_response.data)

    def test_create_existing_custom_url(self):
        data = {
            "raw": "https://genius.com/" \
                   "The-mountain-goats-game-shows-touch-our-lives-lyrics",
                   "custom": "gameshow"
            }
        first_response = self.client.post('/', data)
        second_response = self.client.post('/', data)
        self.assertEqual(second_response.status_code, status.HTTP_409_CONFLICT)

    def test_create_invalid_custom_url(self):
        data = {
            "raw": "https://genius.com/" \
                   "Led-zeppelin-going-to-california-lyrics",
                   "custom": "ThisURLIsTooLong"
            }
        response = self.client.post('/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_visit_invalid_url(self):
        response = self.client.get('http://127.0.0.1:8000/MadeItUp/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    