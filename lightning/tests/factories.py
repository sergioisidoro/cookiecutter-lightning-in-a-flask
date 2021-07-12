import factory
from bottle.models import User


class UserFactory(factory.Factory):

    email = factory.Sequence(lambda n: "user%d@mail.com" % n)
    password = "mypwd"

    class Meta:
        model = User
