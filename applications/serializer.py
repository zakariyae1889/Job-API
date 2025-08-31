from rest_framework import serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="jobseeker.username", read_only=True)
    email = serializers.CharField(source="jobseeker.email", read_only=True)
    jobName=serializers.CharField(source="job.title",read_only=True)
    companyName=serializers.CharField(source="job.company.name",read_only=True)
    categoryName=serializers.CharField(source="job.category.name",read_only=True)

    class Meta:
        model = Application
        fields = [
            "name", "email", "categoryName","companyName","jobName", 
            "cover_letter", "resume", "status", "applied_at","slug"
        ]
        read_only_fields = ("jobseeker", "job")
    # def create(self, validated_data):
    #   user = self.context["request"].user
    #   return Application.objects.create(jobseeker=user, **validated_data)


class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ["cover_letter", "resume"]