from rest_framework.generics import CreateAPIView, ListCreateAPIView

from homework_help.serializers import CommentCreateSerializer, QuestionCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from homework_help.models import Order, Comment




class QuestionCreateApiView(CreateAPIView):
    serializer_class = QuestionCreateSerializer


class CommentCreateApiView(ListCreateAPIView):
    serializer_class = CommentCreateSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #
    #     serializer.is_valid(raise_exception=True)
    #     print(serializer.validated_data['message'])
    #     order = Order.objects.get(order_id=self.kwargs['order_id'])
    #     serializer.save(author=request.user, order=order)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def get_queryset(self):
    #     return PortfolioModel.objects.filter(is_published=True, is_visible=True, published_date__lte=timezone.now())
    def get_queryset(self):
        order = Order.objects.get(order_id=self.kwargs['order_id'])
        return Comment.objects.filter(order=order.id)

    # def get(self, request, *args, **kwargs):
    #     order = Order.objects.get(order_id=self.kwargs['order_id'])
    #     snippets = Comment.objects.filter(order=order.id)
    #     serializer = CommentCreateSerializer(snippets, many=True)
    #     return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            order = Order.objects.get(order_id=self.kwargs['order_id'])
            serializer.save(author=request.user, order=order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


