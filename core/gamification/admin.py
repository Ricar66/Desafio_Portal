from django.contrib import admin
from .models import Campaign, Challenge, User, Score

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')
    search_fields = ('name',)
    list_filter = ('start_date', 'end_date')

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title', 'campaign', 'points', 'is_active')
    search_fields = ('title', 'campaign__name')  # Permite buscar pelo título e campanha
    list_filter = ('is_active', 'campaign')  # Filtros para facilitar a navegação
    readonly_fields = ('id',)  # Torna o ID somente leitura
    fieldsets = (  # Organiza os campos em grupos
        ('Informações do Desafio', {
            'fields': ('title', 'description', 'campaign', 'banner', 'points', 'evaluation_rules')
        }),
        ('Status', {
            'fields': ('is_active',),
        }),
    )

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role', 'is_active')

@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'points', 'date_earned')
    search_fields = ('user__username', 'challenge__title')
    list_filter = ('date_earned',)



# Register your models here.
