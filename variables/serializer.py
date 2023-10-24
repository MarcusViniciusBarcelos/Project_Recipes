from rest_framework import serializers

from .models import Questions, Rules


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Questions
        fields = ['id', 'title', 'answer']


class RulesSerializer(serializers.ModelSerializer):
    questions = QuestionsSerializer(many=True, read_only=True)

    class Meta:
        model = Rules
        fields = ['id', 'name', 'questions', 'result']
