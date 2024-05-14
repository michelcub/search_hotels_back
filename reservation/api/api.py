from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reservation.models import Reservation
from habitacion.models import Room
from django.contrib.auth.models import User

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
      
