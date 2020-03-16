from rest_framework.generics import CreateAPIView, ListCreateAPIView

from homework_help.serializers import CommentCreateSerializer, QuestionCreateSerializer, QuestionFileCreateSerializer
from rest_framework.response import Response
from rest_framework import status
from homework_help.models import Order, Comment, QuestionFile, Question
import simplejson as json




class QuestionCreateApiView(CreateAPIView):
    serializer_class = QuestionCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        data = request.POST.getlist('unique_id')
        serializer.is_valid(raise_exception=True)


        serializer.save(author=request.user)
        q = Question.objects.get(question=serializer.validated_data.get('question'))
        # print(q.id)
        for i in data:
            qf = QuestionFile.objects.get(unique_id=i)
            qf.question = q
            qf.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class QuestionFileCreateApiView(CreateAPIView):
    serializer_class = QuestionFileCreateSerializer

    # def create(self, request, *args, **kwargs):


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

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(order_id=self.kwargs['order_id'])
        qs = Comment.objects.filter(order=order.id)

        data = {}
        item = {}
        i = 0
        # for i in range(len(sqs)):
        for result in qs:
            # document_obj = Document.objects.get(slug=result.slug)
            item["author"] = result.author.first_name
            date = result.created
            date_final = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
            time = str(date.hour) + ":" + str(date.minute)
            item["date"] = date_final
            item["time"] = time
            item["message"] = result.message
            try:
                item["reference_files"] = result.reference_files.url
            except:
                pass

            data[i] = item
            item = {}
            i += 1

        the_data = json.dumps(data)

        return Response(data, content_type="application/json")

    def get_queryset(self):
        order = Order.objects.get(order_id=self.kwargs['order_id'])
        qs = Comment.objects.filter(order=order.id)

        data = {}
        item = {}
        i = 0
        # for i in range(len(sqs)):
        for result in qs:
            # document_obj = Document.objects.get(slug=result.slug)
            item["author"] = result.author.first_name
            date = result.created
            date_final = date.day + "/" + date.month + "/" + date.year
            item["created"] = date_final
            item["message"] = result.message
            try:
                item["reference_files"] = result.reference_files.url
            except:
                pass

            data[i] = item
            item = {}
            i += 1

        the_data = json.dumps(data)

        return Response(data, content_type="application/json")

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

