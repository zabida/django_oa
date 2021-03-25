from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status, mixins, generics, viewsets, pagination, filters
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views

from oa_admin.customer.authentication import MyAuthentication
from oa_admin.customer.pagination import SimpleLimitOffsetPagination
from oa_admin.customer.permission import BlacklistPermission
from snippets.models import Snippet, UserToken
from snippets.serializers import SnippetSerializer, UserTokenSerializer


@api_view(['GET', 'POST'])
def snippet_list(request):
    if request.method == 'GET':
        return Response('func base list')


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk):
    print(request)
    return Response('func bse detail {}'.format(pk))


class SnippetList(views.APIView):
    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(views.APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(data='success', status=status.HTTP_204_NO_CONTENT)


class SnippetListMi(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    authentication_classes = [MyAuthentication]
    permission_classes = [BlacklistPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['code', 'title']

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetDetailMi(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class SnippetListG(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = SimpleLimitOffsetPagination


class SnippetDetailG(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer


class UserTokenListG(generics.ListCreateAPIView):
    queryset = UserToken.objects.all()
    serializer_class = UserTokenSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['token', 'id']
    pagination_class = SimpleLimitOffsetPagination
    search_fields = ['token', 'user__email']
    ordering_fields = ['token', 'created_at']

    # def list(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.query_params)


class UserTokenDetailG(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserToken.objects.all()
    serializer_class = UserTokenSerializer
