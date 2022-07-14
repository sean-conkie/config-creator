from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL

__all__ = [
    "ConnectionType",
    "Connection",
]


class ConnectionType(models.Model):
    description = models.CharField(blank=False, unique=True, max_length=250)
    svg = models.FileField(upload_to=f"admin/", blank=True, null=True)

    def __str__(self) -> str:
        return self.description


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
        verbose_name="Project Name",
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
