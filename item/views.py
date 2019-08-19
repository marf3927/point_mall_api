from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction
from rest_condition import Or, And
import json

from .permissions import IsSafeMethod, InPurchase
from .models import Item, UserItem, Category, History, HistoryItem
from .serializers import ItemSerializer, UserItemSerializer, CategorySerializer, HistorySerializer, HistoryItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (Or(
        IsSafeMethod,
        permissions.IsAdminUser,
        And(InPurchase, permissions.IsAuthenticated)
    ),)

    @action(detail=True, methods=['POST'])
    def purchase(self, request, *args, **kwargs):
        item = self.get_object()
        user = request.user
        if item.price > user.point:
            return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
        user.point -= item.price
        user.save()

        history = History(user=request.user)
        history.save()
        HistoryItem(history=history, item=item, count=1).save()

        try:
            user_item = UserItem.objects.get(user=user, item=item)
        except UserItem.DoesNotExist:
            user_item = UserItem(user=user, item=item)
        user_item.count += 1
        user_item.save()

        serializer = UserItemSerializer(user.items.all(), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path= 'purchase')
    @transaction.atomic()
    def purchase_items(self, request, *args, **kwarge):
        user = request.user
        items = request.data['items']
        sid = transaction.savepoint()
        history = History(user=request.user)
        history.save()

        for i in items:
            item = Item.objects.get(id=i['item_id'])
            count = int(i['count'])

            if item.price * count > user.point:
                transaction.savepoint_rollback(sid)
                return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
            user.point -= item.price * count
            user.save()
            try:
                user_item = UserItem.objects.get(user=user, item=item)
            except UserItem.DoesNotExist:
                user_item = UserItem(user=user, item=item)
            user_item.count += count
            user_item.save()

            HistoryItem(history=history, item=item, count=count).save()

        transaction.savepoint_commit(sid)
        serializer = UserItemSerializer(user.items.all(), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        item = serializer.save()
        category = self.request.data['category_id']
        for i in json.loads(category):
            print(i)
            item.category.add(Category.objects.get(id=i))


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True)
    def items(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = ItemSerializer(category.items.all(), many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user=self.request.user).order_by('-id')

    @action(detail=True, methods=['POST'])
    def refund(self, request, *args, **kwargs):
        history = self.get_object()
        user = request.user
        if history.user != user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        elif history.is_refunded:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        for history_item in history.items.all():
            try:
                user_item = UserItem.objects.get(user=user, item=history_item.item)
                user_item.count = user_item.count - history_item.count
                if user_item.count > 0:
                    user_item.save()
                else:
                    user_item.delete()

                user.point += history_item.item.price * history_item.count
            except UserItem.DoesNotExist:
                pass
        history.is_refunded = True
        history.save()
        user.save()

        serializer = self.get_serializer(history)
        return Response(serializer.data)
