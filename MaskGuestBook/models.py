from django.db import models

# Create your models here.
class GuestBook(models.Model):
    pic = models.ImageField(upload_to='MaskGuestBook/img/%y')
    name = models.CharField(max_length=5)
    phone = models.CharField(max_length = 15)
    message = models.TextField()

    def __str__(self):
        return '{}, {}'.format(self.name, self.message)
