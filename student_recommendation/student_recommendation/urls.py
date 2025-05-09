"""
URL configuration for student_recommendation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recommendations.views import get_student_recommendations
from recommendations.views import get_all_courses, get_all_students, create_new_dummy_data

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/student/<str:student_id>/", get_student_recommendations),
    path("api/all-courses/", get_all_courses),
    path("api/all-students/", get_all_students),
    path('api/reset-dummy-data/', create_new_dummy_data, name='reset_dummy_data'),

]