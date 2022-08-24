from sliced.models import services


def add_variable_to_context(request):
    if "cart" in request.session:
        a = len(set(request.session['cart']))
    else:
        a = 0
    return {
         'serviceData': services.objects.all(),
         'cartTotal': a
     }
