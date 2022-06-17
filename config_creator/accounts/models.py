from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, forename, surname, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            forename=forename.title(),
            forename=surname.title(),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, forename, surname, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            forename=forename.title(),
            forename=surname.title(),
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, forename, surname, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            forename=forename.title(),
            forename=surname.title(),
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    forename = models.TextField(balnk=False)
    surname = models.TextField(balnk=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "email",
        "forename",
        "surname",
    ]  # Email & Password are required by default.

    def get_full_name(self):
        return f"{self.forename} {self.surname}"

    def get_short_name(self):
        return self.forename

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin
