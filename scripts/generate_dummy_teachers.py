from asyncio.log import logger
from io import BytesIO
from subject.models import Grade, Subject, TeachingMedium
from teacher.models import (
    ClassType,
    DayOfWeek,
    Teacher,
    District,
    EducationQualification,
)
import random
import requests
import json
import os
from PIL import Image
from django.core.files import File


from faker import Faker

fake = Faker()
fake.company()


def get_fake_face():
    print("\nDownloading the fake face :", end="")

    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "sec-ch-ua-platform": '"Linux"',
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://this-person-does-not-exist.com/en",
        "Accept-Language": "en-US,en;q=0.9,si;q=0.8",
    }

    response = requests.get(
        "https://this-person-does-not-exist.com/en?new", headers=headers
    )

    print("[Generated] ", end="")

    resp = json.loads(response.text)
    new_img_url = "https://this-person-does-not-exist.com" + resp.get("src")
    new_img_name = resp.get("name")

    resp = requests.get(new_img_url)
    print("[Downloaded] ")

    download_path = os.getcwd() + "/media/teacher/profilepicture"

    file = open(download_path + "/" + new_img_name, "wb+")
    file.write(resp.content)

    django_file_obj = File(file, name=new_img_name)

    return django_file_obj


def get_random_number(smallest, largest):
    return random.randint(smallest, largest)


def run():
    number_of_rounds = 50

    for _ in range(number_of_rounds):
        profile_picture = get_fake_face()

        teacher = Teacher.objects.create(
            name=fake.name(),
            highest_education_qualification=EducationQualification.objects.get(
                id=get_random_number(1, 5)
            ),
            years_of_experience=get_random_number(1, 10),
            working_place=fake.company(),
            contact_mobile=fake.msisdn(),
            message_to_students=fake.paragraph(nb_sentences=50),
            district=District.objects.get(id=get_random_number(1, 25)),
            profile_picture=profile_picture,
        )

        profile_picture.close()

        print(f"Teacher Created - {teacher.name}")

        print(f"New Schedule Created => ", end="")

        random_subject_id = get_random_number(1, 7)

        for _ in range(get_random_number(2, 5)):
            schedule = teacher.schedule_set.create(
                subject=Subject.objects.get(id=random_subject_id),
                grade=Grade.objects.get(id=get_random_number(1, 7)),
                place=fake.company(),
                day=DayOfWeek.objects.get(id=get_random_number(1, 7)),
                from_time=f"{get_random_number(1,23)}:00:00",
                to_time=f"{get_random_number(1,23)}:00:00",
                class_type=ClassType.objects.get(id=1),  # Local
                medium=TeachingMedium.objects.get(
                    id=get_random_number(1, 2)
                ),  # Except Tamil
                district=District.objects.get(id=get_random_number(1, 25)),
                held_online=bool(random.getrandbits(1)),
            )

            schedule.save()

            print(f"[{schedule.id}]", end=" ")
