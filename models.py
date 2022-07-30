# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)
# Unable to inspect table 'django_admin_log'
# The error was: 'DatabaseIntrospection' object has no attribute '_parse_constraint_columns'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Films(models.Model):
    film_id = models.CharField(primary_key=True, max_length=45)
    film_name = models.CharField(max_length=45)
    cover_url = models.CharField(max_length=45)
    release_date = models.CharField(max_length=45)
    film_story = models.CharField(max_length=45)
    film_genre = models.CharField(max_length=45)
    film_censor = models.CharField(max_length=45)
    film_duration = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'films'


class Show(models.Model):
    show_id = models.CharField(max_length=45)
    show_time = models.CharField(max_length=45)
    screen_name = models.CharField(max_length=45)
    show_date = models.CharField(max_length=45)
    price = models.CharField(max_length=45)
    booked_seats = models.CharField(max_length=45)
    available_seats = models.CharField(max_length=45)
    total_seats = models.CharField(max_length=45)
    category_name = models.CharField(max_length=45)
    film_id = models.CharField(max_length=45)
    theatre_code = models.CharField(max_length=45)
    theatre_location = models.CharField(max_length=45)
    last_modified = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'show'
        unique_together = (('show_id', 'category_name'),)


class Track(models.Model):
    track_id = models.AutoField(primary_key=True)
    track_location = models.CharField(max_length=45)
    is_currently_tracking = models.CharField(max_length=45)
    loc_real_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'track'
