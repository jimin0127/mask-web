from django.db import models

# Create your models here.
class GuestBook(models.Model):
    name = models.CharField(max_length=5)
    phone = models.CharField(max_length = 15)
    message = models.TextField()
    pic = models.ImageField(blank=True, upload_to="images")

    def __str__(self):
        return '{}, {}'.format(self.name, self.message)
