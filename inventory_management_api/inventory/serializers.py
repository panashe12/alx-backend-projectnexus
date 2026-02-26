from rest_framework import serializers
from .models import InventoryItem, InventoryChangeLog


class InventoryItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryItem
        fields = "__all__"
        read_only_fields = ("user", "date_added", "last_updated")

    def validate(self, data):
        if data["quantity"] < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        if data["price"] <= 0:
            raise serializers.ValidationError("Price must be positive.")
        return data


class InventoryChangeLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = InventoryChangeLog
        fields = "__all__"