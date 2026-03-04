from django.db import models

class Member(models.Model):
    evo_id = models.CharField(max_length=50, unique=True, verbose_name="ID EVO")
    name = models.CharField(max_length=255, verbose_name="Nome do Aluno")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.evo_id})"

class WorkoutSession(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='sessions')
    check_in_time = models.DateTimeField(verbose_name="Horário de Entrada")
    check_out_time = models.DateTimeField(null=True, blank=True, verbose_name="Horário de Saída")
    is_active = models.BooleanField(default=True, verbose_name="Treino em Andamento")
    
    def __str__(self):
        return f"Treino: {self.member.name} - {self.check_in_time.strftime('%d/%m/%Y %H:%M')}"