from django.db.models import Prefetch, Count, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.models import User
from config.permissions import IsSuperUser, IsTeacher, IsConfirmedTeacher, IsStudent
from course.models import Category, Course, Review, Section, Lesson
from course.serializers import CategoryAddSerializer, CategoryEditSerializer, CategorySerializer, \
    CategoryListSerializer, CourseAddSerializer, CourseEditSerializer, CourseListSerializer, CourseSerializer, \
    ReviewAddSerializer, ReviewListSerializer, SectionAddSerializer, SectionEditSerializer, SectionSerializer, \
    SectionListSerializer, LessonAddSerializer, LessonEditSerializer, LessonSerializer, LessonListSerializer, \
    TeachersSerializer, CourseListByTeacherSerializer, SectionListWithLessonsSerializer


################################################################
# Category
################################################################
class CategoryAddView(CreateAPIView):
    """
    Kategoriya qo'shish
    """
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategoryAddSerializer


class CategoryEditView(UpdateAPIView):
    """
    Kategoriyani tahrirlash
    """
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategoryEditSerializer


class CategoryView(RetrieveAPIView):
    """
    Id bo'yicha kategoriyani olish
    """
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDeleteView(DestroyAPIView):
    """
    Kategoriyani o'chirish
    """
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = Category.objects.all()


class CategoryListView(ListAPIView):
    """
    Kategoriyalar ro'yxatini olish
    """
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


################################################################
# Course
################################################################
class CourseAddView(CreateAPIView):
    """
    Kurs qo'shish
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]
    queryset = Course.objects.all()
    serializer_class = CourseAddSerializer


class CourseEditView(UpdateAPIView):
    """
    Kursni tahrirlash
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]
    serializer_class = CourseEditSerializer

    def get_queryset(self):
        return Course.objects.filter(teacher_id=self.request.user.id)


class CourseListView(ListAPIView):
    """
    Kurslar ro'yxatini olish
    """
    serializer_class = CourseListSerializer
    queryset = Course.objects.all()


class CourseListForStudentView(ListAPIView):
    """
    Studentning kurslari ro'yxatini olish
    """
    permission_classes = [IsAuthenticated, IsStudent]
    serializer_class = CourseListSerializer

    def get_queryset(self):
        return Course.objects.filter(students=self.request.user)


class CourseListForTeacherView(ListAPIView):
    """
    O'qituvchining kurlari ro'yxatini olish
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]
    serializer_class = CourseListByTeacherSerializer

    def get_queryset(self):
        return Course.objects.filter(teacher=self.request.user).annotate(
            students_count=Count('students')
        )


class CourseView(RetrieveAPIView):
    """
    Id bo'yicha kursni ma'lumotlarini olish
    """
    serializer_class = CourseSerializer

    def get_queryset(self):
        return Course.objects.annotate(duration=Sum('section__section__duration')).prefetch_related(
            Prefetch('category', queryset=Category.objects.only('name')),
            Prefetch('teacher', queryset=User.objects.only('id', 'first_name', 'last_name', 'photo'))
        )


class CourseDeleteView(DestroyAPIView):
    """
    Kursni o'chirish
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]

    def get_queryset(self):
        return Course.objects.filter(teacher_id=self.request.user.id)


################################################################
# Review
################################################################
class ReviewAddView(CreateAPIView):
    """
    Izoh qoldirish va baholash
    """
    permission_classes = [IsAuthenticated, IsStudent]
    queryset = Review.objects.all()
    serializer_class = ReviewAddSerializer


class ReviewListView(ListAPIView):
    """
    Izohlar ro'yxatini olish
    """
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('course',)


################################################################
# Section
################################################################
class SectionAddView(CreateAPIView):
    """
    Kursga bo'lim qo'shish
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]
    queryset = Section.objects.all()
    serializer_class = SectionAddSerializer


class SectionEditView(UpdateAPIView):
    """
    Kurs bo'limini tahrirlash
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]
    serializer_class = SectionEditSerializer

    def get_queryset(self):
        return Section.objects.filter(course__teacher=self.request.user)


class SectionView(RetrieveAPIView):
    """
    Id bo'yicha bo'lim ma'lumotlarini olish
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]
    serializer_class = SectionSerializer

    def get_queryset(self):
        return Section.objects.filter(course__teacher=self.request.user).prefetch_related(
            Prefetch('course', queryset=Course.objects.only('name'))
        )


class SectionListView(ListAPIView):
    """
    Bo'limlar ro'yxatini olish
    """
    queryset = Section.objects.all()
    serializer_class = SectionListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('course',)

    def get_queryset(self):
        return Section.objects.prefetch_related(
            Prefetch('section', queryset=Lesson.objects.all())
        )


class SectionListWithLessonsView(ListAPIView):
    """
    Bo'limlar ro'yxatini lessonlari bilan olish
    """
    serializer_class = SectionListWithLessonsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('course',)

    def get_queryset(self):
        return Section.objects.prefetch_related(
            Prefetch('section', queryset=Lesson.objects.all())
        )


class SectionDeleteView(DestroyAPIView):
    """
    Bo'limni o'chirish
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]

    def get_queryset(self):
        return Section.objects.filter(course__teacher=self.request.user)


################################################################
# Lesson
################################################################
class LessonAddView(CreateAPIView):
    """
    Dars qo'shish
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]
    queryset = Lesson.objects.all()
    serializer_class = LessonAddSerializer


class LessonEditView(UpdateAPIView):
    """
    Dars ma'lumotlarini tahrirlash
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]
    serializer_class = LessonEditSerializer

    def get_queryset(self):
        return Lesson.objects.filter(section__course__teacher=self.request.user)


class LessonView(RetrieveAPIView):
    """
    Id bo'yicha dars ma'lumotlarini olish
    """
    serializer_class = LessonSerializer

    def get_queryset(self):
        return Lesson.objects.prefetch_related(
            Prefetch('section', queryset=Section.objects.only('name'))
        )


class LessonListView(ListAPIView):
    """
    Darslar ro'yxatini olish
    """
    serializer_class = LessonListSerializer
    queryset = Lesson.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('section',)


class LessonDeleteView(DestroyAPIView):
    """
    Darsni o'chirish
    """
    permission_classes = [IsAuthenticated, IsTeacher, IsConfirmedTeacher]

    def get_queryset(self):
        return Lesson.objects.filter(section__course__teacher=self.request.user)


################################################################
# Extra
################################################################
class TeachersView(ListAPIView):
    """
    O'qituvchilar ro'yxati, ularning kurslari va har bir kursdagi studentlar sonini olish
    """
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = TeachersSerializer

    def get_queryset(self):
        return User.objects.filter(job=1).prefetch_related(
            Prefetch('teacher', queryset=Course.objects.annotate(
                students_count=Count('students')
            ))
        )


class BuyCourseView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request, pk):
        if Course.objects.filter(id=pk, students=request.user).exists():
            return Response({
                'data': 'Kursni allaqachon sotib olgansiz'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            course = Course.objects.get(id=pk)
            course.students.add(request.user)
            course.save()
            return Response({
                'data': 'Kursni muvaffaqiyatli sotib oldingiz'
            }, status=status.HTTP_200_OK)
        except:
            return Response({
                'data': 'Kurs topilmadi'
            }, status=status.HTTP_404_NOT_FOUND)
