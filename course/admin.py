from django.contrib import admin

from course.models import Category, Course, Review, Section, Lesson

admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Review)
admin.site.register(Section)
admin.site.register(Lesson)
