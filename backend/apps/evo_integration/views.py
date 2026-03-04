import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Member, WorkoutSession

@csrf_exempt
def evo_webhook(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Eduardo Job: Inserir lógica de processamento do JSON da EVO aqui
            print("Payload recebido da EVO:", data) 
            return JsonResponse({"status": "sucesso", "mensagem": "Webhook recebido"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"erro": "Payload inválido"}, status=400)
    
    return JsonResponse({"erro": "Método não permitido"}, status=405)