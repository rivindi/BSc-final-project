from django.conf import settings
from django.db import models
from django.db.models import Avg

from subject.models import Grade, Subject, TeachingMedium

# Create your models here.


class EducationQualification(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class District(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.name}, {self.province.name}"


class Teacher(models.Model):
    name = models.CharField(max_length=100)
    highest_education_qualification = models.ForeignKey(
        EducationQualification, on_delete=models.PROTECT
    )
    years_of_experience = models.IntegerField()
    working_place = models.CharField(max_length=200)
    contact_mobile = models.IntegerField()
    message_to_students = models.TextField()
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    profile_picture = models.ImageField(
        upload_to="teacher/profilepicture", null=True, blank=True
    )

    avg_rating = models.FloatField(default=0.0, max_length=2)

    def get_profile_picture(self):
        try:
            return self.profile_picture.url
        except ValueError:
            return settings.STATIC_URL + "images/default-teacher-avatar.png"

    def average_rating(self):
        return round(self.avg_rating, 1)

    def add_new_rating(self, rate):
        if rate < 1 or rate > 5:
            return False

        self.rating_set.create(stars=rate)

        # Set new average rating
        new_average = self.rating_set.aggregate(Avg("stars")).get("stars__avg")
        self.avg_rating = new_average

        self.save()

        return True

    def __str__(self) -> str:
        return self.name


class Rating(models.Model):
    stars = models.IntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{str(self.stars)} Star(s) to {self.teacher.name}"


class ClassType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class DayOfWeek(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = "Day of Week"


class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    place = models.CharField(max_length=50, null=False, blank=True)
    day = models.ForeignKey(DayOfWeek, on_delete=models.CASCADE)
    from_time = models.TimeField()
    to_time = models.TimeField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    class_type = models.ForeignKey(ClassType, on_delete=models.CASCADE)
    medium = models.ForeignKey(TeachingMedium, on_delete=models.CASCADE)
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, null=True, blank=True
    )
    held_online = models.BooleanField()

    class Meta:
        ordering = ("-teacher__avg_rating",)
