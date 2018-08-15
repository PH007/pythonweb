from django.db import models

# Create your models here.
class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image_name = models.CharField(max_length=100)
    image_coordinates = models.TextField()
