from rest_framework import serializers
from .models import Companies
from   authentication.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User

        fields=("first_name","last_name","email")


class CompanySerializer(serializers.ModelSerializer):
    owner=UserSerializer(read_only=True)
    class Meta:
        model=Companies
        fields=("name","email","web","descriptions","owner","slug","created_at","updated_at")

    def create(self,validate_data):
        owner=self.context["request"].user
        return Companies.objects.create(owner=owner,**validate_data)