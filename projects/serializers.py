from rest_framework import serializers
from projects import models

class TagSerializer(serializers.ModelSerializer):
    """ Serializador para los Tags. """
    class Meta:
        model = models.Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    """ Serializador para los proyectos. """
    tags_list = serializers.SerializerMethodField()
    views = serializers.CharField(source='get_views_count', read_only=True)


    class Meta:
        model = models.Project
        fields = ['id', 'title', 'description', 'thumbnail', 'url', 'url_git', 'tags', 'tags_list', 'created', 'views']
        extra_kwargs = {'tags': {'write_only': True}}


    def get_tags_list(self, obj):
        return TagSerializer(instance=obj.tags, many=True).data


class JobSerializer(serializers.ModelSerializer):
    """ Serializador para los datos de experiencia laboral. """
    class Meta:
        model = models.Job
        fields = '__all__'


class SiteViewsSerializer(serializers.ModelSerializer):
    """ Serializador para los datos de las visitas del portafolio. """
    view_count = serializers.IntegerField(default=models.SiteViews.objects.all().count(), read_only=True)

    class Meta:
        model = models.SiteViews
        fields = ['id', 'ip', 'timestamp', 'view_count']


class ProjectViewSerializer(serializers.ModelSerializer):
    """ Serializador para los datos de visitas a un proyecto. """
    class Meta:
        model = models.ProjectView
        fields = '__all__'
        