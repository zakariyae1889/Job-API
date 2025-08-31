from rest_framework import serializers


from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    jobseeker=serializers.CharField(source="user.username",read_only=True)
    jobtitle=serializers.CharField(source="job.title",read_only=True)
    companyname=serializers.CharField(source="job.company.name",read_only=True)
    categoryname=serializers.CharField(source="job.category.name",read_only=True)

    class Meta:
        model=Favorite
        fields=("jobseeker","jobtitle","companyname","categoryname","added_at")
    
    def create(self,validated_data):
        user=self.context["request"].user

        favorite=Favorite.objects.create(user=user, **validated_data)

        return favorite