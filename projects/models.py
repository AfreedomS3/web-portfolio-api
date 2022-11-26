from django.db import models

# Create your models here.
class Tag(models.Model):
    """ Modelo que almacena los nombres de las tecnologías usadas en un proyecto. """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


TAG_CHOICES = sorted([(item.id, item.name) for item in Tag.objects.all()], key=lambda tuple: tuple[1])


class Project(models.Model):
    """ Modelo que representa información un proyecto. """
    title = models.CharField(max_length=255)
    description = models.TextField()
    thumbnail = models.ImageField(blank=True, null=True)
    url = models.URLField(max_length=255)
    url_git = models.URLField(max_length=255)
    tags = models.ManyToManyField(Tag, choices=TAG_CHOICES, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def get_views_count(self):
        return self.projectview_set.all().count()

    def __str__(self) -> str:
        return self.title


class Job(models.Model):
    """ Modelo que representa información de experiencia laboral. """
    company = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    description = models.TextField()
    date_from = models.DateField()
    date_to = models.DateField(blank=True, null=True)
    current = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.position} - {self.company}' 


class SiteViews(models.Model):
    """ Modelo que almacena información sobre las vistas que recibe el portafolio. """
    ip = models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.ip


class ProjectView(models.Model):
    """ Modelo que almacena información sobre las vistas que recibe un proyecto. """
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    ip = models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.ip
