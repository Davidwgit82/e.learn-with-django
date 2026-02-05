from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.text import slugify

from .models import Category, Course, Reservation

User = get_user_model()


class UserModelTest(TestCase):

    def test_create_instructor_user(self):
        instructor = User.objects.create_user(
            username="teacher1",
            password="pass123",
            is_instructor=True
        )
        self.assertTrue(instructor.is_instructor)
        self.assertFalse(instructor.is_student)

    def test_create_student_user(self):
        student = User.objects.create_user(
            username="student1",
            password="pass123",
            is_student=True
        )
        self.assertTrue(student.is_student)
        self.assertFalse(student.is_instructor)


class CategoryModelTest(TestCase):

    def test_category_creation(self):
        category = Category.objects.create(name="Web Development")

        self.assertEqual(category.name, "Web Development")
        self.assertEqual(category.slug, slugify("Web Development"))
        self.assertIsNotNone(category.created_at)

    def test_category_unique_name(self):
        Category.objects.create(name="Python")

        with self.assertRaises(IntegrityError):
            Category.objects.create(name="Python")


class CourseModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher",
            password="pass",
            is_instructor=True
        )

        self.category = Category.objects.create(name="Backend")

        self.course = Course.objects.create(
            teacher=self.teacher,
            category=self.category,
            title="Django Avancé",
            description="Master Django like a pro",
            prix=100,
            places=2,
            is_active=True
        )

    def test_course_creation(self):
        self.assertEqual(self.course.teacher.username, "teacher")
        self.assertEqual(self.course.category.name, "Backend")
        self.assertTrue(self.course.is_active)
        self.assertEqual(self.course.places, 2)

    
    def test_course_str(self):
        self.assertIn("Django Avancé", str(self.course))
        self.assertIn("teacher", str(self.course))


    def test_course_is_available_when_empty(self):
        self.assertTrue(self.course.is_available)

    def test_course_not_available_when_full(self):
        student1 = User.objects.create_user(username="s1", password="pass", is_student=True)
        student2 = User.objects.create_user(username="s2", password="pass", is_student=True)

        Reservation.objects.create(student=student1, course=self.course)
        Reservation.objects.create(student=student2, course=self.course)

        self.assertFalse(self.course.is_available)

    def test_course_not_available_when_inactive(self):
        self.course.is_active = False
        self.course.save()

        self.assertFalse(self.course.is_available)


class ReservationModelTest(TestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher",
            password="pass",
            is_instructor=True
        )

        self.student = User.objects.create_user(
            username="student",
            password="pass",
            is_student=True
        )

        self.category = Category.objects.create(name="DevOps")

        self.course = Course.objects.create(
            teacher=self.teacher,
            category=self.category,
            title="Docker Basics",
            description="Learn Docker",
            places=1
        )

    def test_reservation_creation(self):
            reservation = Reservation.objects.create(
                student=self.student,
                course=self.course
            )

            self.assertEqual(reservation.student, self.student)
            self.assertEqual(reservation.course, self.course)

    def test_unique_reservation_per_student(self):
        Reservation.objects.create(
            student=self.student,
            course=self.course
        )

        with self.assertRaises(IntegrityError):
            Reservation.objects.create(
                student=self.student,
                course=self.course
            )

    def test_reservation_str(self):
        reservation = Reservation.objects.create(
            student=self.student,
            course=self.course
        )

        self.assertIn(self.student.username, str(reservation))
        self.assertIn(self.course.title, str(reservation))
