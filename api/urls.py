from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
  
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as get_swagger_view

schema_view=get_swagger_view(
    openapi.Info(
        title="Job Portal API",
        default_version="1.0.0",
        description="API documentation for Job Portal"
    ),
    public=True
)

urlpatterns = [

    path('api/v1/admin/', admin.site.urls),
    path("api/v1/",
        include([

            path('token/', TokenObtainPairView.as_view()),
            path("authentications/",include("authentication.urls")),
            path("categories/",include("categories.urls")),
            path("compaines/",include("compaines.urls")),
            path("jobs/",include("job.urls")),
            path("applications/",include("applications.urls")),
            path("reviews/",include("reviews.urls")),
            path("favorites/",include("favorites.urls")),
            path("swagger/documents/",schema_view.with_ui("swagger",cache_timeout=0),name="swagger-documentation")
        ])
    )

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404="utils.error.errorView.handler404"
handler500="utils.error.errorView.handler500"