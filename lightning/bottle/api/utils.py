from bottle.extensions import ma


class AutoSchema(ma.SQLAlchemyAutoSchema):
    """SQLAlchemyAutoSchema override"""

    def update(self, obj, data):
        """Update object nullifying missing data"""
        loadable_fields = [
            k for k, v in self.fields.items() if not v.dump_only
        ]

        provided_values = [
            k for k, v in data.items()
        ]

        fields_to_load = list(set(loadable_fields) & set(provided_values))

        for name in fields_to_load:
            setattr(obj, name, data.get(name))
