from django.contrib import admin
from .models import Member, WorkoutSession, Instructor

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_on_shift')
    list_filter = ('is_on_shift',)
    search_fields = ('name',)

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('evo_id', 'name', 'created_at')
    search_fields = ('name', 'evo_id')

@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ('member', 'instructor', 'check_in_time', 'check_out_time', 'is_active')
    list_filter = ('is_active', 'instructor')