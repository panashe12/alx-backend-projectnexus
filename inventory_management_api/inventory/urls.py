from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, InventoryChangeLogViewSet

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet, basename='items')
router.register(r'logs', InventoryChangeLogViewSet, basename='logs')

urlpatterns = router.urls