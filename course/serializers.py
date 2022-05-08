import datetime
import time
from django.db.models import Avg
from django.utils.text import slugify
from moviepy.video.io.VideoFileClip import VideoFileClip
from rest_framework import serializers
from account.models import User
from course.models import Category, Course, Review, Section, Lesson


################################################################
# Category
################################################################
class CategoryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class CategoryEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


################################################################
# Course
################################################################
class CourseAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ('id', 'teacher', 'students', 'slug', 'last_update')

    def create(self, validated_data):
        validated_data['teacher'] = self.context.get('request').user
        validated_data['slug'] = f"{str(int(time.time()))}-{slugify(validated_data.get('name'))}"
        data = super().create(validated_data)
        return data


class CourseEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ('id', 'teacher', 'students', 'last_update')


class CourseListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'thumbnail', 'name', 'price')


class CourseListByTeacherSerializer(serializers.ModelSerializer):
    students_count = serializers.IntegerField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'students_count')


class TeacherSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'photo', 'rating')

    def get_rating(self, obj):
        stars = Review.objects.filter(course__teacher_id=obj.id).aggregate(rating=Avg('stars'))
        return stars.get('rating')


class CourseSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    teacher = TeacherSerializer()
    price = serializers.SerializerMethodField()
    duration = serializers.IntegerField()
    last_update = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('category', 'teacher', 'name', 'intro_video',
                  'difficulty', 'price', 'last_update', 'student_count', 'duration')

    def get_category(self, obj):
        return obj.category.name

    def get_price(self, obj):
        return f'${obj.price}'

    def get_last_update(self, obj):
        return obj.last_update.strftime("%b %d, %Y")


################################################################
# Review
################################################################
class ReviewAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('course', 'stars', 'comment')

    def create(self, validated_data):
        validated_data['student'] = self.context.get('request').user
        data = super().create(validated_data)
        return data


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('student', 'stars', 'comment')


################################################################
# Section
################################################################
class SectionAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('course', 'name')


class SectionEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('name',)


class SectionSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ('course', 'name')

    def get_course(self, obj):
        return obj.course.name


class SectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name')


class SectionListWithLessonsSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ('id', 'name', 'lessons')

    def get_lessons(self, obj):
        return LessonListSerializer(obj.section.all(), many=True, context={'request': self.context.get('request')}).data


################################################################
# Lesson
################################################################
class LessonAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        exclude = ('id', 'duration')

    def create(self, validated_data):
        video_duration = VideoFileClip(validated_data.get('video').temporary_file_path()).duration
        validated_data['duration'] = int(video_duration)
        data = super().create(validated_data)
        return data


class LessonEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        exclude = ('id', 'duration')

    def update(self, instance, validated_data):
        if validated_data.get('video'):
            video_duration = VideoFileClip(validated_data.get('video').temporary_file_path()).duration
            instance.duration = int(video_duration)
        data = super().update(instance, validated_data)
        return data


class LessonSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        exclude = ('id',)

    def get_section(self, obj):
        return obj.section.name

    def get_duration(self, obj):
        return str(datetime.timedelta(seconds=obj.duration))


class LessonListSerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'video', 'duration')

    def get_duration(self, obj):
        return str(datetime.timedelta(seconds=obj.duration))


################################################################
# Extra
################################################################
class CourseByTeacherSerializer(serializers.ModelSerializer):
    students_count = serializers.IntegerField()

    class Meta:
        model = Course
        fields = ('name', 'students_count')


class TeachersSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'courses')

    def get_courses(self, obj):
        return CourseByTeacherSerializer(obj.teacher.all(), many=True).data
