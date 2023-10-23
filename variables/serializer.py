from rest_framework import serializers

from .models import Rules, Values, Variables


class VariablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variables
        fields = ('id', 'name')


class ValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Values
        fields = ('id', 'name', 'variables')


class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        fields = ('id', 'name', 'description', 'variable', 'variable_object')

    variable_object = VariablesSerializer(many=True, read_only=True)
    variable = serializers.SerializerMethodField()

    def get_variable(self, obj):
        return f'{obj.variable.name} {", ".join([value.name for value in obj.variable.values.all()])}'
