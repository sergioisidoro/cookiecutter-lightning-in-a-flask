import click
from flask.cli import with_appcontext


@click.group()
def manage():
    """Administration of the flask App"""


@manage.command("create-admin")
@with_appcontext
@click.option('--email', prompt=True)
@click.option('--password', prompt=True)
def create_admin(email, password):
    """Create a new admin user"""
    from bottle.db import db
    from bottle.models import User

    click.echo("Creating...")

    user = User(email=email, password=password, active=True, admin=True)
    db.session.add(user)
    db.session.commit()
    click.echo("Admin created")


if __name__ == "__main__":
    manage()  # pragma: no cover
