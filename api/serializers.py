from rest_framework import serializers
from .models import Calls, Contacts, DeletedMessages, GroupMembers, Groups, Messages, Sessions, StatusViews, Statuses, Users


class CallsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calls
        fields = '__all__'


class ContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacts
        fields = '__all__'


class DeletedMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeletedMessages
        fields = '__all__'


class GroupMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembers
        fields = '__all__'


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = '__all__'


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'


class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sessions
        fields = '__all__'


class StatusViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusViews
        fields = '__all__'


class StatusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statuses
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
