import django_filters
from django.db import transaction
from django.db.utils import IntegrityError
from django.db.models import F
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from rest_framework.generics import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets
from rest_framework_extensions.mixins import NestedViewSetMixin
from webapp.models import Subject, User, Course, Tags, Webinar, Video
from webapp.serializers import SubjectSerializer, CourseSerializer, TagsSerializer, WebinarSerializer, \
    VideoSerializer, PersonalizedSuggestionSerializer
from webapp.permissions import IsStudent, IsInstructor, ListAndRetrieve

import os
# Create your views here.


def home(request):
    u = User.objects.get(pk = request.user.pk)
    person = "Student" if u.is_student else "Instructor"
    return HttpResponse("Welcome " + u.username + " as " + person)


class SubjectViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

    def create(self, request, **kwargs):
        request.data['owner'] = request.user.pk
        return super().create(request)


class CourseViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

    @transaction.atomic
    def create(self, request, **kwargs):
        subject_id = self.get_parents_query_dict().get("subject_id")
        subject = get_object_or_404(Subject, pk=subject_id)

        course = Course.objects.create(subject=subject, **request.data)
        return Response(CourseSerializer(course).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["GET"], name="most viewed")
    def mostviewed(self, request, *args, **kwargs):
        return Response(CourseSerializer(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        current_course = self.get_object()
        current_course.viewed = F('viewed') + 1
        current_course.save()
        print("here")

        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        subject_id = self.get_parents_query_dict().get("subject_id")
        if self.action == "mostviewed":
            return Course.objects.filter(subject_id=subject_id).order_by("-viewed")
        if self.action == "list":
            return  Course.objects.filter(subject_id=subject_id)
        return Course.objects.all()

class TagViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [permissions.IsAuthenticated, IsInstructor]

    def create(self, request, **kwargs):
        request.data['owner'] = request.user.pk
        return super().create(request)


class WebinarViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = Webinar.objects.all()
    serializer_class = WebinarSerializer
    permission_classes = [permissions.IsAuthenticated, ListAndRetrieve]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['title', 'tags__name', 'subject__name', 'course__name']

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        request_subjects = eval(self.request.data["subjects"])
        subjects = Subject.objects.filter(id__in=request_subjects)

        request_courses = eval(self.request.data["courses"])
        courses = Course.objects.filter(id__in=request_courses)

        request_tags = eval(self.request.data['tags'])
        del self.request.data['tags']

        webinar = Webinar.objects.create(title=self.request.data['title'],
                                         webinar=self.request.FILES['webinar'])

        request_new_tags = eval(self.request.data['new_tags'])

        new_tags = [Tags(name=n, owner_id=request.user.pk) for n in request_new_tags]

        for new_tag in new_tags:
            try:
                new_tag.save()
            except IntegrityError as e:
                return Response(f"Tag with name '{new_tag.name}' already exists", status=status.HTTP_400_BAD_REQUEST)
            request_tags.append(new_tag.id)

        tags = Tags.objects.filter(id__in=request_tags)
        webinar.tags.set(tags)
        webinar.subject.set(subjects)
        webinar.course.set(courses)

        return Response(WebinarSerializer(webinar).data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):

        obj = self.get_object()
        os.remove(os.path.join(settings.MEDIA_ROOT, str(obj.webinar)))

        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):

        current_webinar = self.get_object()
        current_webinar.viewed = F('viewed') + 1
        current_webinar.save()
        webinars = Webinar.objects.filter(tags__name__in=current_webinar.tags.values('name')).order_by("-viewed")[:5]

        videos = Video.objects.filter(tags__name__in=current_webinar.tags.values('name')).order_by("-viewed")[:5]
        suggestions = {'current_webinar': WebinarSerializer(current_webinar).data,
                       'webinars': WebinarSerializer(webinars, many=True).data,
                       'videos': VideoSerializer(videos, many=True).data}

        return JsonResponse(suggestions, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], name="most viewed")
    def mostviewed(self, request, *args, **kwargs):
        return Response(WebinarSerializer(self.get_queryset(), many=True).data, status=status.HTTP_200_OK)
        # return Response("hello", status=status.HTTP_200_OK)

    def get_queryset(self):
        if self.action == "mostviewed":
            return Webinar.objects.all().order_by('viewed').reverse()

        return Webinar.objects.all()


class VideoViewSet(NestedViewSetMixin, viewsets.ModelViewSet):

    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated, ListAndRetrieve]

    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['title', 'tags__name', 'subject__name', 'course__name']

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        request_subjects = eval(self.request.data["subjects"])
        subjects = Subject.objects.filter(id__in=request_subjects)

        request_courses = eval(self.request.data["courses"])
        courses = Course.objects.filter(id__in=request_courses)

        request_tags = eval(self.request.data['tags'])
        del self.request.data['tags']

        video = Video.objects.create(title=self.request.data['title'],
                                        video=self.request.FILES['video'])

        request_new_tags = eval(self.request.data['new_tags'])

        new_tags = [Tags(name=n, owner_id=request.user.pk) for n in request_new_tags]

        # We can create tags in bulk but in django bulk_create has error. it does not
        # return id once it creates. However bulk_create works with postgresql.

        for new_tag in new_tags:
            try:
                new_tag.save()
            except IntegrityError as e:
                return Response(f"Tag with name '{new_tag.name}' already exists", status=status.HTTP_400_BAD_REQUEST)
            request_tags.append(new_tag.id)

        tags = Tags.objects.filter(id__in=request_tags)
        video.tags.set(tags)
        video.subject.set(subjects)
        video.course.set(courses)

        return Response(VideoSerializer(video).data, status=status.HTTP_201_CREATED)

