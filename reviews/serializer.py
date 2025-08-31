from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="jobseeker.username", read_only=True)  
    jobName = serializers.CharField(source="job.title", read_only=True)
    companyName = serializers.CharField(source="job.company.name", read_only=True)
    categoryName = serializers.CharField(source="job.category.name", read_only=True)

    class Meta:
        model = Review
        fields = ("categoryName", "jobName", "companyName", "username", "comment", "rating", "created_at")

    def create(self, validated_data):
        jobseeker = self.context["request"].user
        job = validated_data.pop("job")
        return Review.objects.create(jobseeker=jobseeker, job=job, **validated_data)
