from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Questions, Rules
from .serializer import QuestionsSerializer, RulesSerializer


class QuestionsList(APIView):
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


class RulesList(APIView):
    def get(self, request):
        rules = Rules.objects.all()
        serializer = RulesSerializer(rules, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Cria o serializer da regra com dados do payload
        serializer = RulesSerializer(data=request.data)
        if serializer.is_valid():
            # Salva a regra
            rule = serializer.save()

            # Atualiza a regra com as perguntas fornecidas
            for question_data in request.data.get('questions', []):
                # Verifica se a pergunta já existe
                existing_question = Questions.objects.filter(
                    title=question_data['title']).first()

                if existing_question:
                    # Se a pergunta já existe, apenas a associa à regra
                    rule.questions.add(existing_question)
                else:
                    # Se a pergunta não existe, cria uma nova e a associa à regra
                    question_serializer = QuestionsSerializer(
                        data=question_data)
                    if question_serializer.is_valid():
                        question = question_serializer.save()
                        rule.questions.add(question)
                    else:
                        # Se a validação falhar, retorne os erros de validação
                        return Response(question_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Atualiza o serializer da regra para incluir as perguntas
            updated_serializer = RulesSerializer(rule)
            return Response(updated_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(RetrieveUpdateDestroyAPIView):
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


class RuleDetailView(RetrieveUpdateDestroyAPIView):
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
