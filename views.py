from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from subject.models import Grade, Subject
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


from teacher.forms import ContactUsForm
from teacher.models import EducationQualification, Province, Schedule, Teacher


# Create your views here.
def list_schedules_view(request):
    results = Schedule.objects.all()

    # Filtering results
    grade = request.GET.get("grade")
    if grade:
        results = results.filter(grade__id=grade)

    subject = request.GET.get("subject")
    if subject:
        results = results.filter(subject__id=subject)

    province = request.GET.get("province")
    if province:
        results = results.filter(district__province__id=province)

    education_qualification = request.GET.get("education_qualification")
    if education_qualification:
        results = results.filter(
            teacher__highest_education_qualification__id=education_qualification
        )

    if province:
        results = results.filter(district__province__id=province)

    # Hidden Filters
    class_type = request.GET.get("class_type")
    if class_type:
        results = results.filter(class_type__id=class_type)

    medium = request.GET.get("medium")
    if medium:
        results = results.filter(medium__id=medium)

    grades = Grade.objects.all()

    subjects = Subject.objects.filter(class_type__id=class_type)

    education_qualifications = EducationQualification.objects.all()

    provinces = Province.objects.all()

    minimum_years_of_experience = request.GET.get("min_experience_years")

    if minimum_years_of_experience:
        results = results.filter(
            teacher__years_of_experience__gte=minimum_years_of_experience
        )

    return render(
        request,
        "teacher/available-classes.html",
        context={
            "results": results,
            "grades": grades,
            "subjects": subjects,
            "provinces": provinces,
            "education_qualifications": education_qualifications,
            "experience_years": range(1, 11),
        },
    )


def shedule_details_view(request, id):
    schedule = Schedule.objects.get(id=id)

    return render(
        request, "teacher/schedule-details.html", context={"schedule": schedule}
    )


class ContactUsView(View):
    def get(self, request):
        return render(request, "contact-us.html")

    def post(self, request):
        form = ContactUsForm(request.POST)

        if not form.is_valid():
            return "Invalid Request"

        form.send_mail()

        return HttpResponse("We received your message!")


def teacher_profile_view(request, id):
    try:
        teacher = Teacher.objects.get(id=id)
    except Teacher.DoesNotExist:
        teacher = None

    return render(request, "teacher/profile.html", context={"teacher": teacher})


@method_decorator(csrf_exempt, name="dispatch")
class RateTeacherView(View):
    def post(self, request, id):
        rating = int(request.POST.get("rating"))

        # Check if this user have already voted for this specific teacher
        rated_teachers = request.session.get("rated_teachers_list")

        if rated_teachers is None:
            request.session["rated_teachers_list"] = []
            rated_teachers = []

        if int(id) in rated_teachers:
            return HttpResponse("Sorry, you can only rate a teacher once!")

        teacher = Teacher.objects.get(id=id)
        teacher.add_new_rating(rating)

        rated_teachers.append(int(id))
        request.session["rated_teachers_list"] = rated_teachers

        return HttpResponse(f"Thank you for rating {teacher.name}")
