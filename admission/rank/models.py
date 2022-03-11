from django.db import models

# Create your models here.


class Program(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return f"{self.name} ({self.code})"


class College(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=256)
    programs = models.ManyToManyField(Program, through="CollegeProgram")

    def __str__(self):
        return f"{self.name} ({self.code})"


class CollegeProgram(models.Model):
    TYPE = (
        (
            "R",
            "Regular",
        ),
        (
            "F",
            "Fullfee",
        ),
    )
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    seats = models.PositiveSmallIntegerField()
    cutin = models.PositiveIntegerField(default=0)
    cutoff = models.PositiveIntegerField(default=0)
    type = models.CharField(choices=TYPE, max_length=1, default="R")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["college", "program", "type"], name="manyToMany"
            )
        ]

    def __str__(self):
        return (
            f"{self.college.code}|{self.program.code}|{self.type} "
            f"(seat={self.seats} | range={self.cutin}-{self.cutoff})"
        )

    def is_valid_range(self):
        return self.cutin < self.cutoff


class Addmission(models.Model):
    GENDER_CHOICES = (
        (
            "M",
            "Male",
        ),
        (
            "F",
            "Female",
        ),
    )

    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=64, null=True)
    last_name = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    batch = models.PositiveSmallIntegerField()
    collegeprogram = models.ForeignKey(CollegeProgram, on_delete=models.CASCADE)

    QUOTA_NORMAL = "NOR"
    QUOTA_DALIT = "DAL"
    QUOTA_FEMALE = "FEM"
    QUOTA_GOVERNMENT = "GOV"
    QUOTA_FOREIGN = "FOR"
    QUOTA_TEACHER_STAFF = "STF"
    QUOTA_FOREIGN = "FOR"
    QUOTA_OTHER = "OTH"
    QUOTA_CHOICES = [
        (QUOTA_NORMAL, "Normal Quota"),
        (QUOTA_DALIT, "Dalit Quota"),
        (QUOTA_FEMALE, "Female Quota"),
        (QUOTA_GOVERNMENT, "Government Quota"),
        (QUOTA_TEACHER_STAFF, "Teacher/Staff Quota"),
        (QUOTA_FOREIGN, "Foreign Quota"),
        (QUOTA_OTHER, "Other"),
    ]

    quota = models.CharField(max_length=3, choices=QUOTA_CHOICES, default=QUOTA_NORMAL)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    rank = models.PositiveIntegerField(null=True)
    district = models.ForeignKey("District", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return (
            f"[{self.rank}] {self.first_name} {self.middle_name} {self.last_name} "
            f"| {self.collegeprogram.college.code} | {self.collegeprogram.program.name} | {self.batch}"
        )


class Zone(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class District(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.zone.name})"
