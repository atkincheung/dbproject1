from django.db import models

# Create your models here.

class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.TextField()
    postId = models.IntegerField()
    likes = models.IntegerField()
    user_id = models.IntegerField()
    username = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'listings'

    def __str__(self):
        return f"Comment {self.id} by {self.username}"
