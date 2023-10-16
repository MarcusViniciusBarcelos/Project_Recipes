from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


class RecipeAPIV2Pagination(PageNumberPagination):
    page_size = 10


class RecipeAPIv2ViewSet(ModelViewSet):
    queryset = Recipe.objects.get_published()  # type: ignore
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination

    def create(self, request):
        serializer = RecipeSerializer(
            data=request.data,
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            author_id=3, category_id=3, is_published=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
