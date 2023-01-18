from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField

SKILLS = (('skill_1','Maths'),
          ('skill_2','Data Science'),
          ('skill_3','Programming'),
          ('skill_4','Critical Thinking'),
          ('skill_5','Statistics'),)

TECHNOLOGIES = (('technologies_1','Python'),
          ('technologies_2','Java'),
          ('technologies_3','C/C++'),
          ('technologies_4','Haskell'),
          ('technologies_5','R'),)


class CustomUser(AbstractUser):
    # Define the roles for users
    MANAGER = 1
    GRADUATE = 2
    HR_REP = 3
    
    ROLE_CHOICES = (
        (MANAGER, 'Manager'),
        (GRADUATE, 'Graduate'),
        (HR_REP, 'HR_rep'),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.email}"


class Department(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.name} Department"


class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    managerId = models.AutoField(primary_key=True)
    managerName = models.CharField(max_length=128)


    class Meta:
        verbose_name_plural = 'Managers'
        permissions = (("see_manager", "can see manager page"),)

    def __str__(self):
        return f"{self.managerName} Manager"


class Team(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True, blank=True)
    skills = MultiSelectField(choices=SKILLS)
    technologies = MultiSelectField(choices=TECHNOLOGIES)
    capacity = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.DO_NOTHING)

    class Meta():
        verbose_name_plural = "Teams"

    def __str__(self):
        return f"Name: {self.name}, ID: {self.id}, Capacity: {self.capacity}"


class Graduate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teamId = models.ForeignKey(Team, on_delete=models.DO_NOTHING)

    class Meta():
        verbose_name_plural = "Graduates"
        permissions = (("see_grad", "can see grad page"),)


class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    adminId = models.AutoField(primary_key=True)
    adminName = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Admins'
        permissions = (("see_admin", "can see admin page"),)

    def __str__(self):
        return f"{self.adminName} Admin"

class Preference(models.Model):
    gradId = models.ForeignKey(Graduate, on_delete=models.DO_NOTHING)
    teamId = models.ForeignKey(Team, on_delete=models.DO_NOTHING)
    weight = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
