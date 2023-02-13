from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MaxValueValidator, MinValueValidator

class CustomUser(AbstractUser):
    # has ID PK, email, name, last name by default from AbstractUser
    # username = models.CharField(unique=False, blank=True, max_length = 20)
    # email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.email} -> uid: {self.id}"


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
        return f"MANAGER | {self.user}"

class Skill(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        # Needs to be exactly this so it displays in the template properly
        return f"{self.name}"

class Technology(models.Model):
    name = models.CharField(max_length=128)

    class Meta():
        verbose_name_plural = "Technologies"

    def __str__(self):
        # Needs to be exactly this so it displays in the template properly
        return f"{self.name}"

class Team(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True, blank=True)
    capacity = models.IntegerField()
    lower_bound = models.IntegerField(default=1)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank = True)
    technologies = models.ManyToManyField(Technology, blank = True)

    class Meta():
        verbose_name_plural = "Teams"

    def __str__(self):
        return f"'{self.name}' -> teamID: {self.id}"

class Graduate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    assigned_team = models.ForeignKey(Team, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta():
        verbose_name_plural = "Graduates"

    def __str__(self):
        return f"GRADUATE | {self.user}"

class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Admins'

    def __str__(self):
        return f"ADMIN | {self.user}"

class Grad_CSV(models.Model):
    csvfile = models.FileField(upload_to='documents/grad CSVs')

class TeamCSV(models.Model):
    csvfile = models.FileField(upload_to='documents/team CSVs')

class Preference(models.Model):
    grad = models.ForeignKey(Graduate, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    weight = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.grad.user.email} -> {self.weight} votes for {self.team.name}"    
