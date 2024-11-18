from collections import defaultdict
from rest_framework import serializers
from django.db import transaction

from accounts.models import Address
from .models import Order, OrderItem
from shop.models import Product
from shop.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'unit_price', 'total_price']
        read_only_fields = ['id', 'product', 'unit_price', 'total_price']


class OrderSerializer(serializers.Serializer):
    items = OrderItemSerializer(many=True)
    address_id = serializers.IntegerField()
    # total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        fields = ['items', 'address_id']

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        items_data = validated_data.pop('items')
        address_id = validated_data.get('address_id')

        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            raise serializers.ValidationError('地址不存在')

        # 按商店分组商品项
        shop_items = defaultdict(list)
        for item_data in items_data:
            product_id = item_data['product_id']
            quantity = item_data['quantity']

            try:
                product = Product.objects.select_related('shop').get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({"error": f"商品ID {product_id} 不存在"})

            if product.status == 'Unavailable':
                raise serializers.ValidationError({"error": f"商品 {product.name} 已失效"})

            if product.stock_quantity < quantity:
                raise serializers.ValidationError({"error": f"商品 {product.name} 库存不足"})

            shop_id = product.shop.id
            shop_items[shop_id].append({
                'product': product,
                'quantity': quantity
            })

        created_orders = []
        for shop_id, items in shop_items.items():
            # 创建订单
            order = Order.objects.create(
                user=user,
                shop_id=shop_id,
                recipient_name=address.recipient_name,
                total_price=0,
                address=address.address,
                city=address.city,
                province=address.province,
                phone=address.phone,
                status='Pending Payment'
            )

            total_amount = 0
            for item in items:
                product = item['product']
                quantity = item['quantity']
                unit_price = product.price
                total_price = unit_price * quantity
                total_amount += total_price

                product.stock_quantity -= quantity

                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )

            order.total_price = total_amount
            order.save()
            created_orders.append(order)
        # print('return!')
        return created_orders

    def to_representation(self, instance):

        if isinstance(instance, Order):
            single_object = True
            instance = [instance]
        else:
            single_object = False

        data = []
        for order in instance:
            order_data = {
                'order_id': order.id,
                'user': order.user.id,
                'shop_id': order.shop.id,
                'total_price': str(order.total_price),
                'order_date': order.order_date.isoformat(),
                'status': order.status,
                'address': {
                    'recipient_name': order.recipient_name,
                    'address': order.address,
                    'city': order.city,
                    'province': order.province,
                    'phone': order.phone,
                },
                'items': []
            }
            # 获取订单项
            order_items = order.items.all()
            # order_total_price = 0
            for item in order_items:
                order_data['items'].append({
                    'id': item.id,
                    'product': ProductSerializer(item.product).data,
                    'quantity': item.quantity,
                    'unit_price': str(item.unit_price),
                    'total_price': str(item.total_price),
                    'is_cancelled': item.is_cancelled,
                })
                # if not item.is_cancelled:
                #     order_total_price += item.total_price
            # order_data['total_price'] = order_total_price
            data.append(order_data)
        return {'orders': data} if not single_object else data[0]
