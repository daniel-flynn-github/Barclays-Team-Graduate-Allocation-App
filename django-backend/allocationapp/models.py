from django.db import models

# Create your models here.

SKILLS = (('skill_1','Skill Title 1'),
          ('skill_2','Skill Title 2'),
          ('skill_3','Skill Title 3'),
          ('skill_4','Skill Title 4'),
          ('skill_5','Skill Title 5'),)

TECHNOLOGIES = (('technologies_1','Skill Title 1'),
          ('technologies_2','Skill Title 2'),
          ('technologies_3','Skill Title 3'),
          ('technologies_4','Skill Title 4'),
          ('technologies_5','Skill Title 5'),)

class Team(models.Model):
    teamID = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=128)
    teamDescription = models.CharField(max_length = 512, null = True, blank = True)
    teamSkills = models.MultiSelectField(choices=SKILLS)
    teamTechnologies = models.MultiSelectField(choices = TECHNOLOGIES)
    capacity = models.IntegerField()
    department = models.ForeignKey(Department)
    manager = models.ForeginKey(Manager)


    class Meta():
        verbose_name_plural = "Teams"

    def __str__(self):
        return f"Name: {self.teamName}, ID: {self.teamID}, Capacity: {self.capacity}"


class Department(models.Model):
    departmentID = models.AutoField(primary_key=True)
    departmentName = models.CharField(max_length=128)

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.departmentName} Department"

class Allocation(models.Model):
    allocationID = models.AutoField(primary_key=True)
    teamID = models.ForeignKey(Team)
    graduateID = models.OneToOneField(Graduate)

    class Meta:
        verbose_name_plural = 'Allocations'

    def __str__(self):
        return f"{Graduate.objects.get(id=self.graduateID)} has been allocated to {Team.objects.get(id=self.teamID)}"