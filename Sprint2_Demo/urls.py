from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from Sprint2 import views

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  path("", views.Home.as_view()),
  path(r"main/index.html", views.Home.as_view(), name='home'),
  path(r"main/login.html", views.Login.as_view(), name='login'),
  path(r"logout", views.Logout.as_view(), name='logout'),
  path(r"courses", views.Classes.as_view()),
  path(r"sections", views.Sections.as_view()),
  path(r"users", views.Users.as_view()),
  path(r"passwordchange", views.FormInput.as_view()),
  path(r"createuser", views.FormInput.as_view()),
  path(r"createcourse", views.FormInput.as_view()),
  path(r"createsection", views.FormInput.as_view()),
  path(r"contactinfo", views.FormInput.as_view()),
  path(r"taprefs", views.FormInput.as_view()),
  path(r"taAddSchedule", views.FormInput.as_view()),
  path(r"taDelSchedule", views.DeleteEnroll.as_view()),
  path(r"tatocourse", views.FormInput.as_view()),
  path(r"instructortocourse", views.FormInput.as_view()),
  path(r"tatosection", views.AssignTA.as_view()),
  path(r"viewTaQual", views.viewTaQual.as_view()),
  path(r"viewconflicts", views.ViewConflicts.as_view()),
  path(r"deluser", views.DelUser.as_view()),
  path(r"reset", views.Reset.as_view()),
]
