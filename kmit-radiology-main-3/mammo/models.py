from django.db import models


class Mammography(models.Model):
    title = models.CharField(max_length = 25)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='Mammogram/', null=True, blank=True)

    def __str__(self):
        return self.title