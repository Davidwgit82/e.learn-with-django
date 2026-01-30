from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError

from .models import User, Category, Course, Reservation


class UserModelTest(TestCase):
    def test_create_user_roles(self):
        user = User.objects.create_user(
            username="teacher1",
            password="testpass123",
            is_instructor=True
        )

        self.assertTrue(user.is_instructor)
        self.assertFalse(user.is_student)


class CategoryModelTest(TestCase):
    def test_category_creation_and_str(self):
        category = Category.objects.create(name="Programmation")

        self.assertEqual(str(category), "Programmation")
        self.assertIsNotNone(category.created_at)
        self.assertIsNotNone(category.updated_at)


class CourseModelTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher",
            password="pass123",
            is_instructor=True
        )

        self.student = User.objects.create_user(
            username="student",
            password="pass123",
            is_student=True
        )

        self.category = Category.objects.create(name="Web")

        self.course = Course.objects.create(
            teacher=self.teacher,
            category=self.category,
            title="Django Avancé",
            description="Cours complet Django",
            prix=5000,
            places=2
        )

    def test_course_creation(self):
        self.assertEqual(self.course.teacher.username, "teacher")
        self.assertEqual(self.course.category.name, "Web")
        self.assertTrue(self.course.is_available)

    def test_course_str(self):
        self.assertEqual(
            str(self.course),
            "Django Avancé (Par: teacher)"
        )

    def test_course_availability(self):
        Reservation.objects.create(
            student=self.student,
            course=self.course
        )

        self.assertTrue(self.course.is_available)

        second_student = User.objects.create_user(
            username="student2",
            password="pass123",
            is_student=True
        )

        Reservation.objects.create(
            student=second_student,
            course=self.course
        )

        self.assertFalse(self.course.is_available)


class ReservationModelTest(TestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher",
            password="pass123"
        )

        self.student = User.objects.create_user(
            username="student",
            password="pass123"
        )

        self.category = Category.objects.create(name="Backend")

        self.course = Course.objects.create(
            teacher=self.teacher,
            category=self.category,
            title="Python",
            description="Cours Python",
            prix=3000,
            places=1
        )

    def test_reservation_creation(self):
        reservation = Reservation.objects.create(
            student=self.student,
            course=self.course
        )

        self.assertEqual(reservation.student.username, "student")
        self.assertEqual(reservation.course.title, "Python")

    def test_unique_reservation_constraint(self):
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

        self.assertEqual(
            str(reservation),
            "student réservé -> Python"
        )