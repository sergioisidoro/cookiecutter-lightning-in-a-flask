# ⚡️⚗️⚡️ Lightning in a Flask
## An oppinionated, production ready and batteries included FLASK API backend

## Oppinions
- We use Pipenv. This is controversial, but it's time for a decent package manager in Python and proper version locking to use in production. PDM is nice for isolated environemtns, but not nice for Docker and executables (like 'flask' executable). Since we don't add requirements that often we can live with the pain of the slow speeds and caching.

- We use postgres. I think by now this shouldn't be an oppinion that for most production and long term web development SQL and Postgres are probably the most solid solution.

- Production ready with WSGI, and dev environment with docker-compose.override.

- There has been huge debate about using JWT for session storage. Blacklisting tokens is a bit of a hack to prematurely optmisie inserts. Here we go for a full fledged server side session storage in addition to the JWT session management.

- It includes a lightwight permission scheme based on flask-pundit, a port of Ruby's library Pundit

- It includes an administration interface with flask-admin

- It assumes a SaaS like pattern, where users can only access their own data.