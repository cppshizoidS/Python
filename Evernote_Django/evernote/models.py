from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=45, null=False, unique=False)

    def __str__(self):
        return self.name


class Note(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=45, null=False)
    date = models.DateField(auto_now=True, null=False)
    text = models.TextField(null=True)
    file = models.FileField(upload_to='notes_files/', null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    @property
    def name_of_file(self):
        return str(self.file).rsplit('/', 1)[1]

    def __str__(self):
        return self.name


