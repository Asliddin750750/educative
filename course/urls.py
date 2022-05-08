from django.urls import path

from course.views import CategoryAddView, CategoryEditView, CategoryView, CategoryDeleteView, CategoryListView, \
    CourseAddView, CourseEditView, CourseListView, CourseView, CourseDeleteView, ReviewAddView, ReviewListView, \
    SectionAddView, SectionEditView, SectionView, SectionListView, SectionDeleteView, LessonAddView, LessonEditView, \
    LessonView, LessonListView, LessonDeleteView, TeachersView, CourseListForStudentView, CourseListForTeacherView, \
    SectionListWithLessonsView

app_name = 'course'
urlpatterns = [
    # category
    path('category/add/', CategoryAddView.as_view(), name='category-add'),
    path('category/edit/<int:pk>/', CategoryEditView.as_view(), name='category-edit'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category-get'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category-delete'),
    path('category/list/', CategoryListView.as_view(), name='category-list'),
    # course
    path('add/', CourseAddView.as_view(), name='add'),
    path('edit/<int:pk>/', CourseEditView.as_view(), name='edit'),
    path('list/', CourseListView.as_view(), name='list'),
    path('list/for/student/', CourseListForStudentView.as_view(), name='list-for-student'),
    path('list/for/teacher/', CourseListForTeacherView.as_view(), name='list-for-teacher'),
    path('<int:pk>/', CourseView.as_view(), name='get'),
    path('delete/<int:pk>/', CourseDeleteView.as_view(), name='delete'),
    # review
    path('review/add/', ReviewAddView.as_view(), name='review-add'),
    path('review/list/', ReviewListView.as_view(), name='review-list'),
    # section
    path('section/add/', SectionAddView.as_view(), name='section-add'),
    path('section/edit/<int:pk>/', SectionEditView.as_view(), name='section-edit'),
    path('section/<int:pk>/', SectionView.as_view(), name='section-get'),
    path('section/list/', SectionListView.as_view(), name='section-list'),
    path('section/list/with/lessons/', SectionListWithLessonsView.as_view(), name='section-list-with-lessons'),
    path('section/delete/<int:pk>/', SectionDeleteView.as_view(), name='section-delete'),
    # lesson
    path('lesson/add/', LessonAddView.as_view(), name='lesson-add'),
    path('lesson/edit/<int:pk>/', LessonEditView.as_view(), name='lesson-edit'),
    path('lesson/<int:pk>/', LessonView.as_view(), name='lesson-get'),
    path('lesson/list/', LessonListView.as_view(), name='lesson-list'),
    path('lesson/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson-delete'),
    # extra
    path('teachers/', TeachersView.as_view(), name='teachers')
]

# 1.prefetch
# 2.mp4 (filefield video validator)
# 3.comments
# 4.test all apis
# 5.bazani to'ldirish uchun komanda
# 6.course slug field unique with time.time()
# 7.https://educative-online-platform.herokuapp.com/ bilan solishtirish
# 8.@property
#     def student_count(self):
#         return self.students.count()
