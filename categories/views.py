from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .serializer import CategoriesSerializers 
from .filters import CategoryFilter
from .models import Categories, CategoriesHistorySlug
from utils.cache.cache_utils import safe_cache_get, safe_cache_set, safe_cache_delete

def get_category_by_slug(slug):
    category = Categories.objects.filter(slug=slug).first()
    if not category:
        history_slug = CategoriesHistorySlug.objects.filter(old_slug=slug).first()
        if history_slug:
            category = history_slug.category
    return category


class CategoriesListView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        cache_key = "all_categories"
        cache_data = safe_cache_get(cache_key)
        if cache_data:
            return Response({"source": "cache", "data": cache_data})

        queryset = Categories.objects.all()
        filterset = CategoryFilter(request.GET, queryset=queryset)
        queryset = filterset.qs

        ordering = request.GET.get("ordering", "-create_at")
        queryset = queryset.order_by(ordering)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = CategoriesSerializers(result_page, many=True)
        safe_cache_set(cache_key, serializer.data, timeout=300)

        return paginator.get_paginated_response({"CategorysList": serializer.data})


class CategoriesDetailsView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, slug, *args, **kwargs):
        cache_key = f"slug_{slug}_category"
        cache_data = safe_cache_get(cache_key)

        if cache_data:
            return Response({"category": cache_data}, status=status.HTTP_200_OK)

        category = get_category_by_slug(slug)
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriesSerializers(category)
        safe_cache_set(cache_key, serializer.data, timeout=300)

        return Response({"category": serializer.data}, status=status.HTTP_200_OK)


class CreateCategoryView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = CategoriesSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)

        name=serializer.validated_data.get("name")

        if Categories.objects.filter(name=name).exists():
              return Response({"error": f" Category Whit This {name} already exists"},status=status.HTTP_400_BAD_REQUEST)
      

        category = serializer.save()

        # clear cache
        safe_cache_delete(f"{request.user.id}")
       
       

        return Response({
            "message": "Category Created Successfully",
            "category": CategoriesSerializers(category).data
        }, status=status.HTTP_201_CREATED)


class UpdateCategoryView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def patch(self, request, slug, *args, **kwargs):
        category = get_category_by_slug(slug)
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategoriesSerializers(category, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # clear cache
        safe_cache_delete(f"{request.user.id}")
       
        safe_cache_delete(f"{slug}")

        return Response({
            "message": "Update category successfully",
            "category": serializer.data
        }, status=status.HTTP_200_OK)


class DeleteCategoryView(APIView):
    permission_classes = [IsAdminUser]
    throttle_classes = [UserRateThrottle]

    def delete(self, request, slug, *args, **kwargs):
        category = get_category_by_slug(slug)
        if not category:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

        slug = category.slug
        category.delete()

        # clear cache
        safe_cache_delete(f"{request.user.id}")
       
        safe_cache_delete(f"{slug}")

        return Response({"message": "Delete category successfully"}, status=status.HTTP_200_OK)


