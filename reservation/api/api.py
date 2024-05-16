from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from reservation.models import Reservation
from habitacion.models import Room
from django.contrib.auth.models import User
from payment.models import Payment
from hotel.models import Hotel

from reservation.api.serializer import ReservationSerializer

import uuid

@api_view(['POST'])
def reserva_habitacion(request):
        data = request.data
        init_date = data.get('init', None)
        end_date = data.get('end', None)
        customer_list = data.get('customers', None)
        
        
        
        if init_date is None or end_date is None or len(customer_list) == 0:
            return Response({'message': 'Fechas de inicio y fin son requeridas'}, status.HTTP_400_BAD_REQUEST)
        
        user_list = []
        
        for customer in customer_list:
            if not User.objects.filter(username=customer['email']).exists():
                user = User.objects.create_user(username=customer['email'], email=customer['email'], password=uuid.uuid4(), first_name=customer['first_name'], last_name=customer['last_name'])
                user_list.append(user)
            else:
                user = User.objects.get(username=customer['email'])
                user_list.append(user)
                
        rooms = Room.objects.all()

       
        for room in rooms:
            if not Reservation.objects.filter(room=room, init_date__lte=end_date, end_date__gte=init_date).exists():
                reservation = Reservation.objects.create(room=room, init_date=init_date, end_date=end_date)
                reservation.customers.set(user_list)
                reservation.main_customer = user_list[0]
                reservation.quantity = len(user_list)
                reservation.save()
                return Response({'message': f'Reserva creada para la habitación {room.id} exitosamente',
                                 'reservation': reservation}, status.HTTP_201_CREATED)
        return Response({'message': 'No hay habitaciones disponibles'}, status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def reserva(request):
    reservations = Reservation.objects.all()
    
    if request.query_params.get('room', None):
        room_id = request.query_params.get('room')
        reservations = reservations.filter(room=room_id)
        
    if request.query_params.get('username', None):
        customer_username = request.query_params.get('username')
        reservations = reservations.filter(customers__username=customer_username)
        
    if request.query_params.get('init', None):
        init_date = request.query_params.get('init')
        reservations = reservations.filter(init_date=init_date)
        
    if request.query_params.get('end', None):
        end_date = request.query_params.get('end')
        reservations = reservations.filter(end_date=end_date)    
        
    return Response({'reservations': reservations}, status.HTTP_200_OK)
      

@api_view(['POST'])
@permission_classes([AllowAny])
def create_reservation(request):
    try:
        data = request.data
        room_type = data.get('room', None)
        hotel = room_type.get('hotel', None).get('id', None)
        services = data.get('services', [])
        users = data.get('users', [])
        total = data.get('total', None)
        init_date = data.get('init', None)
        end_date = data.get('end', None)
        payment_id = data.get('payment', None)
        
       
        if None in [room_type, hotel, total, init_date, end_date, payment_id]:
            return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)
        
        room = get_object_or_404(Room, pk=room_type['id'])
        payment = get_object_or_404(Payment, pk=payment_id)
        hotel = get_object_or_404(Hotel, pk=hotel)
        
        customers = []
        for user_data in users:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['email'],
                    'first_name': user_data['name'],
                    'last_name': user_data['lastname'],
                    'password': user_data.get('password', ''),
                }
            )
            customers.append(user)
        
        
        reservation = Reservation.objects.create(
            room=room,
            init_date=init_date,
            end_date=end_date,
            main_customer=customers[0] if customers else None,
            quantity=len(customers),
            amount=total,
            hotel=hotel
        )
        
        
        reservation.customers.set(customers)
        reservation.services.set(services)
        
        
        
        reservation.save()
        
       
        payment.reservation = reservation
        payment.save()
        
        reservation.check_is_paid()
        
        
        return Response(ReservationSerializer(reservation).data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print('error al crear la reserva>>>>>>>>>>>>', str(e))
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        