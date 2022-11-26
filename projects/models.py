from django.db import models

# Create your models here.
class Tag(models.Model):
    """ Modelo que almacena los nombres de las tecnologías usadas en un proyecto. """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name



