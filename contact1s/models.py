from django.db import models

# Create your models here.
class Contact(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    class Meta:
        db_table = 'contact1s'

    def __str__(self):
        return f"Contact {self.id} by {self.username}"
