from django.db import models
from django.utils import timezone

class Member(models.Model):
    evo_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Agora o painel vai mostrar: [ALU-99] Wenderson Cunha
        return f"[{self.evo_id}] {self.name}"

class Instructor(models.Model):
    name = models.CharField(max_length=255)
    evo_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_on_shift = models.BooleanField(default=False, help_text="Online no turno")
    # NOVA COLUNA: Define o limite do RF07
    max_capacity = models.IntegerField(default=5, help_text="Limite máximo de alunos simultâneos")

    def __str__(self):
        status = "🟢 No Salão" if self.is_on_shift else "🔴 Ausente"
        return f"{self.name} - {status} (Capacidade: {self.max_capacity})"

class WorkoutSession(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    check_in_time = models.DateTimeField(default=timezone.now)
    check_out_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        prof = self.instructor.name if self.instructor else "Sem professor"
        return f"{self.member.name} (Atendido por: {prof})"