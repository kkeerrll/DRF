from rest_framework import viewsets, generics, status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from spa.tasks import send_email_course_update

from permissions import IsOwner, IsModerator
from spa.models import Course, Lesson, Subscription
from spa.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        """Права доступа"""
        if self.action == 'retrieve':
            permission_classes = [IsOwner | IsModerator | IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsOwner | IsAdminUser]
        elif self.action == 'update':
            permission_classes = [IsOwner | IsModerator | IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        instance = serializer.save()

        send_email_course_update.delay(instance.pk)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class LessonUpdateAPIView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]


class LessonRetrieveAPIView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsModerator | IsAdminUser]


class SubscribeCourseView(generics.CreateAPIView):
    """
    Создает подписку пользователя на указанный курс.

    Parameters:
        course_id (int): Идентификатор курса.

    Returns:
        Response: Объект ответа с информацией о результате операции.
            HTTP_201_CREATED: Подписка успешно создана.
            HTTP_400_BAD_REQUEST: Подписка уже существует.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)

        # Проверка, подписан ли пользователь уже на этот курс
        if Subscription.objects.filter(user=request.user, course=course).exists():
            return Response({'detail': 'Вы уже подписаны на этот курс.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data={'user': request.user.id, 'course': course.id})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response({'detail': 'Вы успешно подписались на курс.'}, status=status.HTTP_201_CREATED)


class UnsubscribeCourseView(generics.DestroyAPIView):
    """
    Удаляет подписку пользователя на указанный курс.

    Parameters:
        course_id (int): Идентификатор курса.

    Returns:
        Response: Объект ответа с информацией о результате операции.
            HTTP_200_OK: Подписка успешно удалена.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        course_id = self.kwargs.get('course_id')
        course = Course.objects.get(pk=course_id)
        return Subscription.objects.get(user=self.request.user, course=course)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Вы успешно отписались от курса.'}, status=status.HTTP_200_OK)
