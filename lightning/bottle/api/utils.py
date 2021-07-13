from bottle.extensions import ma


class AutoSchema(ma.SQLAlchemyAutoSchema):
    """SQLAlchemyAutoSchema override"""

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]
        for name in loadable_fields:
            setattr(obj, name, data.get(name))
