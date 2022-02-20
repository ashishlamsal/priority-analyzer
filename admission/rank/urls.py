from django.urls import include, path
from rest_framework import routers
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView
from . import views

router = routers.DefaultRouter()
router.register(r"programs", views.ProgramViewSet)
router.register(r"colleges", views.CollegeViewSet)
router.register(r"collegeprograms", views.CollegeProgramViewSet)
router.register(
    r"collegeprogramslist", views.CollegeProgramsListViewSet, "collegeprogramslist"
)
router.register(r"admissions", views.AddmissionViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("prediction/", views.Prediction.as_view()),
    path("analysis/", views.Analysis.as_view()),
    path("rank/", views.Rank.as_view()),
    path("district/", views.DistrictView.as_view()),
    path("zone/", views.ZoneView.as_view()),
    path(
        "openapi/",
        get_schema_view(
            title="BE Rank Analyzer",
            description="API for BE rank and priority analyzer",
            version="1.0.0",
        ),
        name="openapi-schema",
    ),
    path(
        "docs/",
        TemplateView.as_view(
            template_name="rank/docs.html",
            extra_context={"schema_url": "openapi-schema"},
        ),
        name="docs",
    ),
]
