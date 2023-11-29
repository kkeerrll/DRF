import pytest
from django.urls import reverse
from rest_framework import status

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
