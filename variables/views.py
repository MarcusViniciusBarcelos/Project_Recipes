from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Rules, Values, Variables
from .serializer import RulesSerializer, ValuesSerializer, VariablesSerializer


class ValuesListView(ModelViewSet):
    queryset = Values.objects.all()
    serializer_class = ValuesSerializer

    def post(self, request, variables_id):
        variables = get_object_or_404(Variables, id=variables_id)
        request.data['variables'] = variables.pk
        serializer = ValuesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(variables=variables)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # Use 'kwargs.get' para obter o valor do parâmetro sem causar KeyError
        variables_id = kwargs.get('variables_id')

        if variables_id is not None:
            variables = get_object_or_404(Variables, id=variables_id)
            queryset = self.filter_queryset(
                self.get_queryset().filter(variables=variables))
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # Se 'variables_id' não estiver presente, pode ser um erro de configuração
            return Response({'error': 'Missing "variables_id" parameter'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def add_value_to_variable(self, request, variables_id):
        variables = get_object_or_404(Variables, id=variables_id)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(variables=variables)
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
