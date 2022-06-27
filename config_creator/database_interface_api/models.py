from django.db import models
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class ConnectionType(models.Model):
    description = models.CharField(blank=False, unique=True, max_length=250)
    svg = models.FileField(upload_to=f"admin/", blank=True, null=True)

    def __str__(self) -> str:
        return self.description


class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    connectiontype = models.ForeignKey(
        ConnectionType, on_delete=models.CASCADE, verbose_name="Connection Type"
    )
    connectionstring = models.CharField(
        blank=False, unique=False, max_length=250, verbose_name="Connection String"
    )
    name = models.CharField(blank=False, unique=False, max_length=250)
    secret_key = models.CharField(blank=True, unique=True, null=True, max_length=250)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("connection-detail", kwargs={"pk": self.pk})
