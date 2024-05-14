def reserva_habitacion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        habitacion_id = data.get('habitacion_id')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')

        # Verificar si ya existe una reserva para esta habitación que se solape con el rango de fechas seleccionado
        if Reserva.objects.filter(habitacion_id=habitacion_id, fecha_inicio__lte=fecha_fin, fecha_fin__gte=fecha_inicio).exists():
            return JsonResponse({'error': 'La habitación ya está reservada para este período'}, status=400)

        # Crear la reserva si no hay conflictos
        reserva = Reserva.objects.create(habitacion_id=habitacion_id, cliente=request.user, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
        return JsonResponse({'message': 'Reserva creada exitosamente'}, status=201)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)