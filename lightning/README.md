## Quickstart
```
docker-compose up
```

## Management commands

* Create administrator user: `docker-compose run webservice flask manage create-admin`

## API
Base route for all resource api endpoints currently registered is `api/v1`

### Login
```
POST /auth/login

{
    'email': 'user@email.com',
    'password': "Hunter2",
}
```
Returns
```
{
      "user_id": 123,
      "access_token": "THE_ACCESS_TOKEN",
      "refresh_token": "REFRESH_TOKEN"
}
```
### Authenticate requests
Include Authorization header as such:
```
Authorization: 'Bearer TOKEN'
```

### Refresh your token
Make a request to the refresh endpoint authenticated with the **refresh token**
```
POST: /auth/refresh
```
will return a new access token. 
```
{"access_token": "NEW_ACCESS_TOKEN"}
```

### Revoke a token (eg. Logout)
Make an authenticated request to 
```
POST: auth/revoke_access
```