import pytest
from django.urls import reverse
from rest_framework import status
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
from spa.models import Lesson, Course, Subscription
from users.models import User
from spa.models import Subscription


@pytest.mark.django_db
class TestSubscriptionViews:

    def test_subscribe_course(self, client, user, course):
        url = reverse('course:subscribe-course', kwargs={'course_id': course.id})
        client.force_authenticate(user=user)
        response = client.post(url)
        assert response.status_code == status.HTTP_201_CREATED
        assert Subscription.objects.filter(user=user, course=course).exists()

    def test_unsubscribe_course(self, client, user, subscription):
        url = reverse('course:unsubscribe-course', kwargs={'course_id': subscription.course.id})
        client.force_authenticate(user=user)
        response = client.delete(url)
        assert response.status_code == status.HTTP_200_OK
        assert not Subscription.objects.filter(id=subscription.id).exists()

from django.test import TestCase


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='likusya-2000@mail.ru',
            password='test',
            is_active=True,
            is_staff=True,
            is_superuser=True,
            role="moderator"
        )
        self.client.force_authenticate(user=self.user)

        self.course = Course.objects.create(title="Python Developer")

        self.lesson = Lesson.objects.create(
            title='test',
            description='Test',
            owner=self.user,
            video_link='https://www.youtube.com/watch?v=...'
        )

    def test_create_lesson(self):
        data = {
            'title': self.lesson.title,
            'description': self.lesson.description,
            'course': self.course.id,
            'video_link': self.lesson.video_link
        }

        response = self.client.post(
            reverse('education:lesson_create'),
            data=data
        )

        self.assertEquals(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEquals(response.json(), {
            'id': 2,
            'title': 'test',
            'description': 'Test',
            'photo': None,
            'video_link': 'https://www.youtube.com/watch?v=...',
            'course': 1,
            'owner': 1
        })

    def test_list_lesson(self):
        response = self.client.get(
            reverse("education:lesson_list")
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), {'count': 1,
                                            'next': None,
                                            'previous': None,
                                            'results': [
                                                {'id': self.lesson.pk,
                                                 'title': 'test',
                                                 'description': 'Test',
                                                 'photo': None,
                                                 'video_link': 'https://www.youtube.com/watch?v=...',
                                                 'course': None,
                                                 'owner': self.lesson.owner_id}]})

    def test_destroy_lesson(self):
        response = self.client.delete(
            reverse("education:lesson_delete",
                    args=[self.lesson.pk])
        )

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_lesson(self):
        response = self.client.patch(
            reverse("education:lesson_update",
                    args=[self.lesson.pk]),
            data={"title": "Lesson 2 test"}
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json(), {
            "id": self.lesson.pk,
            "title": "Lesson 2 test",
            "description": self.lesson.description,
            "owner": self.lesson.owner_id,
            "photo": None,
            "video_link": self.lesson.video_link,
            "course": None,
        })

    def test_detail_lesson(self):
        response = self.client.get(
            reverse("education:lesson_get",
                    args=[self.lesson.pk])
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

        self.assertEquals(response.json(), {
            "id": self.lesson.pk,
            "title": self.lesson.title,
            "description": self.lesson.description,
            "owner": self.lesson.owner_id,
            "photo": None,
            "video_link": self.lesson.video_link,
            "course": None,
        })

    def tearDown(self):
        User.objects.all().delete()
        Lesson.objects.all().delete()
        Course.objects.all().delete()

