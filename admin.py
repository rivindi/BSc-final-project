from django.contrib import admin

from teacher.models import (
    ClassType,
    DayOfWeek,
    District,
    EducationQualification,
    Province,
    Rating,
    Schedule,
    Teacher,
)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "grade",
        "subject",
        "from_time",
        "to_time",
        "teacher",
        "held_online",
    )


# Register your models here.
admin.site.register(EducationQualification)
admin.site.register(Province)
admin.site.register(District)
admin.site.register(Teacher)
admin.site.register(Rating)
admin.site.register(ClassType)
admin.site.register(DayOfWeek)
admin.site.register(Schedule, ScheduleAdmin)
