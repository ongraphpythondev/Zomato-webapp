from django.db import models

# Create your models here.


class restaurant_model(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='')
    phone = models.IntegerField()
    image = models.ImageField(upload_to='menu_images/')
    address = models.CharField(max_length=200, null=True, blank=True)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name
