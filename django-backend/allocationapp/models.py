from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator, MinValueValidator


class CustomUser(AbstractUser):
    # has ID PK, email, name, last name by default from AbstractUser

    def __str__(self):
        return f"Name:{self.first_name} {self.last_name}, Email:{self.email}"


class Department(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.name} Department"


class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Managers'

    def __str__(self):
        return f"{self.user}"


class Skill(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"Skill: {self.name}"


class Technology(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f"Technology: {self.name}"


class Team(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True, blank=True)
    capacity = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.DO_NOTHING)
    skills = models.ManyToManyField(Skill)
    technologies = models.ManyToManyField(Technology)

    class Meta():
        verbose_name_plural = "Teams"

    def __str__(self):
        return f"Name: {self.name}, ID: {self.id}, Capacity: {self.capacity}"


class Graduate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    assigned_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

    class Meta():
        verbose_name_plural = "Graduates"

    def __str__(self):
        return f"{self.user}"


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Admins'

    def __str__(self):
        return f"{self.user}"


class Preference(models.Model):
    grad = models.ForeignKey(Graduate, on_delete=models.DO_NOTHING)
    team = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    weight = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"Grad: {self.grad.user.email} has a preference of {self.weight} for {self.team.name}"
