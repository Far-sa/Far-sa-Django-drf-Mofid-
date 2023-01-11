from django.core import checks
from django.db import models


#! how to define an attribute for a custom field
class OrderField(models.PositiveIntegerField):
    description = "Ordering field on a unique field"

    def __init__(self, unique_for_field=None, *args, **kwargs):
        self.unique_for_field = unique_for_field
        super().__init__(*args, **kwargs)

    def check(self, *args, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_for_field_attribute(*args, **kwargs),
        ]

    def _check_for_field_attribute(self):
        if self.unique_for_field is None:
            return [checks.Error("OrderField must define a 'unique_for_field'")]
        elif self.unique_for_field not in [
            f.name for f in self.model._meta.get_fields()
        ]:
            return [checks.Error("OrderField does not match an existing model field")]

        return []
