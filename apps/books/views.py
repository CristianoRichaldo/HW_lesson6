from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse

from .models import Books
from .serializers import BooksSerializers

Books = ['Книга']

class BookListApi(APIView):

    @extend_schema(
            tags=Books,
            summary='СПИСОК ВСЕХ КНИГ',
            responses={200: BooksSerializers(many=True)}
    )
    def get(self, request):
        books = Books.objects.all()
        serializer = BooksSerializers(books, many=True)
        return Response(serializer.data)

    @extend_schema(
            tags=Books,
            summary='Добавить книгу в список',
            request=BooksSerializers,
            responses={201: BooksSerializers}
        )
    def post(self, request):
        serializer = BooksSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Item
from .serializers import ItemSerializer

class ItemListCreateAPIView(APIView):
    """
    Класс для получения списка элементов и создания новых записей.
    Доступ: Авторизованные пользователи (JWT или Django Token).
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Получить список всех элементов",
        operation_description="Возвращает полный список элементов, доступных текущему пользователю.",
        responses={
            200: ItemSerializer(many=True),
            401: "Ошибка авторизации (Токен не валиден или отсутствует)"
        }
    )
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Создать новый элемент",
        operation_description="Создает новую запись в базе данных. Поле 'title' обязательно.",
        request_body=ItemSerializer,
        responses={
            201: ItemSerializer,
            400: "Невалидные данные запроса",
            401: "Ошибка авторизации"
        }
    )
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemDetailAPIView(APIView):
    """
    Класс для работы с конкретным элементом (Просмотр, Изменение, Удаление).
    """
   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="Получить элемент по ID",
        operation_description="Возвращает детальную информацию по конкретному элементу.",
        responses={200: ItemSerializer, 404: "Элемент не найден"}
    )
    def get(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ItemSerializer(item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Обновить элемент (Полностью)",
        request_body=ItemSerializer,
        responses={200: ItemSerializer, 400: "Ошибки валидации", 403: "Нет прав для редактирования"}
    )
    def put(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Удалить элемент",
        responses={24: "Успешно удалено", 403: "Нет прав для удаления"}
    )
    def delete(self, request, pk):
        try:
            item = Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
            
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
