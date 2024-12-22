from django.urls import path, include
from rest_framework import routers
from .views import (
    CallsViewSet,
    ContactsViewSet,
    DeletedMessagesViewSet,
    GroupMembersViewSet,
    GroupsViewSet,
    MessagesViewSet,
    SessionsViewSet,
    StatusViewsViewSet,
    StatusesViewSet,
    UsersViewSet,
)

router = routers.DefaultRouter()

router.register(r'calls', CallsViewSet)
router.register(r'contacts', ContactsViewSet)
router.register(r'deleted_messages', DeletedMessagesViewSet)
router.register(r'group_members', GroupMembersViewSet)
router.register(r'groups', GroupsViewSet)
router.register(r'messages', MessagesViewSet, basename='messages')
router.register(r'sessions', SessionsViewSet)
router.register(r'status_views', StatusViewsViewSet)
router.register(r'statuses', StatusesViewSet)
router.register(r'users', UsersViewSet)

urlpatterns = [
    path('', include(router.urls)),
]