from rest_framework_gis import serializers
from mine.models import *


class MiningClaimBeaconsSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        fields = {'id','name',}
        geo_field = 'location'
        model = MiningClaimBeacons


class MiningClaimPolygonSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        fields = {'id','name',}
        geo_field = 'location'
        model = MiningClaimPolygon


class MiningClaimLocationSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        fields = {'id','name',}
        geo_field = 'location'
        model = MiningClaimLocation


class MineLocationSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        fields = {'id','name',}
        geo_field = 'location'
        model = MineLocation


class MinePolygonSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        fields = {'id','name',}
        geo_field = 'polygon'
        model = MinePolygon


class MineWorksLocationSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        fields = {'id', 'works', 'quantity', 'comment'}
        geo_field = 'location'
        model = MineWorks


class MineWorksPolygonSerializer(serializers.GeoFeatureModelSerializer):

    class Meta:
        fields = {'id', 'works', 'quantity', 'comment'}
        geo_field = 'polygon'
        model = MineWorks
