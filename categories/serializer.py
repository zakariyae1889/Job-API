from rest_framework.serializers import ModelSerializer

from .models import Categories

class CategoriesSerializers(ModelSerializer):
    class Meta:
        model=Categories
        fields="__all__"

    def create(self, validated_data):
        category=Categories.objects.create(**validated_data)
        return category