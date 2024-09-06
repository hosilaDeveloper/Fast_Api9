from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True)
    email = fields.CharField(max_length=212, unique=True)
    hashed_password = fields.CharField(max_length=212)
    is_active = fields.BooleanField(default=True)

    def __str__(self):
        return self.email
