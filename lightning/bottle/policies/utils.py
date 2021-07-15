import abc
from sqlalchemy.orm import Query


class SQLAlchemyPolicy(metaclass=abc.ABCMeta):
    """
    Class with type annotations so we ensure scopes
    return Queries that can be further filtered, and not,
    for example a list or a single entity
    """

    @abc.abstractmethod
    def scope(self) -> Query:
        pass  # pragma: no cover

