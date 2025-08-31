from rest_framework import serializers
from .models import Job
from categories.models import Categories
from compaines.models import Companies
class JobSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)  # للعرض
    company = serializers.CharField(source="company.name", read_only=True) 
    username=serializers.CharField(source="user.username",read_only=True)
    
    category_name = serializers.CharField(write_only=True)
    company_name=serializers.CharField(write_only=True)
   
    
    
    class Meta:
        model = Job
        
        fields = (
            
            "title",
            "category_name",
            "company_name",
            "category",
            "company",
            "username",  
            "experience",
            "location",
            "vacancy",
            "job_nature",
            "salary",
            "description",
            "posted_date",
            "application_date",
            "update_at",
            "slug",
            "logo",
            "create_at",
            "update_at"
        )
    def create(self, validated_data):
        user = self.context["request"].user

        # استخرج الأسماء
        category_name = validated_data.pop("category_name")
        company_name = validated_data.pop("company_name")

        # جلب الـ ForeignKey من الاسم
        category = Categories.objects.get(name=category_name)
        company = Companies.objects.get(name=company_name)

        # إنشاء الـ Job
        job = Job.objects.create(
            user=user,
            category=category,
            company=company,
            **validated_data
        )
        return job

