from rest_framework import viewsets
from .models import Calls, Contacts, DeletedMessages, GroupMembers, Groups, Messages, Sessions, StatusViews, Statuses, Users
from .serializers import CallsSerializer, ContactsSerializer, DeletedMessagesSerializer, GroupMembersSerializer, GroupsSerializer, MessagesSerializer, SessionsSerializer, StatusViewsSerializer, StatusesSerializer, UsersSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Q
from django.conf import settings

from api import aes

class CallsViewSet(viewsets.ModelViewSet):
    queryset = Calls.objects.all()
    serializer_class = CallsSerializer


class ContactsViewSet(viewsets.ModelViewSet):
    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer

    @action(detail=False, methods=['get'])
    def getMyContacts(self, request):
        user_id = request.query_params.get('id', None)
        if user_id is None:
            return Response({'error': 'No está registrado'}, status=status.HTTP_400_BAD_REQUEST)

        contacts = Contacts.objects.filter(user_id=user_id)

        contact_data = []
        for contact in contacts:
            last_message = Messages.objects.filter(
                Q(sender_id=user_id, receiver_id=contact.contact_id) |
                Q(sender_id=contact.contact_id, receiver_id=user_id)
            ).order_by('-timestamp').first()

            contact_info = {
                'contact': ContactsSerializer(contact).data,
                'last_message': MessagesSerializer(last_message).data if last_message else None
            }
            contact_data.append(contact_info)

        if contact_data:
            return Response(contact_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No tiene contactos'}, status=status.HTTP_204_NO_CONTENT)


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
    
    
    

    @action(detail=False, methods=['get'])
    def getMessagesContact(self, request):
        sender_id = request.query_params.get('sender', None)
        receiver_id = request.query_params.get('receiver', None)

        if sender_id is None or receiver_id is None:
            return Response({'error': 'No identificado'}, status=status.HTTP_400_BAD_REQUEST)

        messages = Messages.objects.filter(receiver_id=receiver_id, sender_id=sender_id)

        if messages.exists():
            serialized_messages = self.serializer_class(messages, many=True)
            return Response(serialized_messages.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No tiene contactos'}, status=status.HTTP_204_NO_CONTENT)


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

    def perform_create(self, serializer):
        password = self.request.data.get('password_hash')
        
        if password:
            password_hash_encriptado = aes.cifrar_mensaje(password, settings.ENCRYPTION_KEY)
            serializer.save(password_hash=password_hash_encriptado)
        else:
            serializer.save()

    def create(self, request, *args, **kwargs):
        # Aquí obtenemos el serializer con los datos de la solicitud
        serializer = self.get_serializer(data=request.data)
        
        # Verificamos si los datos son válidos
        if serializer.is_valid():
            self.perform_create(serializer)  # Guardamos el objeto
            return Response({"status": "success"}, status=status.HTTP_201_CREATED)
        else:
            # Si no son válidos, devolvemos los errores en la respuesta
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'])
    def login(self, request):
        phone = request.query_params.get('phone', None)
        password = request.query_params.get('password', None)
        password_hash = aes.cifrar_mensaje(password,settings.ENCRYPTION_KEY)
        user = Users.objects.filter(phone_number=phone, password_hash=password_hash).first()
        if user:
            user.is_online = 1
            user.status = "activo"
            user.save()
            serializer = UsersSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Usuario o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def logout(self, request):
        id = request.query_params.get('id', None)
        user = Users.objects.filter(id=id).first()
        if user:
            user.is_online = 0
            user.status = "inactivo"
            user.last_seen = timezone.now()
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Usuario o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)
