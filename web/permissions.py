from course.models import Reservation
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(Reservation)
permission = Permission.objects.create(
    codename = 'can_reserve_a_course',
    name = 'Can book/reserve a course',
    content_type = content_type
)