from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from .models import ArticleCollection
from .serializers import CollectionModelSerializer
from rest_framework.permissions import IsAuthenticated


class MyCollectionListAPIView(ListAPIView):
    """我的文集"""
    serializer_class = CollectionModelSerializer
    permission_classes = [IsAuthenticated]  # 必须是登陆用户才能访问过来

    def get_queryset(self):
        user = self.request.user
        """重写queryset属性值"""
        ret = ArticleCollection.objects.filter(user=user).order_by("orders", "-id")
        if len(ret) < 1:
            # 当用户如果没有文集,在默认给用户创建2个文集
            collection1 = ArticleCollection.objects.create(
                user=user,
                name="日记本",
                orders=1,
            )

            collection2 = ArticleCollection.objects.create(
                user=user,
                name="随笔",
                orders=2,
            )

            ret = [
                {"id": collection1.pk, "name": collection1.name},
                {"id": collection2.pk, "name": collection2.name},
            ]

        return ret


from rest_framework.generics import CreateAPIView


class CollectionCreateAPIView(CreateAPIView):
    """添加文集"""
    serializer_class = CollectionModelSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.generics import UpdateAPIView


class CollectionUpdateAPIView(UpdateAPIView):
    """修改文集"""
    queryset = ArticleCollection.objects.all()
    serializer_class = CollectionModelSerializer
    permission_classes = [IsAuthenticated]


from rest_framework.viewsets import GenericViewSet
from .models import Article
from .serializers import ArticleModelSerializer
from rest_framework.response import Response


class ArticleOfCollectionViewSet(GenericViewSet, ListAPIView, CreateAPIView):
    """当前文集的文章列表"""
    serializer_class = ArticleModelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        collection_id = request.query_params.get("collection")
        user = request.user
        queryset = Article.objects.filter(is_delete=False, user=user, collection_id=collection_id).order_by("orders",
                                                                                                            "-id")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


from rest_framework.views import APIView
from rest_framework import status


class ArticlePublicStatusAPIView(APIView):
    """切换文章的发布状态"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response("对不起,当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)

        is_public = request.data.get("is_public")
        article.is_public = not not is_public
        article.pub_date = None
        article.save()
        return Response("操作成功!")


class ArticlechangeCollection(APIView):
    """移动文章"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response("对不起,当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)

        collection_id = request.data.get("collection_id")
        article.collection_id = int(collection_id)
        article.save()
        return Response("操作成功!")


class ArticleIntervalAPIView(APIView):
    """定时发布文章"""
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            article = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response("对不起,当前文章不存在!", status=status.HTTP_400_BAD_REQUEST)

        pub_date = request.data.get("pub_date")
        article.pub_date = pub_date
        article.save()
        return Response("操作成功!")

from .models import Special
from .serializers import SpecialModelSerializer
class SpecialListAPIView(ListAPIView):
    queryset = Special.objects.all()
    serializer_class = SpecialModelSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        ret = self.get_queryset().filter(mymanager__user=user)
        queryset = self.filter_queryset(ret)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)