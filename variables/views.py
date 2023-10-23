from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Rules, Values, Variables
from .serializer import RulesSerializer, ValuesSerializer, VariablesSerializer


class ValuesListView(ModelViewSet):
    queryset = Values.objects.all()
    serializer_class = ValuesSerializer

    def post(self, request, variables_id):
        variables = get_object_or_404(Variables, id=variables_id)
        request.data['variables'] = variables.id
        serializer = ValuesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VariablesListView(ModelViewSet):
    queryset = Variables.objects.all()
    serializer_class = VariablesSerializer

    def post(self, request):
        serializer = VariablesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RulesListView(ModelViewSet):
    queryset = Rules.objects.all()
    serializer_class = RulesSerializer

    def post(self, request):
        serializer = RulesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
