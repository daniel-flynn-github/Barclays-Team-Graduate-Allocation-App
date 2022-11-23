from django.db import models

# Create your models here.

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
        return f"{Graduate.objects.get(id=graduateID)} has been allocated to {Team.objects.get(id=teamID)}"



