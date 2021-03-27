from webapp.models import Subject, Course, Tags, Webinar, Video

from rest_framework import serializers


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['id', 'name', 'owner']


class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ['id', 'name', 'owner']


class CourseSerializer(serializers.ModelSerializer):

    subject = SubjectSerializer()

    class Meta:
        model = Course
        fields = ['id', 'number', 'name', 'subject']


class WebinarSerializer(serializers.ModelSerializer):

    subject = SubjectSerializer(many=True)
    tags = TagsSerializer(many=True)
    course = CourseSerializer(many=True)

    class Meta:
        model = Webinar
        fields = ['id', 'title', 'webinar', 'subject', 'tags', 'course']


class VideoSerializer(serializers.ModelSerializer):

    course = CourseSerializer(many=True)
    subject = SubjectSerializer(many=True)
    tags = TagsSerializer(many=True)

    class Meta:
        model = Video
        fields = ['id', 'title', 'video', 'subject', 'course', 'tags']


class PersonalizedSuggestionSerializer(serializers.Serializer):
    videos = VideoSerializer(many=True)
    webinars = WebinarSerializer(many=True)
    current_webinar = WebinarSerializer(many=False)
