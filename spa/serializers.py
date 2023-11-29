from rest_framework import serializers

from spa.models import Course, Lesson, Subscription


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')

    class Meta:
        model = Course
        fields = '__all__'

    def get_num_lessons(self, obj):
        """
            Возвращает количество уроков в курсе.
        """
        return obj.lesson_set.count()

    def get_is_subscribed(self, obj):
        """
            Возвращает информацию о том, подписан ли пользователь на обновления курса.

            Parameters:
                obj (Course): Экземпляр модели курса.

            Returns:
                bool: Признак подписки на курс.
        """
        user = self.context['request'].user

        return Subscription.objects.filter(user=user, course=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    """
       Сериализатор для модели подписки на курс.

       Attributes:
           model (Subscription): Модель, которая используется для сериализации.
           fields : Поля, которые будут сериализованы (все поля).
    """

    class Meta:
        model = Subscription
        fields = '__all__'
