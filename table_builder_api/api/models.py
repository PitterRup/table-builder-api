from django.db import models


class DynamicTable(models.Model):
    name = models.CharField(max_length=128, unique=True)
    fields = models.JSONField()

    def __str__(self):
        return f'DynamicTable({self.id}, {self.name})'
