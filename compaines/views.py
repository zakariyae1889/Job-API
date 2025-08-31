from  rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.pagination import PageNumberPagination
from .serializer import CompanySerializer
from .filters import FilterCompany
from .models import Companies, CompanyHistorySlug
from utils.cache.cache_utils import safe_cache_delete, safe_cache_get, safe_cache_set
from permission.Permission import IsEmployee
from django.db.models import Q


def get_companies_by_slug(slug):
    company = Companies.objects.filter(slug=slug).first()
    if not company:
        history_slug = CompanyHistorySlug.objects.filter(old_slug=slug).first()
        if history_slug:
            company = history_slug.company
    return company


class CompaniesListView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs):
        cache_key = "all_companies"
        cache_data = safe_cache_get(cache_key)

        if cache_data:
            return Response({"source": "cache", "data": cache_data})

        queryset = Companies.objects.all()
        filterset = FilterCompany(request.GET, queryset=queryset)
        queryset = filterset.qs

        ordering = request.GET.get("ordering", "-created_at")
        queryset = queryset.order_by(ordering)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = CompanySerializer(result_page, many=True)
        safe_cache_set(cache_key, serializer.data, timeout=300)

        return paginator.get_paginated_response(serializer.data)


class CompanyDetailsView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, slug, *args, **kwargs):
        cache_key = f"company_{slug}_slug"
        cache_data = safe_cache_get(cache_key)

        if cache_data:
            return Response({"source": "cache", "data": cache_data})

        company = get_companies_by_slug(slug)
        if not company:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySerializer(company)
        safe_cache_set(cache_key, serializer.data, timeout=300)

        return Response({"company": serializer.data}, status=status.HTTP_200_OK)


class CreateCompanyView(APIView):
    permission_classes = [IsEmployee]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = CompanySerializer(data=request.data,context={"request":request})
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get("name")
        email = serializer.validated_data.get("email")

        if Companies.objects.filter(Q(name__iexact=name) | Q(email__iexact=email)).exists():
            return Response(
                {"error": f"Company with name '{name}' or email '{email}' already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        company = serializer.save()
        safe_cache_delete(f"{request.user.id}")
       
        

        return Response({
            "message": "Company Created Successfully",
            "company": CompanySerializer(company).data
        }, status=status.HTTP_201_CREATED)


class UpdateCompanyView(APIView):
    permission_classes = [IsEmployee]
    throttle_classes = [UserRateThrottle]

    def patch(self, request, slug, *args, **kwargs):
        company = get_companies_by_slug(slug)
        if not company:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        safe_cache_delete(f"{request.user.id}")
       
        safe_cache_delete(f"{slug}")

        return Response({
            "message": "Company Updated Successfully",
            "company": serializer.data
        }, status=status.HTTP_200_OK)


class DeleteCompanyView(APIView):
    permission_classes = [IsEmployee]
    throttle_classes = [UserRateThrottle]

    def delete(self, request, slug, *args, **kwargs):
        company = get_companies_by_slug(slug)
        if not company:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

        safe_cache_delete(f"{request.user.id}")
       
        safe_cache_delete(f"{slug}")
        company.delete()

        return Response({"message": "Company Deleted Successfully"}, status=status.HTTP_200_OK)
