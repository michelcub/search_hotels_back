from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from payment.models import Payment

from payment.api.serializer import PaymentSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def create_payment(request):
    try:
        data = request.data
        amount = data.get('amount', None)
        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        payment = Payment.objects.create(amount=amount)
        
        if not payment:
            return Response({'error': 'Payment not created'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    except Exception as e:
        print('error al realizar el pago>>>>>>>>>>>>', str(e))
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)