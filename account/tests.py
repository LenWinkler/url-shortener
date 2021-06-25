from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class AccountTestCases(APITestCase):

    def test_create_account(self):
        data = {
            'username': 'testaccount',
            'email': 'test@testing.com',
            'password': 'useruser',
            'password2': 'useruser'
        }
        response = self.client.post('/account/api/register', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_account(self):
        data = {
            'username': 'testaccount',
            'email': 'test@testing.com',
            'password': 'useruser',
            'password2': 'useruser'
        }
        client = APIClient()
        POST_response = client.post('/account/api/register', data)
        token = POST_response.data['token']
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        updated_data = {
            'username': 'updatedaccount',
            'email': 'testupdate@testing.com'
        }
        PUT_response = client.put('/account/api/properties/update',
                                    updated_data)
        self.assertEqual(PUT_response.status_code, status.HTTP_200_OK)
        self.assertEqual(PUT_response.data['response'],
                        'account updated successfully')

    def test_delete_account(self):
        data = {
            'username': 'testaccount',
            'email': 'test@testing.com',
            'password': 'useruser',
            'password2': 'useruser'
        }
        client = APIClient()
        POST_response = client.post('/account/api/register', data)
        token = POST_response.data['token']
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        DEL_response = client.delete('/account/api/delete')
        self.assertEqual(DEL_response.status_code, status.HTTP_204_NO_CONTENT)
