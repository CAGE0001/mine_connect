from rest_framework import routers
from .viewsets import *


router = routers.DefaultRouter()
router.register(r"mine_location", MineLocationViewSet)
router.register(r"mining_claim_location", MiningClaimLocationViewSet)

urlpatterns = router.urls