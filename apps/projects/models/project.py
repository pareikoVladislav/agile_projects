from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    files = models.ManyToManyField('ProjectFile', related_name='projects')

    @property
    def count_of_files(self):
        return self.files.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
