from django.db import models
# Create your models here.

class GuestBookModel(models.Model):
    name = models.CharField(max_length=5)
    phone = models.CharField(max_length=15)
    message = models.TextField()
    image_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.image_name