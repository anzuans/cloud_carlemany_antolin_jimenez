from tortoise import fields
from tortoise.models import Model


class FileDB(Model):
    """File model for database persistence."""

    id = fields.IntField(pk=True)
    title = fields.CharField(min_length=1, max_length=255)
    description = fields.CharField(min_length=0, max_length=500, default="")
    content = fields.TextField(default="")
    user_id = fields.IntField()  # Reference to user from authentication app
