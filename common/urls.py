from django.urls import path
from common.views import unconfirmed_teachers, index

app_name = 'common'
urlpatterns = [
    path('', index, name='index'),
    path('unconfirmed/teachers/', unconfirmed_teachers, name='unconfirmed_teachers')
]
