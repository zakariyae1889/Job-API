from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from permission.Permission import IsEmployee, IsJobSeeker
from .models import  Application,ApplicationSlugHistory
from .serializer import ApplicationSerializer,ApplicationUpdateSerializer
from utils.cache.cache_utils import safe_cache_get, safe_cache_set, safe_cache_delete
from job.models import Job,JobHistorySlug

def get_job_by_slug(slug):
    job = Job.objects.filter(slug=slug).first()
    if not job:
        history_slug = JobHistorySlug.objects.filter(old_slug=slug).first()
        if history_slug:
            job = history_slug.job
    return job

def get_application_by_slug(slug):
    application = Application.objects.filter(slug=slug).first()
    if not application:
        history_slug = ApplicationSlugHistory.objects.filter(old_slug=slug).first()
        if history_slug:
            application = history_slug.application
    return application


class ApplicationListView(APIView):
    permission_classes = [IsJobSeeker]
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        cache_key = f"jobseeker_{request.user.id}_applications"
        cache_data = safe_cache_get(cache_key)
        if cache_data:
            return Response({"source": "cache", "data": cache_data})

        applications = Application.objects.filter(jobseeker=request.user).select_related("job")
        serializer = ApplicationSerializer(applications, many=True)
        safe_cache_set(cache_key, serializer.data, timeout=300)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployeeApplicationListView(APIView):
    permission_classes = [IsEmployee]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        cache_key = f"employee_{request.user.id}_applications"
        cache_data = safe_cache_get(cache_key)
        if cache_data:
            return Response({"source": "cache", "data": cache_data})

        status_filter = request.query_params.get("status")
        applications = Application.objects.filter(job__user=request.user).select_related("job", "jobseeker")

        if status_filter:
            applications = applications.filter(status=status_filter)

        serializer = ApplicationSerializer(applications, many=True)
        safe_cache_set(cache_key, serializer.data, timeout=300)
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployeeApplicationUpdateStatusView(APIView):
    permission_classes = [IsEmployee]
    throttle_classes = [UserRateThrottle]

    def post(self, request, slug, *args, **kwargs):
        application = get_application_by_slug(slug)
        if not application:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get("status")
        if new_status not in ["pending", "accepted", "rejected"]:
            return Response({"message": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        application.status = new_status
        application.save()
        safe_cache_delete(f"employee_{request.user.id}_applications")
        safe_cache_delete(f"application_{slug}_slug")

        return Response({"detail": f"Application status updated to {new_status}"}, status=status.HTTP_200_OK)
    
class JobSeekerApplyView(APIView):
    permission_classes = [IsJobSeeker]
    throttle_classes = [UserRateThrottle]
    def post(self, request, slug, *args, **kwargs):
        job = get_job_by_slug(slug)
        if not job:
            return Response({"error": "No job found to apply for"}, status=status.HTTP_404_NOT_FOUND)
        if Application.objects.filter(job=job, jobseeker=request.user).exists():
            return Response(
                {"detail": "لقد قمت بالتقديم مسبقًا على هذه الوظيفة."},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer=ApplicationSerializer(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save(job=job, jobseeker=request.user)

            safe_cache_delete(f"{request.user.id}")
            safe_cache_delete(f"{slug}")
            return Response({"message":"job-apply created successfully","job-apply": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UpdateJobSeekerApplyView(APIView):
    permission_classes = [IsJobSeeker]
    throttle_classes = [UserRateThrottle]
    
    def patch(self,request,slug,*args, **kwargs):
        application=get_application_by_slug(slug)
        if not application:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer=ApplicationUpdateSerializer(application,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        safe_cache_delete(f"{request.user.id}")
        safe_cache_delete(f"{slug}")
        
        return Response({"message":"job-apply update successfully","job-apply": serializer.data}, status=status.HTTP_200_OK)
    
class DeleteJobSeekerApplyView(APIView):
    permission_classes = [IsJobSeeker]
    throttle_classes = [UserRateThrottle]

    def delete(self,request,slug,*args, **kwargs):
        application=get_application_by_slug(slug)
        
        if not application:
            return Response({"error":"Application not found"},status=status.HTTP_404_NOT_FOUND)
        safe_cache_delete(f"{request.user.id}")
        safe_cache_delete(f"{slug}")

        application.delete()

        return Response({"message":"job-apply delete successfully"}, status=status.HTTP_200_OK)
