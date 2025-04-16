from django.contrib.messages import success
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from departments_app.models import Department, School, Subject


@require_GET
def list_departments(request: HttpRequest) -> HttpResponse:
    schools = School.objects.all()
    return render(
        request,
        f"{__package__}/{list_departments.__name__}.html",
        {
            "schools": schools,
        },
    )


@require_http_methods(["GET", "POST"])
def create_school(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        school = School.objects.create(
            name=request.POST["name"],
        )
        success(request, f"Created {school}.")
        return redirect(list_departments.__name__)
    return render(request, f"{__package__}/{create_school.__name__}.html")


@require_http_methods(["GET", "POST"])
def edit_school(request: HttpRequest, uuid: str) -> HttpResponse:
    school = get_object_or_404(School, uuid=uuid)
    if request.method == "POST":
        school.name = request.POST["name"]
        school.save()
        success(request, f"Saved changes to {school}.")
        return redirect(list_departments.__name__)
    return render(
        request,
        f"{__package__}/{edit_school.__name__}.html",
        {
            "school": school,
        },
    )


@require_POST
def delete_school(request: HttpRequest, uuid: str) -> HttpResponse:
    school = get_object_or_404(School, uuid=uuid)
    name = school.name
    school.delete()
    success(request, f"Deleted {name}.")
    return redirect(list_departments.__name__)


@require_http_methods(["GET", "POST"])
def create_department(request: HttpRequest) -> HttpResponse:
    try:
        school = School.objects.get(uuid=request.GET["school"])
    except KeyError:
        school = None
    if request.method == "POST":
        department = Department.objects.create(
            name=request.POST["name"],
            school=School.objects.get(uuid=request.POST["school"]),
        )
        success(request, f"Created {department}.")
        return redirect(list_departments.__name__)
    return render(
        request,
        f"{__package__}/{create_department.__name__}.html",
        {
            "schools": School.objects.all(),
            "school": school,
        },
    )


@require_http_methods(["GET", "POST"])
def edit_department(request: HttpRequest, uuid: str) -> HttpResponse:
    department = get_object_or_404(Department, uuid=uuid)
    if request.method == "POST":
        department.name = request.POST["name"]
        department.school = School.objects.get(uuid=request.POST["name"])
        department.save()
        success(request, f"Saved changes to {department}.")
        return redirect(list_departments.__name__)
    return render(
        request,
        f"{__package__}/{edit_department.__name__}.html",
        {
            "department": department,
            "schools": School.objects.all(),
        },
    )


@require_POST
def delete_department(request: HttpRequest, uuid: str) -> HttpResponse:
    department = get_object_or_404(Department, uuid=uuid)
    name = department.name
    department.delete()
    success(request, f"Deleted {name}.")
    return redirect(list_departments.__name__)


@require_http_methods(["GET", "POST"])
def create_subject(request: HttpRequest) -> HttpResponse:
    try:
        department = Department.objects.get(uuid=request.GET["department"])
    except KeyError:
        department = None
    if request.method == "POST":
        subject = Subject.objects.create(
            name=request.POST["name"],
            code=request.POST["code"],
            department=Department.objects.get(uuid=request.POST["department"]),
        )
        success(request, f"Created {subject}.")
        return redirect(list_departments.__name__)
    return render(
        request,
        f"{__package__}/{create_subject.__name__}.html",
        {
            "departments": Department.objects.all(),
            "department": department,
        },
    )


@require_http_methods(["GET", "POST"])
def edit_subject(request: HttpRequest, uuid: str) -> HttpResponse:
    subject = get_object_or_404(Subject, uuid=uuid)
    if request.method == "POST":
        subject.name = request.POST["name"]
        subject.code = request.POST["code"]
        subject.department = Department.objects.get(uuid=request.POST["department"])
        subject.save()
        success(request, f"Saved changes to {subject}.")
        return redirect(list_departments.__name__)
    return render(
        request,
        f"{__package__}/{edit_subject.__name__}.html",
        {
            "subject": subject,
            "departments": Department.objects.all(),
        },
    )


@require_POST
def delete_subject(request: HttpRequest, uuid: str) -> HttpResponse:
    subject = get_object_or_404(Subject, uuid=uuid)
    name = subject.name
    subject.delete()
    success(request, f"Deleted {name}.")
    return redirect(list_departments.__name__)
