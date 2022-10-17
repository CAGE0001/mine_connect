from rest_framework import viewsets
from rest_framework_gis import filters
from .models import *
from .serializers import *


class MineLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MineLocation.objects.filter(location__isnull=False)
    serializer_class = MineLocationSerializer
    bbox_filter_field = 'location'
    filter_backends = (filters.InBBOXFilter, )


class MiningClaimLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MiningClaimLocation.objects.filter(location__isnull=False)
    serializer_class = MiningClaimLocationSerializer
    bbox_filter_field = 'location'
    filter_backends = (filters.InBBOXFilter, )
