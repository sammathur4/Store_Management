from rest_framework import routers
from .views import StoreViewSet

default_router = routers.SimpleRouter()

default_router.register("store", StoreViewSet, basename="store")

urlpatterns = default_router.urls
