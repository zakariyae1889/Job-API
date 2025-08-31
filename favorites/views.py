from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .serializer import FavoriteSerializer
from .models import Favorite
from job.models import Job, JobHistorySlug
from utils.cache.cache_utils import safe_cache_delete, safe_cache_get, safe_cache_set


def get_job_by_slug(slug):
    job = Job.objects.filter(slug=slug).first()
    if not job:
        slug_history = JobHistorySlug.objects.filter(old_slug=slug).first()
        if slug_history:
            job = slug_history.job
    return job


class FavoritListView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        cache_key = f"user-{request.user.id}-favorites"
        cache_data = safe_cache_get(cache_key)

        if cache_data:
            return Response({"source": "cache", "data": cache_data})

        favorites = Favorite.objects.filter(user=request.user).all()
        serializer = FavoriteSerializer(favorites, many=True)
        safe_cache_set(cache_key, serializer.data, timeout=300)
        return Response({"favorites": serializer.data}, status=status.HTTP_200_OK)


class CreateFavoritView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, slug, *args, **kwargs):
        job = get_job_by_slug(slug)

        if not job:
            return Response({"error": "No job found"}, status=status.HTTP_404_NOT_FOUND)

        if Favorite.objects.filter(job=job, user=request.user).exists():
            return Response({"message": "Already in favorites"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = FavoriteSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(job=job)
            safe_cache_delete(f"user-{request.user.id}-favorites")
            safe_cache_delete(f"favorite_{job.slug}_slug")
            return Response({"message": "Favorite created successfully", "favorite": serializer.data}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def patch(self, request, slug, *args, **kwargs):
        job = get_job_by_slug(slug)

        if not job:
            return Response({"error": "No job found"}, status=status.HTTP_404_NOT_FOUND)

        favorite = Favorite.objects.filter(job=job, user=request.user).first()
        if not favorite:
            return Response({"message": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = FavoriteSerializer(favorite, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        safe_cache_delete(f"user-{request.user.id}-favorites")
        safe_cache_delete(f"favorite_{job.slug}_slug")
        return Response({"message": "Favorite updated successfully", "favorite": serializer.data}, status=status.HTTP_200_OK)


class DeleteFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def delete(self, request, slug, *args, **kwargs):
        job = get_job_by_slug(slug)

        if not job:
            return Response({"error": "No job found"}, status=status.HTTP_404_NOT_FOUND)

        favorite = Favorite.objects.filter(job=job, user=request.user).first()
        if not favorite:
            return Response({"message": "Favorite not found"}, status=status.HTTP_404_NOT_FOUND)

        favorite.delete()
        safe_cache_delete(f"user-{request.user.id}-favorites")
        safe_cache_delete(f"favorite_{job.slug}_slug")
        return Response({"message": "Favorite deleted successfully"}, status=status.HTTP_200_OK)
