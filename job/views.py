from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.pagination import PageNumberPagination

from .serializer import JobSerializer
from .models import Job, JobHistorySlug
from .filters import JobFilter

from utils.cache.cache_utils import safe_cache_delete, safe_cache_get, safe_cache_set
from permission.Permission import IsEmployee


def get_job_by_slug(slug):
    job = Job.objects.filter(slug=slug).first()
    if not job:
        history_slug = JobHistorySlug.objects.filter(old_slug=slug).first()
        if history_slug:
            job = history_slug.job
    return job


class JobListView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        cache_key = "all_jobs"
        cache_data = safe_cache_get(cache_key)

        if cache_data:
            return Response({"source": "cache", "data": cache_data})

        queryset = Job.objects.all()
        filterset = JobFilter(request.GET, queryset=queryset)
        queryset = filterset.qs

        ordering = request.GET.get("ordering", "-create_at")
        queryset = queryset.order_by(ordering)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = JobSerializer(result_page, many=True)
        safe_cache_set(cache_key, serializer.data, timeout=300)

        return paginator.get_paginated_response(serializer.data)


class JobDetailsView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, slug, *args, **kwargs):
        cache_key = f"job_{slug}_slug"
        cache_data = safe_cache_get(cache_key)

        if cache_data:
            return Response({"source": "cache", "data": cache_data})

        job = get_job_by_slug(slug)
        if not job:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job)
        safe_cache_set(cache_key, serializer.data, timeout=300)

        return Response({"job": serializer.data}, status=status.HTTP_200_OK)


class CreateJobView(APIView):
    permission_classes = [IsEmployee]
    throttle_classes = [ UserRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = JobSerializer(data=request.data, context={"request":request})
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get("title")

        if Job.objects.filter(title__iexact=title).exists():
            return Response({"error": f"Job with title '{title}' already exists"}, status=status.HTTP_400_BAD_REQUEST)

        job = serializer.save()
        safe_cache_delete(f"{request.user.id}")
       
        

        return Response({"message": "Job created successfully", "job": JobSerializer(job).data},
                        status=status.HTTP_201_CREATED)


class UpdateJobView(APIView):
    permission_classes = [IsEmployee]
    throttle_classes = [ UserRateThrottle]

    def patch(self, request, slug, *args, **kwargs):
        job =get_job_by_slug(slug)
        if not job:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        safe_cache_delete(f"{request.user.id}")
       
        safe_cache_delete(f"{slug}")

        return Response({"message": "Job updated successfully", "job": serializer.data}, status=status.HTTP_200_OK)


class JobDeleteView(APIView):
    permission_classes = [IsEmployee]
    throttle_classes = [UserRateThrottle]

    def delete(self, request, slug, *args, **kwargs):
        job = get_job_by_slug(slug)
        if not job:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        safe_cache_delete(f"{request.user.id}")
       
        safe_cache_delete(f"{slug}")
        job.delete()

        return Response({"message": "Job deleted successfully"}, status=status.HTTP_200_OK)
