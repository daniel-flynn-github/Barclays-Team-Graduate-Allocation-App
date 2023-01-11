from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.email



# class Department(models.Model):
#     departmentID = models.AutoField(primary_key=True)
#     departmentName = models.CharField(max_length=128)

#     class Meta:
#         verbose_name_plural = 'Departments'

#     def __str__(self):
#         return f"{self.departmentName} Department"

# SKILLS = (('skill_1','Skill Title 1'),
#           ('skill_2','Skill Title 2'),
#           ('skill_3','Skill Title 3'),
#           ('skill_4','Skill Title 4'),
#           ('skill_5','Skill Title 5'),)

# TECHNOLOGIES = (('technologies_1','Skill Title 1'),
#           ('technologies_2','Skill Title 2'),
#           ('technologies_3','Skill Title 3'),
#           ('technologies_4','Skill Title 4'),
#           ('technologies_5','Skill Title 5'),)

# # class Team(models.Model):
# #     teamID = models.AutoField(primary_key=True)
# #     teamName = models.CharField(max_length=128)
# #     teamDescription = models.CharField(max_length = 512, null = True, blank = True)
# #     #teamSkills = models.MultiSelectField(choices=SKILLS)
# #     #teamTechnologies = models.MultiSelectField(choices = TECHNOLOGIES)
# #     capacity = models.IntegerField()
# #     department = models.ForeignKey(Department)
# #     #manager = models.ForeignKey(Manager)


# #     class Meta():
# #         verbose_name_plural = "Teams"

# #     def __str__(self):
# #         return f"Name: {self.teamName}, ID: {self.teamID}, Capacity: {self.capacity}"


class Admin(CustomUser):
    adminID = models.AutoField(primary_key=True)
    adminName = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Admins'

    def __str__(self):
        return f"{self.adminName} Admin"



