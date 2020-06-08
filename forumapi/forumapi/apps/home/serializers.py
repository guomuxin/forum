from rest_framework import serializers
from . import models

class BannerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = ['image', 'link', 'is_http']

class NavModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Nav
        fields = ['name', 'link', "son_list", 'is_http', "icon"]
