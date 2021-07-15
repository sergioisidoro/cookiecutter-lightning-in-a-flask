from bottle.manage import create_admin
from bottle.models.user import User


def test_create_admin_management_command(db, app):
    runner = app.test_cli_runner()
    runner.invoke(
        create_admin,
        ['--email', 'cli@admin.com', '--password', 'Hunter2']
    )

    admin_users = User.query.filter_by(email="cli@admin.com", admin=True).all()
    assert len(admin_users) == 1
