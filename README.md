# ⚡️⚗️⚡️ Lightning in a Flask
## An oppinionated, production ready and batteries included FLASK SPA (single page application) API backend

## Oppinions
- We use Pipenv. This is controversial, but it's time for a decent package manager in Python and proper version locking to use in production. PDM is nice for isolated environments, but not nice for Docker and executables (like 'flask' executable). Since we don't add requirements that often we can live with the pain of the slow speeds and caching.

- We use postgres. I think by now this shouldn't be an opinion that for most production and long term web development SQL and Postgres are probably the most solid solution.

- Production ready with WSGI, and dev environment with docker-compose.override.

- There has been huge debate about using JWT for session storage. Blacklisting tokens is a bit of a hack to prematurely optimise inserts. Here we go for a full fledged server side session storage in addition to the JWT session management.

- It includes a light-weight permission scheme based on flask-pundit, a port of Ruby's library Pundit

- It includes an administration interface with flask-admin

- It assumes a SaaS like pattern in the API and permissions, where users can only access their own data.

- Oauth / openid connect login and registration takes a strong stance at using PKCE in the frontend to acquire tokens, avoiding backend redirects, or implicit flows. 

## Used libraries
* flask-sqlalchemy - For dabase ORM
* flask-migrate - to manage database migrations
* passlib - For hashing and salting passwords
* flask-smorest - A new and improved version of flask-restfull
* flask-marshmallow - To serialise models
* marshmallow-sqlalchemy - To automatically generate model serialisers
* psycopg2-binary - For the Postgres driver
* flask-jwt-extended - For JWT authentication
* flask-pundit (fork) - For handling permisisons through OOP policies
* flask-admin - For administration platform
* authlib - For OAuth and openId connect token validation and exchange
* requests - Requred by authlib
* flask-cors - For managing CORS headers.

## TODO
- Document PKCE Oauth flows
- Replace flask-pundit by django-rules (despite the name is a general lib)