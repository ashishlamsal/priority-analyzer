from django.db import models

# Create your models here.
class Program(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=3)

    def __str__(self):
        return f"{self.name} ({self.code})"


class College(models.Model):
    name = models.CharField(max_length=256)
    code = models.CharField(max_length=3)
    programs = models.ManyToManyField(Program, through='CollegeProgram')

    def __str__(self):
        return f"{self.name} ({self.code})"


class CollegeProgram(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    seat = models.PositiveSmallIntegerField()
    cutoff = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.college.code}, {self.program} -- NoOfSeat={self.seat}"


class Student(models.Model):
    QUOTA_REGULAR = 'RE'
    QUOTA_OTHER = 'OT'
    QUOTA_CHOICES = [
        (QUOTA_REGULAR, 'Regular'),
        (QUOTA_OTHER, 'Other'),
    ]

    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male', ),
        (GENDER_FEMALE, 'Female', ),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
    )
    details = models.ForeignKey(CollegeProgram, on_delete=models.CASCADE)
    batch = models.PositiveSmallIntegerField()
    rank = models.PositiveIntegerField()
    score = models.DecimalField(max_digits=5, decimal_places=2)
    quota = models.CharField(
        max_length=2,
        choices=QUOTA_CHOICES,
        default=QUOTA_REGULAR,
    )

    def __str__(self):
        return f"[{self.rank}] {self.first_name} {self.last_name} ({self.details.college.code} {self.details.program.name}/{self.batch})"
