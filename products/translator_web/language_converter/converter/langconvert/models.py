from django.db import models



class Subscriber(models.Model):
    email = models.EmailField(unique=True)



class Contact(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    category = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


