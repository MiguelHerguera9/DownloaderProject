#from django.shortcuts import render

#def index(request):
    #return render(request, 'index.html')
from django.http import JsonResponse
from django.shortcuts import render

def index(request):
    if request.method == 'POST':
        # Obtener las URLs del formulario
        urls = request.POST.get('urls', '')  # Campo del formulario
        print(f"URLs recibidas: {urls}")  # Imprime en la consola del servidor
        return JsonResponse({'message': 'Datos recibidos correctamente', 'data': urls})
    return render(request, 'index.html')
