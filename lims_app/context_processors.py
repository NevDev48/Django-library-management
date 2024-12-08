from .models import reader  # Import model reader

def current_user(request):
    reference_id = request.session.get('reference_id')
    current_user = None
    if reference_id:
        try:
            current_user = reader.objects.get(reference_id=reference_id)
        except reader.DoesNotExist:
            current_user = None
    return {'current_user': current_user}
