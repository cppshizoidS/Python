from django.contrib import admin
from django.urls import path, include
from evernote import views
from evernote.views import RegisterUser, LoginUser, Landing, NoteViewSet, MainPage, NewNotePage, TagAPIView
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt

router = routers.SimpleRouter()
router.register(r'notes', NoteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('evernote/api/', include(router.urls)),
    path('evernote/api/v1/tags', TagAPIView.as_view()),


    path('evernote/main', csrf_exempt(MainPage.as_view()), name='main_page'),

    path('evernote', Landing.as_view(), name='landing_page'),

    path('evernote/registration', RegisterUser.as_view(), name='registration_page'),
    path('evernote/login', LoginUser.as_view(), name='login_page'),
    path('evernote/logout', views.logout_user, name='logout'),
    # #
    path('evernote/add-note', NewNotePage.as_view(), name='add-note_page'),
    #
    path('evernote/download-file/<int:idnote>', views.download_file, name='download-file_page'),
]
