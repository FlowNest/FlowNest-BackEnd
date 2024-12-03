from rest_framework import viewsets
from .models import Calls, Contacts, DeletedMessages, GroupMembers, Groups, Messages, Sessions, StatusViews, Statuses, Users
from .serializers import CallsSerializer, ContactsSerializer, DeletedMessagesSerializer, GroupMembersSerializer, GroupsSerializer, MessagesSerializer, SessionsSerializer, StatusViewsSerializer, StatusesSerializer, UsersSerializer

class CallsViewSet(viewsets.ModelViewSet):
    queryset = Calls.objects.all()
    serializer_class = CallsSerializer


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer


class DeletedMessagesViewSet(viewsets.ModelViewSet):
    queryset = DeletedMessages.objects.all()
    serializer_class = DeletedMessagesSerializer


class GroupMembersViewSet(viewsets.ModelViewSet):
    queryset = GroupMembers.objects.all()
    serializer_class = GroupMembersSerializer


class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Groups.objects.all()
    serializer_class = GroupsSerializer


class MessagesViewSet(viewsets.ModelViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer


class SessionsViewSet(viewsets.ModelViewSet):
    queryset = Sessions.objects.all()
    serializer_class = SessionsSerializer


class StatusViewsViewSet(viewsets.ModelViewSet):
    queryset = StatusViews.objects.all()
    serializer_class = StatusViewsSerializer


class StatusesViewSet(viewsets.ModelViewSet):
    queryset = Statuses.objects.all()
    serializer_class = StatusesSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
