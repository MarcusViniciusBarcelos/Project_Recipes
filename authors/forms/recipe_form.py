from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError

from recipes.models import Recipe
from utils.django_forms import add_attr
from utils.strings import is_positive_number


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._my_errors = defaultdict(list)

        add_attr(self.fields.get('preparation_steps'), 'class', 'span-2')

    class Meta:
        model = Recipe
        fields = 'title', 'description', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        widgets = {
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Porções', 'Porções'),
                    ('Pedaços', 'Pedaços'),
                    ('Pessoas', 'Pessoas'),
                    ('Copos', 'Copos'),
                ),
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos', 'Minutos'),
                    ('Horas', 'Horas')
                ),
            ),
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cleaned_data = self.cleaned_data

        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if description == title:
            self._my_errors['description'].append(
                'Cannot be equal to title'
            )
            self._my_errors['title'].append(
                'Cannot be equal to Description'
            )
        if self._my_errors:
            raise ValidationError(self._my_errors)
        return super_clean

    def validate_field(self, field_name, min_length=None, is_positive=False):
        field_value = self.cleaned_data.get(field_name)

        if min_length is not None and len(field_value) < min_length:
            formatted_field_name = field_name.replace('_', ' ').capitalize()
            self._my_errors[field_name].append(
                f'{formatted_field_name} must be at least {min_length} characters'
            )

        if is_positive and not is_positive_number(field_value):
            self._my_errors[field_name].append(
                'Must be a positive number'
            )

        return field_value

    def clean_title(self):
        return self.validate_field('title', min_length=5)

    def clean_description(self):
        return self.validate_field('description', min_length=10)

    def clean_preparation_time(self):
        return self.validate_field('preparation_time', is_positive=True)

    def clean_servings(self):
        return self.validate_field('servings', is_positive=True)

    def clean_preparation_steps(self):
        return self.validate_field('preparation_steps', min_length=30)
