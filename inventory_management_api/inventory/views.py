from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import InventoryItem, InventoryChangeLog
from .serializers import InventoryItemSerializer, InventoryChangeLogSerializer
from .permissions import IsOwner


class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]

    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['name', 'quantity', 'price', 'date_added']

    def get_queryset(self):
        queryset = InventoryItem.objects.filter(user=self.request.user)

        low_stock = self.request.query_params.get("low_stock")
        if low_stock:
            queryset = queryset.filter(quantity__lt=int(low_stock))

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        old_quantity = self.get_object().quantity
        updated_item = serializer.save()

        if old_quantity != updated_item.quantity:
            InventoryChangeLog.objects.create(
                item=updated_item,
                changed_by=self.request.user,
                old_quantity=old_quantity,
                new_quantity=updated_item.quantity
            )


class InventoryChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InventoryChangeLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryChangeLog.objects.filter(
            item__user=self.request.user
        )
