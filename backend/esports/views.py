from django.shortcuts import render

def formulario_usuario(request):
    return render(request, 'pages/usuarios_formulario.html')
