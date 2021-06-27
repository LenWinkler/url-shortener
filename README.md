# Url shortener backend

Backend for an app which allows users to register an account and create shortened urls. Built with Django Rest Framework and using DRF's token authentication. I don't know how a URL shortener actually works so this was my attempt to reverse engineer the basic functionality of one. 

###### ***Note: If this was a production app, I'd purchase a shorter domain name to use!***  😁

***For endpoints requiring an auth token, token is passed in header under 'Authorization' with following format:***

```
'token <auth token>'
```

## *User Accounts* endpoints:

#### Register User

``` http
POST shortn-it.herokuapp.com/account/api/register
```

| Parameter   | Type     | Description                         |
| :---------- | :------- | :---------------------------------- |
| `username`  | `string` | **Required**. Username for the user |
| `email`     | `string` | **Required**. Email for the user    |
| `password`  | `string` | **Required**. The user's password   |
| `password2` | `string` | **Required**. Confirm password      |

#### User Login

``` http
POST shortn-it.herokuapp.com/account/api/login
```

| Parameter   | Type     | Description                         |
| :---------- | :------- | :---------------------------------- |
| `username`  | `string` | **Required**. Username for the user |
| `password`  | `string` | **Required**. The user's password   |

#### Get Account Details (*requires auth token*)

``` http
GET shortn-it.herokuapp.com/account/api/properties
```

#### Update User Account (*requires auth token*)

``` http
PUT shortn-it.herokuapp.com/account/api/properties/update
```

| Parameter   | Type     | Description                   |
| :---------- | :------- | :---------------------------- |
| `username`  | `string` | Updated username for the user |
| `email`     | `string` | Updated email for the user    |

#### Delete User (*requires auth token*)

``` http
DELETE shortn-it.herokuapp.com/account/api/delete
```

## *Url endpoints*

#### Create New Url (*requires auth token*)

``` http
POST shortn-it.herokuapp.com
```

| Parameter | Type     | Description                                                  |
| :-------- | :------- | :----------------------------------------------------------- |
| `raw`     | `string` | **Required**. Raw url to be shortened                        |
| `custom`  | `string` | Custom url between 3-8 characters to be used instead of hash |

#### Visit Created Url

``` http
GET shortn-it.herokuapp.com/<url hash>
```

#### Get User's Urls (*requires auth token*)

``` http
GET shortn-it.herokuapp.com/urls
```

#### Delete Url (*requires auth token*)

``` http
DELETE shortn-it.herokuapp.com/delete
```

| Parameter  | Type     | Description                                 |
| :--------- | :------- | :------------------------------------------ |
| `url_hash` | `string` | **Required**. Hash of the url to be deleted |
