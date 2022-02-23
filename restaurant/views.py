from django.shortcuts import render, redirect
from .models import restaurant_model
from django.core.mail import send_mail

from customer.models import MenuItem, OrderModel
from django.views import View

#adding required libraries for rest
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ContactSerializer

@api_view(['GET','POST'])
def restaurant_res(request):
    if request.method == 'GET':
        restaurants = restaurant_model.objects.all()
        serializer = ContactSerializer(restaurants, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE','PATCH'])
def restaurant_res_by_key(request, pk):
    try:
        restaurants = restaurant_model.objects.get(pk=pk)
    except restaurant_model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = ContactSerializer(restaurants)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ContactSerializer(restaurants, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = ContactSerializer(restaurants, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    elif request.method == 'DELETE':
        restaurants.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)







# Create your views here.


def index(request):
    rest = restaurant_model.objects.all()
    return render(request, 'restaurant/index.html', {
        "rest": rest
    })

class restaurant_detail(View):
    def get(self, request, *args, **kwargs):
        searchkey = ''
        rest_id = kwargs['id']
        if 'search' in request.GET:
            searchkey = request.GET['search']
        print(searchkey)
        rest = restaurant_model.objects.get(pk=rest_id)

        main_course = MenuItem.objects.filter(restaurant__id=rest_id).filter(
            category__name__contains='Main Course').filter(name__contains=searchkey)
        starters = MenuItem.objects.filter(restaurant__id=rest_id).filter(
            category__name__contains='Starters').filter(name__contains=searchkey)
        deserts = MenuItem.objects.filter(restaurant__id=rest_id).filter(
            category__name__contains='Deserts').filter(name__contains=searchkey)
        drinks = MenuItem.objects.filter(restaurant__id=rest_id).filter(
            category__name__contains='Drinks').filter(name__contains=searchkey)

        context = {
            'restaurant': rest.name,
            'main_course': main_course,
            'starters': starters,
            'deserts': deserts,
            'drinks': drinks,
        }
        return render(request, 'restaurant/restaurant_detail.html', context)

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

        send_mail(
            'Thank you for your order',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }
        return redirect('order-confirmation', pk=order.pk)

