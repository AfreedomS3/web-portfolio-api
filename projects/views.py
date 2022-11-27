from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.conf import settings
from cloudinary_storage.storage import MediaCloudinaryStorage

from projects import models
from projects import serializers

# Create your views here.
@api_view(['GET'])
def api_root(request, format=None):
    """ Vista para la ruta raíz del API. """
    return Response({
        'tags': reverse('tag-list', request=request, format=format),
        'projects': reverse('project-list', request=request, format=format),
        'jobs': reverse('job-list', request=request, format=format),
        'project-views': reverse('project-views', request=request, format=format)
    })


class TagList(generics.ListCreateAPIView):
    """ Vista para listar y crear tags. """
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Vista para el detalle de cada tag. """
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProjectList(generics.ListCreateAPIView):
    """ Vista para listar y crear proyectos. """
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [JSONParser, FormParser, MultiPartParser]


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Vista para el detalle de cada proyecto. """
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [FormParser, MultiPartParser]

    def destroy(self, request, *args, **kwargs):
        instance = super().get_object()
        
        # Eliminar la imagen del proyecto al ejecutar un delete
        storage_instance = MediaCloudinaryStorage()
        storage_instance.delete(name=instance.thumbnail.name)

        self.perform_destroy(instance)

        return Response(status.HTTP_204_NO_CONTENT)

    def get_object(self, **kwargs):
        project = super().get_object(**kwargs)
        models.ProjectView.objects.create(project=project, ip=self.request.META['REMOTE_ADDR'])
        return project


class JobList(generics.ListCreateAPIView):
    """ Vista para listar y crear experiencias laborales. """
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class JobDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Vista para el detalle de cada experiencia laboral. """
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SiteViewsList(generics.ListCreateAPIView):
    """ Vista para listar y crear visualizaciones. """
    queryset = models.SiteViews.objects.all()
    serializer_class = serializers.SiteViewsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProjectViewList(generics.ListAPIView):
    """ Vista para listar las visualizaciones de los proyectos. """
    queryset = models.ProjectView.objects.all()
    serializer_class = serializers.ProjectViewSerializer
