from tortoise import fields
from tortoise.models import Model


class FileDB(Model):
    """File metadata model for database persistence."""

    id = fields.IntField(pk=True)
    title = fields.CharField(min_length=1, max_length=255)
    description = fields.CharField(max_length=500, null=True)
    content_path = fields.CharField(max_length=500, null=True)
    original_filename = fields.CharField(max_length=255, null=True)
    user_id = fields.IntField()
