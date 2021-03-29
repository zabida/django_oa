from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from oa_admin.customer import errors

from snippets.models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet, UserToken, User


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """, 
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()


class UserTokenSerializer(serializers.Serializer):
    # user = UserSerializer(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    effective_date = serializers.DateField(format='%Y-%m-%d', read_only=True)

    def get_user(self, obj):
        try:
            user = User.objects.get(id=obj.get('user'))
        except ObjectDoesNotExist:
            return {}
        return {'username': user.username, 'id': user.id}

    def create(self, validated_data):
        user = User.objects.filter(id=validated_data.get('user_id')).first()
        if not user:
            raise errors.raise_validation_error('未找到user')

        validated_data['user'] = user
        user_token = UserToken(**validated_data)
        user_token.save()
        return user_token
