from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


schema_view = get_schema_view(
   openapi.Info(
      title="Motor de reserva de hoteles API",
      default_version='v1',
      description="api para el motor de reserva de hoteles",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="orestelopez96@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/hotel/', include('hotel.api.urls')),
    path('api/v1/room/', include('habitacion.api.urls')),
    path('api/v1/reservation/', include('reservation.api.urls')),
    path('api/v1/payment/', include('payment.api.urls')),
    path('api/v1/user/', include('user.api.urls')),
    
    
    #Rutas para obtener doc de la api
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
