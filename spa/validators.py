from rest_framework import serializers


def validator_scam_url(url):
    """
       Проверяет, является ли URL допустимым для использования.

       Parameters:
            - url (str): Проверяемый URL.

       Raises:
            - serializers.ValidationError: Вызывается, если URL не начинается с 'https://www.youtube.com/'.

    """
    if not url.startswith('https://www.youtube.com/'):
        raise serializers.ValidationError('Использование стороннего ресурса!')
