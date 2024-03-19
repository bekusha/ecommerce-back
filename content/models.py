from django.db import models

class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return self.title

class ContactPage(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.title
