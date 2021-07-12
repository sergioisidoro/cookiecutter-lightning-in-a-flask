# ⚡️⚗️⚡️ Lightning in a Flask
## An oppinionated, production ready and batteries included FLASK API backend


## Oppinions
- We use Pipenv. This is controversial, but it's time for a decent package manager in Python and proper version locking to use in production.

- We use postgres. I think by now this shouldn't be an oppinion that for most production and long term web development SQL and Postgres are probably the most solid solution.

- Production ready with WSGI, and dev environment with docker-compose.override.