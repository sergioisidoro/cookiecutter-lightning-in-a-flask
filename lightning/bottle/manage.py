import click
from flask.cli import with_appcontext


@click.group()
def admin():
    """Administration of the flask App"""


@admin.command("create-admin")
@with_appcontext
@click.option('--email', prompt=True)
@click.option('--password', prompt=True)
def create_admin(email, password):
    """Create a new admin user"""
    from bottle.extensions import db
    from bottle.models import User

    click.echo("New admin user setup")

    user = User(email=email, password=password, active=True, admin=True)
    db.session.add(user)
    db.session.commit()
    click.echo("Created admin")


if __name__ == "__main__":
    admin()
