from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.forms import model_to_dict
from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import generics, status, mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import StaticHTMLRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from . import serializers
from .models import *
from .forms import *


class MainPage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'evernote/main.html'

    def get(self, request):
        if request.user.is_authenticated:
            return Response()
        return redirect('registration_page')


class NewNotePage(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'evernote/new_note.html'

    def get(self, request):
        note_form = AddNoteForm()
        if request.user.is_authenticated:
            return Response({'note_form': note_form})
        else:
            return redirect('registration_page')

    def post(self, request):
        note_form = AddNoteForm(request.POST, request.FILES)
        if request.user.is_authenticated:
            return Response({'note_form': note_form})
        else:
            return redirect('registration_page')


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    # permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Note.objects.filter(person=self.request.user).order_by('-date')
        date = self.request.query_params.get('date')
        tags = self.request.query_params.get('tags')
        if date is not None:
            queryset = queryset.filter(date=date)
        if tags is not None:
            queryset = queryset.filter(tags__name=tags)
        return queryset


class TagAPIView(APIView):
    def get(self, request):
        tags = Tag.objects.all().values()
        return Response({'tags': list(tags)})

    def post(self, request):
        note = Note.objects.get(pk=request.data['note_id'])
        tag, is_exists = Tag.objects.get_or_create(name=request.data['name'])
        if is_exists is False:
            tag.save()
        old_tags = list(Tag.objects.filter(note=note.id))
        new_tags = []
        for old_tag in old_tags:
            new_tags.append(old_tag)
        new_tags.append(tag)
        note.tags.set(new_tags)
        return Response({'post': model_to_dict(tag)})


def download_file(request, idnote: int):
    file = Note.objects.get(pk=idnote).file
    response = HttpResponse(file)
    filename = str(file).rsplit('/', 1)[1]
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


class Landing(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'evernote/index.html'

    def get(self, request):
        return Response()


def logout_user(request):
    logout(request)
    return redirect('landing_page')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'evernote/login.html'

    def get_success_url(self):
        return reverse_lazy('main_page')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'evernote/registration.html'
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main_page')
