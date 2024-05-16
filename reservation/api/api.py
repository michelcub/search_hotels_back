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

@api_view(['GET'])
def reservation_list(request):
    print(request.user, '>>>>>>')
    try:
        reservations = Reservation.objects.all()
        
        
        
        
        reservations_data = ReservationSerializer(reservations, many=True).data
        return Response(reservations_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      

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
        
        
@api_view(['DELETE'])
def delete_reservation(request, id):
    try:
        reservation = Reservation.objects.get(pk=id)
        if not reservation:
            return Response({'error': 'Reservation not found'}, status=status.HTTP_404_NOT_FOUND)
        
        payment = Payment.objects.get(reservation=reservation)
        payment.delete()
        reservation.delete()
        
        reservations = Reservation.objects.all()
        print(reservations, '>>>>>>>>>>>>>>>>>>>>>')
        reservations_data = ReservationSerializer(reservations, many=True).data
        
        if len(reservations_data) == 0:
            return Response({'reservations':reservations_data}, status=status.HTTP_200_OK) 
        
        print(reservations_data, '>>>>>>>>>>>>>>>>>>>>>')
        return Response({'reservations':reservations_data},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)