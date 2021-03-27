from django.contrib import admin
from django.urls import include, path
import webapp.views as views
from rest_framework.routers import DefaultRouter
from rest_framework_extensions.routers import ExtendedSimpleRouter
router = ExtendedSimpleRouter()
router.register(r'subject', views.SubjectViewSet, basename='subject')\
    .register(r'course', views.CourseViewSet, basename='subject-course', parents_query_lookups=['subject_id'])
router.register(r'tags', views.TagViewSet)
router.register(r'webinar', views.WebinarViewSet, basename="webinar")
router.register(r'video', views.VideoViewSet, basename="webinar")

urlpatterns = [
    path('', include(router.urls)),
]