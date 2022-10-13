from core.models import BigQueryDataType, DEFAULT_DATA_TYPE_ID
from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL

__all__ = [
    "ConnectionType",
    "Connection",
    "Dataset",
    "Table",
    "Column",
]


class ConnectionType(models.Model):
    description = models.CharField(blank=False, unique=True, max_length=250)
    svg = models.FileField(upload_to=f"admin/", blank=True, null=True)

    def __str__(self) -> str:
        return self.description

    def todict(self):
        return {
            "description": self.description,
        }


class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connectiontype = models.ForeignKey(
        ConnectionType,
        on_delete=models.CASCADE,
        verbose_name="Connection Type",
    )
    connectionstring = models.CharField(
        blank=True,
        unique=False,
        max_length=250,
        verbose_name="Connection String",
        null=True,
    )
    credentials = models.FileField(
        verbose_name="Credentials File",
        upload_to=f"credential/",
        blank=True,
        null=True,
    )
    name = models.CharField(
        blank=False,
        unique=False,
        max_length=250,
        verbose_name="Connection Name",
        null=False,
    )
    user_name = models.CharField(
        blank=True,
        unique=False,
        max_length=250,
        verbose_name="User Name",
        null=True,
    )
    host = models.CharField(
        blank=True,
        unique=False,
        max_length=250,
        verbose_name="Host Name",
        null=True,
    )
    sid = models.CharField(
        blank=True,
        unique=False,
        max_length=250,
        verbose_name="SID",
        null=True,
    )
    port = models.IntegerField(
        blank=True, unique=False, verbose_name="Port", null=True, default=0
    )
    schema = models.FileField(
        verbose_name="Schema File",
        upload_to=f"schema/",
        blank=True,
        null=True,
    )
    secret_key = models.CharField(blank=True, unique=True, null=True, max_length=250)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("connection-detail", kwargs={"pk": self.pk})

    def todict(self):
        return {
            "id": self.id,
            "name": self.name,
            "credentials": self.credentials,
            "connection_string": self.connectionstring,
            "user_name": self.user_name,
            "host": self.host,
            "sid": self.sid,
            "port": self.port,
            "schema": self.schema,
            "secret_key": self.secret_key,
            "connection_type": self.connectiontype.todict(),
        }


class Dataset(models.Model):
    connection = models.ForeignKey(
        Connection,
        on_delete=models.CASCADE,
        verbose_name="Project",
    )
    name = models.CharField(
        blank=False,
        unique=False,
        max_length=250,
        verbose_name="Dataset Name",
        null=False,
    )

    def __str__(self):
        return self.name

    def todict(self):
        """
        It takes an object of type `User` and returns a dictionary with the keys `id` and `name` and the
        values of the object's `id` and `name` attributes

        Returns:
          A dictionary with the id and name of the object.
        """
        return {
            "id": self.id,
            "name": self.name,
        }


class Table(models.Model):
    dataset = models.ForeignKey(
        Dataset,
        on_delete=models.CASCADE,
        verbose_name="Dataset",
    )
    name = models.CharField(
        blank=False,
        unique=False,
        max_length=250,
        verbose_name="Table Name",
        null=False,
    )

    def __str__(self):
        return self.name

    def todict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


class Column(models.Model):
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        verbose_name="Table",
    )
    name = models.CharField(
        blank=False,
        unique=False,
        max_length=250,
        verbose_name="Table Name",
        null=False,
    )
    data_type = models.ForeignKey(
        BigQueryDataType,
        verbose_name="Data Type",
        on_delete=models.SET_DEFAULT,
        default=DEFAULT_DATA_TYPE_ID,
        null=False,
        blank=True,
    )
    position = models.IntegerField(
        verbose_name="Ordinal Position",
        null=False,
        blank=True,
        default=-1,
    )
    is_nullable = models.BooleanField(
        verbose_name="Is Column Nullable",
        default=True,
    )

    def __str__(self):
        return self.name

    def todict(self):
        return {
            "id": self.id,
            "table": self.table.todict(),
            "name": self.name,
            "data_type": self.data_type,
            "position": self.position,
            "is_nullable": self.is_nullable,
        }
