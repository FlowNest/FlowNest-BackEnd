from django.conf import settings
from django.db import models
from django.utils.timezone import localtime
from django.utils import timezone


from .aes import cifrar_mensaje

class Calls(models.Model):
    caller = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    receiver_id = models.IntegerField(blank=True, null=True)
    call_type = models.CharField(max_length=5, blank=True, null=True)
    call_status = models.CharField(max_length=8, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    duration = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'calls'


class Contacts(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    contact = models.ForeignKey('Users', models.DO_NOTHING, related_name='contacts_contact_set', blank=True, null=True)
    alias_name = models.CharField(max_length=50, blank=True, null=True)
    blocked = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contacts'


class DeletedMessages(models.Model):
    message = models.ForeignKey('Messages', models.DO_NOTHING, blank=True, null=True)
    deleted_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='deleted_by', blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deleted_messages'


class GroupMembers(models.Model):
    group = models.ForeignKey('Groups', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    is_admin = models.IntegerField(blank=True, null=True)
    joined_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'group_members'


class Groups(models.Model):
    group_name = models.CharField(max_length=100, blank=True, null=True)
    group_description = models.TextField(blank=True, null=True)
    group_picture = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by', blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'groups'


class Messages(models.Model):
    sender = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    receiver_id = models.IntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=False)
    message_type = models.CharField(max_length=20, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    is_deleted = models.IntegerField(blank=True, null=True)
    media_url = models.CharField(max_length=255, blank=True, null=True)
    is_group_message = models.IntegerField(blank=False, null=False, default=0)

    class Meta:
        managed = False
        db_table = 'messages'

    def save(self, *args, **kwargs):
        # Establecer la hora local antes de guardar el mensaje
        if not self.timestamp:  # Si no hay timestamp asignado, usar la hora local
            self.timestamp = localtime(timezone.now())  # Esto convierte la hora UTC a la hora local

        super().save(*args, **kwargs)
    
class Sessions(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    session_token = models.CharField(max_length=255, blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sessions'


class StatusViews(models.Model):
    status = models.ForeignKey('Statuses', models.DO_NOTHING, blank=True, null=True)
    viewer = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    viewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'status_views'


class Statuses(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    status_type = models.CharField(max_length=20, blank=True, null=True)
    media_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'statuses'


class Users(models.Model):
    phone_number = models.CharField(unique=True, max_length=15, blank=True, null=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.TextField(blank=True, null=True)
    last_seen = models.DateTimeField(blank=True, null=True)
    is_online = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
