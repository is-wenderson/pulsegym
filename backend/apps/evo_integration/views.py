import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Q, F
from .models import Member, Instructor, WorkoutSession

@csrf_exempt
def evo_webhook(request):
    if request.method != 'POST':
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        data = json.loads(request.body)
        
        # Aceita 'usuario_id' ou 'aluno_id' para flexibilidade
        usuario_id = str(data.get("usuario_id") or data.get("aluno_id"))
        nome = data.get("nome", "Usuário Desconhecido")
        tipo_evento = data.get("evento")
        tipo_usuario = data.get("tipo_usuario", "aluno") # Define 'aluno' como padrão se a EVO não mandar

        if not usuario_id or not tipo_evento:
            return JsonResponse({"erro": "Payload ausente de campos obrigatórios"}, status=400)

        # --- FLUXO 1: É UM INSTRUTOR PASSANDO NA CATRACA ---
        if tipo_usuario == "instrutor":
            instrutor, created = Instructor.objects.get_or_create(
                evo_id=usuario_id,
                defaults={'name': nome, 'max_capacity': 5} # Capacidade padrão é 5
            )
            
            if tipo_evento == "checkin":
                instrutor.is_on_shift = True
                instrutor.save()
                return JsonResponse({"status": "sucesso", "acao": "Instrutor online no salão", "nome": instrutor.name}, status=200)
            elif tipo_evento == "checkout":
                instrutor.is_on_shift = False
                instrutor.save()
                return JsonResponse({"status": "sucesso", "acao": "Instrutor offline (Fim de turno)"}, status=200)

        # --- FLUXO 2: É UM ALUNO PASSANDO NA CATRACA ---
        elif tipo_usuario == "aluno":
            member, created = Member.objects.get_or_create(
                evo_id=usuario_id,
                defaults={'name': nome}
            )

            if tipo_evento == "checkin":
                session_ativa = WorkoutSession.objects.filter(member=member, is_active=True).first()
                if session_ativa:
                    return JsonResponse({"status": "ignorado", "mensagem": "Aluno já possui treino em andamento"}, status=200)

                # ALGORITMO COM TRAVA (RF07)
                # Pega instrutores online, conta os alunos ativos de cada um, e FILTRA excluindo quem já bateu a capacidade máxima
                instrutores_disponiveis = Instructor.objects.filter(is_on_shift=True).annotate(
                    active_students=Count('workoutsession', filter=Q(workoutsession__is_active=True))
                ).filter(active_students__lt=F('max_capacity')).order_by('active_students')
                
                instrutor_escolhido = instrutores_disponiveis.first() 

                WorkoutSession.objects.create(
                    member=member,
                    instructor=instrutor_escolhido,
                    check_in_time=timezone.now(),
                    is_active=True
                )
                
                # RF04/RF05: Se todos estiverem lotados, instrutor_escolhido será None (Fila de espera)
                mensagem = f"Atribuído a {instrutor_escolhido.name}" if instrutor_escolhido else "Fila de espera (Todos lotados)"

                return JsonResponse({"status": "sucesso", "acao": "Treino iniciado", "detalhe": mensagem}, status=200)

            # --- FLUXO 1: É UM INSTRUTOR PASSANDO NA CATRACA ---
        if tipo_usuario == "instrutor":
            instrutor, created = Instructor.objects.get_or_create(
                evo_id=usuario_id,
                defaults={'name': nome, 'max_capacity': 5}
            )
            
            if tipo_evento == "checkin":
                instrutor.is_on_shift = True
                instrutor.save()
                return JsonResponse({"status": "sucesso", "acao": "Instrutor online no salão", "nome": instrutor.name}, status=200)
            
            elif tipo_evento == "checkout":
                # 1. Desliga o turno do professor
                instrutor.is_on_shift = False
                instrutor.save()

                # 2. ALGORITMO DE REATRIBUIÇÃO (RF17)
                # Busca todos os alunos que estavam treinando com este professor
                alunos_orfaos = WorkoutSession.objects.filter(instructor=instrutor, is_active=True)
                reatribuidos = 0
                para_fila = 0

                for sessao in alunos_orfaos:
                    # Roda a roleta para achar quem tem a menor fila e ainda tem vaga
                    novo_instrutor = Instructor.objects.filter(is_on_shift=True).annotate(
                        active_students=Count('workoutsession', filter=Q(workoutsession__is_active=True))
                    ).filter(active_students__lt=F('max_capacity')).order_by('active_students').first()

                    # Transfere o aluno
                    sessao.instructor = novo_instrutor
                    sessao.save()

                    if novo_instrutor:
                        reatribuidos += 1
                    else:
                        para_fila += 1

                mensagem = f"Fim de turno. {reatribuidos} alunos realocados, {para_fila} foram para a fila de espera."
                return JsonResponse({"status": "sucesso", "acao": "Instrutor offline", "detalhe": mensagem}, status=200)

        return JsonResponse({"erro": "Tipo de evento ou usuário inválido"}, status=400)

    except Exception as e:
        return JsonResponse({"erro_interno": str(e)}, status=500)
    

def tv_dashboard_api(request):
    if request.method != 'GET':
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    # 1. Pega os instrutores online
    instrutores = Instructor.objects.filter(is_on_shift=True)
    dados_instrutores = []
    
    for inst in instrutores:
        # Busca os alunos ativos com este professor específico
        alunos_ativos = WorkoutSession.objects.filter(instructor=inst, is_active=True)
        dados_instrutores.append({
            "nome": inst.name,
            "capacidade": inst.max_capacity,
            "ocupacao": alunos_ativos.count(),
            "alunos": [s.member.name for s in alunos_ativos]
        })

    # 2. Pega a Fila de Espera (Alunos ativos, mas sem professor vinculado)
    espera = WorkoutSession.objects.filter(is_active=True, instructor__isnull=True)
    dados_espera = [s.member.name for s in espera]

    return JsonResponse({
        "instrutores": dados_instrutores,
        "fila_espera": dados_espera,
        "total_ativos": WorkoutSession.objects.filter(is_active=True).count()
    })