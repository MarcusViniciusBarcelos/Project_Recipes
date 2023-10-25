from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Questions, Rules
from .serializer import QuestionsSerializer, RulesSerializer


class QuestionsList(ModelViewSet):
    def get(self, request):
        questions = Questions.objects.all()
        serializer = QuestionsSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RulesList(ModelViewSet):
    def get(self, request):
        rules = Rules.objects.all()
        serializer = RulesSerializer(rules, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Extrai IDs das perguntas do payload
        questions_ids = request.data.pop('questions', [])

        # Cria a regra sem associar perguntas
        serializer = RulesSerializer(data=request.data)
        if serializer.is_valid():
            rule = serializer.save()

            # Associa as perguntas à regra pelos IDs fornecidos
            for question_id in questions_ids:
                question = get_object_or_404(Questions, pk=question_id)
                rule.questions.add(question)

            # Atualiza o serializer da regra para incluir as perguntas
            updated_serializer = RulesSerializer(rule)
            return Response(updated_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(ModelViewSet):
    queryset = Questions.objects.all()
    serializer_class = QuestionsSerializer

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class RuleDetailView(ModelViewSet):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
