from django.contrib.auth.models import AbstractUser, Group, Permission, BaseUserManager
from django.db import models
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, role='broker', **extra_fields):
        if not username:
            raise ValueError("O campo 'username' é obrigatório")
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        return self.create_user(username, password, role='admin', **extra_fields)

from django.core.validators import RegexValidator

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('broker', 'Corretor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='broker', blank=False, null=False)

    # Novos campos
    birth_date = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    city = models.CharField(max_length=100, blank=True, verbose_name="Cidade")
    state = models.CharField(max_length=100, blank=True, verbose_name="Estado")
    cep = models.CharField(
        max_length=9,
        blank=True,
        verbose_name="CEP",
        validators=[RegexValidator(r'^\d{5}-\d{3}$', message="Formato do CEP inválido. Use o formato 12345-678.")]
    )
    street = models.CharField(max_length=200, blank=True, verbose_name="Rua")

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
    )

    objects = UserManager()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Modelo de Campanha
class Campaign(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"
        ordering = ['-start_date']  # Ordena por data de início, mais recente primeiro

    def __str__(self):
        return self.name

# Modelo de Desafio
class Challenge(models.Model):
    campaign = models.ForeignKey(
        Campaign, 
        on_delete=models.CASCADE, 
        related_name='challenges'
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    points = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)  # Identidade visual
    evaluation_rules = models.TextField(blank=True, null=True)  # Regras de avaliação
    assigned_users = models.ManyToManyField('User', related_name='assigned_challenges', blank=True)  # Usuários atribuídos
    participants = models.ManyToManyField('User', related_name='participating_challenges', blank=True)  # Participantes

    class Meta:
        verbose_name = "Challenge"
        verbose_name_plural = "Challenges"
        ordering = ['-points']  # Ordena por pontos, maior primeiro

    def __str__(self):
        return f"{self.title} ({self.campaign.name})"

# Modelo de Pontuação
class Score(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='scores'
    )
    challenge = models.ForeignKey(
        Challenge, 
        on_delete=models.CASCADE, 
        related_name='scores'
    )
    points = models.PositiveIntegerField(default=0)
    date_earned = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Score"
        verbose_name_plural = "Scores"
        unique_together = ('user', 'challenge')  # Garante que o mesmo usuário não ganhe pontuação duplicada para um desafio
        ordering = ['-date_earned']  # Ordena por data de pontuação, mais recente primeiro

    def __str__(self):
        return f"{self.user.username} - {self.challenge.title} ({self.points} pontos)"

# Dashboards
@login_required
def dashboard(request):
    print(f"Usuário logado: {request.user.username}, Role: {request.user.role}")
    
    if request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'broker':
        return redirect('broker_dashboard')
    else:
        return render(request, 'gamification/dashboard.html', {
            'role': 'unknown',
            'buttons': [],
        })


@login_required
def broker_dashboard(request):
    challenges = Challenge.objects.filter(assigned_users=request.user)
    return render(request, 'gamification/broker_dashboard.html', {
        'challenges': challenges,
        'buttons': [
            {'name': 'Aceitar Desafios', 'url': 'accept_challenge'},
            {'name': 'Ver Desafios Atribuídos', 'url': 'broker_dashboard'},
            {'name': 'Visualizar Detalhes do Desafio', 'url': 'challenge_detail'},
        ]
    })
