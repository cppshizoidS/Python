from abc import ABC

from rest_framework import serializers
from django.contrib.auth.models import User
from evernote.models import *


class UserSerializer(serializers.ModelSerializer):
    notes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'notes')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class StringListSerializer(serializers.ListSerializer):
    child = serializers.CharField()


class NoteSerializer(serializers.ModelSerializer):
    person = serializers.HiddenField(default=serializers.CurrentUserDefault())
    tags = StringListSerializer(read_only=True, required=False)

    class Meta:
        model = Note
        fields = ('id', 'person', 'name', 'date', 'text', 'file', 'tags')
