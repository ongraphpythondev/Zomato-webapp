from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .models import MenuItem, Category, OrderModel
from django.core.mail import send_mail

#adding various apis
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import MenuItemSerializer, OrderModelSerializer

@api_view(['GET','POST'])
def menu_list(request):
    if request.method == 'GET':
        menus = MenuItem.objects.all()
        serializer = MenuItemSerializer(menus, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE','PATCH'])
def customer_by_key(request, pk):
    try:
        menus = MenuItem.objects.get(pk=pk)
    except MenuItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MenuItemSerializer(menus)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MenuItemSerializer(menus, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = MenuItemSerializer(menus, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        menus.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Order item apis  OrderModel

@api_view(['GET','POST'])
def order_list(request):
    if request.method == 'GET':
        orders = OrderModel.objects.all()
        serializer = OrderModelSerializer(orders, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = OrderModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE','PATCH'])
def order_by_key(request, pk):
    try:
        orders = OrderModel.objects.get(pk=pk)
    except OrderModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = OrderModelSerializer(orders)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OrderModelSerializer(orders, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = OrderModelSerializer(orders, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        orders.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        searchkey = ''
        if 'search' in request.GET:
            searchkey = request.GET['search']
        print(searchkey)
        main_course = MenuItem.objects.filter(
            category__name__contains='Main Course').filter(name__contains=searchkey)
        starters = MenuItem.objects.filter(
            category__name__contains='Starters').filter(name__contains=searchkey)
        deserts = MenuItem.objects.filter(
            category__name__contains='Deserts').filter(name__contains=searchkey)
        drinks = MenuItem.objects.filter(
            category__name__contains='Drinks').filter(name__contains=searchkey)

        # pass into context
        context = {
            'main_course': main_course,
            'starters': starters,
            'deserts': deserts,
            'drin ks': drinks,
        }
        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code
        )
        order.items.add(*item_ids)

        # After all things are done confirmation email is to be send

        body = ('Thank you for your order. Your meals will be delivered as soon as possible\n'
                f'Your total: {price}\n'
                'Thank you again for your order')

        # send_mail(
        #     'Thank you for your order',
        #     body,
        #     'example@example.com',
        #     [email],
        #     fail_silently=False
        # )

        context = {
            'items': order_items['items'],
            'price': price
        }
        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }
        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)

        )
        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)
