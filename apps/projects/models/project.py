from django.db import models


class Project(models.Model):
    name = models.CharField(unique=True, max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    files = models.ManyToManyField('ProjectFile', related_name='project')

    @property
    def count_of_files(self):
        return self.files.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']


class ProjectFile(models.Model):
    file_name = models.CharField(max_length=120)
    file_path = models.FileField(upload_to='documents/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ['-created_at']
