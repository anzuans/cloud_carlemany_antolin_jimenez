from tortoise import fields
from tortoise.models import Model

class UserDB(Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(min_length=5, max_length=255, unique=True)
    password = fields.CharField(min_length=5, max_length=255)
    address = fields.CharField(min_length=5, max_length=255, null=True)
