from django.shortcuts import render, get_object_or_404, redirect
from .models import Campaign, Challenge, User, Score
from django.contrib import messages
from .forms import ChallengeForm, UserForm
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth import login
from django.db.models import Sum
from django.contrib.auth.views import LogoutView
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError



class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']

def select_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        if role not in ['admin', 'broker']:
            messages.error(request, 'Selecione um papel válido.')
            return redirect('select_role')
        request.session['role'] = role
        return redirect('login')
    return render(request, 'gamification/select_role.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Verifica se o papel foi armazenado na sessão
        role = request.session.get('role')
        if not role:
            messages.error(request, 'Selecione seu papel primeiro.')
            return redirect('select_role')
        
        # Cria ou recupera o usuário com base no papel
        user, created = User.objects.get_or_create(username=username, defaults={'role': role})
        
        # Autentica o usuário sem validar a senha
        login(request, user)
        return redirect('dashboard')
    return render(request, 'gamification/login.html')

@login_required
def dashboard(request):
    role = getattr(request.user, 'role', 'unknown')  # Obtém o role ou 'unknown'

    print(f"Usuário logado: {request.user.username}, Role: {role}")  # Log para depuração

    if role == 'admin':
        context = {
            'role': 'admin',
            'buttons': [
                {'name': 'Gerenciar Usuários', 'url': 'manage_users'},
                {'name': 'Criar Desafios', 'url': 'create_challenge'},
                {'name': 'Atribuir Desafios', 'url': 'assign_challenge'},
                {'name': 'Visualizar Ranking Geral', 'url': 'ranking'},
            ]
        }
    elif role == 'broker':
        context = {
            'role': 'broker',
            'buttons': [
                {'name': 'Ver Desafios Atribuídos', 'url': 'broker_dashboard'},
                {'name': 'Aceitar Participar de Desafios', 'url': 'accept_challenge', 'param': 1},
                {'name': 'Visualizar Detalhes dos Desafios', 'url': 'challenge_detail', 'param': 1},
            ]
        }
    else:
        context = {'role': 'unknown', 'buttons': []}

    print(f"Contexto enviado: {context}")  # Log do contexto para depuração

    return render(request, 'gamification/dashboard.html', context)



@user_passes_test(lambda u: u.role == 'admin')
def create_challenge(request):
    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ChallengeForm()
    return render(request, 'gamification/create_challenge.html', {'form': form})


def campaign_list(request):
    campaigns = Campaign.objects.all()
    return render(request, 'gamification/campaign_list.html', {'campaigns': campaigns})

def campaign_detail(request, pk):
    campaign = get_object_or_404(Campaign, pk=pk)
    challenges = campaign.challenges.all()
    return render(request, 'gamification/campaign_detail.html', {'campaign': campaign, 'challenges': challenges})

@user_passes_test(lambda u: u.role == 'admin')
def manage_users(request):
    users = User.objects.all()
    return render(request, 'gamification/manage_users.html', {'users': users})

@login_required
def edit_user(request, user_id):
    # Verifique se o usuário tem permissão para editar
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        messages.error(request, "Você não tem permissão para editar usuários.")
        return redirect('manage_users')

    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuário atualizado com sucesso!")
            return redirect('manage_users')
    else:
        form = UserForm(instance=user)

    return render(request, 'gamification/edit_user.html', {'form': form, 'user': user})


@user_passes_test(lambda u: u.role == 'admin')
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        role = request.POST.get('role')
        password = request.POST.get('password')

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe!')
        else:
            User.objects.create_user(username=username, password=password, role=role)
            messages.success(request, 'Usuário criado com sucesso!')
        return redirect('manage_users')

    return render(request, 'gamification/add_user.html')


@login_required
def delete_user(request, user_id):
    # Verifica se o usuário é um administrador
    if not hasattr(request.user, 'role') or request.user.role != 'admin':
        messages.error(request, "Você não tem permissão para excluir usuários.")
        return redirect('manage_users')

    # Impede que o usuário logado se exclua
    if request.user.id == user_id:
        messages.error(request, "Você não pode excluir a si mesmo.")
        return redirect('manage_users')

    # Exclui o usuário
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.success(request, 'Usuário excluído com sucesso!')
    return redirect('manage_users')

@user_passes_test(lambda u: u.role == 'admin')
def assign_challenge(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        challenge_id = request.POST.get('challenge')
        user = User.objects.filter(username=cpf).first()
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        if user:
            challenge.assigned_users.add(user)
            messages.success(request, 'Desafio atribuído com sucesso!')
        else:
            messages.error(request, 'Usuário não encontrado.')
        return redirect('assign_challenge')
    challenges = Challenge.objects.all()
    return render(request, 'gamification/assign_challenge.html', {'challenges': challenges})

@login_required
def challenge_detail(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    return render(request, 'gamification/challenge_detail.html', {'challenge': challenge})

@login_required
def accept_challenge(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)

    # Verificar se o usuário já está participando do desafio
    if challenge.participants.filter(id=request.user.id).exists():
        messages.warning(request, "Você já está participando deste desafio.")
    else:
        challenge.participants.add(request.user)
        messages.success(request, 
  
"Você aceitou participar do desafio!")

    return redirect('broker_dashboard')  # Ou redirecione para onde você desejar

@login_required
def user_profile(request):
    return render(request, 'gamification/user_profile.html', {'user': request.user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('user_profile')
    return render(request, 'gamification/update_profile.html', {'user': request.user})

@login_required
def aceitar_desafio(request, challenge_id):
    # Obtém o desafio
    challenge = get_object_or_404(Challenge, id=challenge_id)

    # Verifica se o usuário já está participando
    if challenge.participants.filter(id=request.user.id).exists():
        messages.error(request, "Você já está participando deste desafio.")
        return redirect('broker_dashboard')  # Redireciona para o dashboard do corretor

    # Adiciona o usuário como participante
    challenge.participants.add(request.user)
    messages.success(request, "Você entrou no desafio com sucesso!")
    return redirect('broker_dashboard')  # Redireciona para o dashboard do corretor

from django.db.models import Sum
from django.shortcuts import render
from .models import Score

def ranking(request):
    rankings = (
        Score.objects.values('id', 'user__username')
        .annotate(total_points=Sum('points'))
        .order_by('-total_points')
    )

    # Adiciona posições e emojis
    rankings_with_positions = []
    for position, ranking in enumerate(rankings, start=1):
        ranking['position'] = position
        if position == 1:
            ranking['emoji'] = '🥇'
        elif position == 2:
            ranking['emoji'] = '🥈'
        elif position == 3:
            ranking['emoji'] = '🥉'
        else:
            ranking['emoji'] = ''
        rankings_with_positions.append(ranking)

    return render(request, 'gamification/ranking.html', {'rankings': rankings_with_positions})


def challenge_ranking(request, challenge_id):
    challenge = get_object_or_404(Challenge, id=challenge_id)
    rankings = (
        Score.objects.filter(challenge=challenge)
        .values('user__username')
        .annotate(total_points=Sum('points'))
        .order_by('-total_points')
    )
    rankings_with_positions = []
    for position, ranking in enumerate(rankings, start=1):
        ranking['position'] = position
        if position == 1:
            ranking['emoji'] = '🥇'
        elif position == 2:
            ranking['emoji'] = '🥈'
        elif position == 3:
            ranking['emoji'] = '🥉'
        else:
            ranking['emoji'] = ''
        rankings_with_positions.append(ranking)
    return render(request, 'gamification/classificacao_desafio.html', {
        'challenge': challenge,
        'rankings': rankings_with_positions,
    })


@user_passes_test(lambda u: u.role == 'admin')
def admin_dashboard(request):
    challenges = Challenge.objects.all()
    return render(request, 'gamification/admin_dashboard.html', {
        'challenges': challenges,
        'buttons': [
            {'name': 'Ver Ranking Geral', 'url': 'ranking'},
            *[{'name': f'Ranking do Desafio: {challenge.title}', 'url': 'challenge_ranking', 'param': challenge.id} for challenge in challenges]
        ]
    })
class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']

@login_required
def view_ranking(request):
    rankings = (
        Score.objects.all()
        .values('user__username', 'challenge__title')  # Agrupa por usuário e desafio
        .annotate(total_points=Sum('points'))  # Soma os pontos
        .order_by('-total_points')  # Ordena por pontuação
    )

    can_edit = request.user.role == 'admin'  # Verifica se o usuário é administrador

    return render(
        request,
        'gamification/ranking_geral.html',
        {
            'rankings': rankings,
            'can_edit': can_edit,  # Passa a permissão de edição para o template
        },
    )

@user_passes_test(lambda u: u.role == 'admin')  # Apenas administradores podem editar
def edit_score(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    if request.method == 'POST':
        new_points = request.POST.get('points')
        score.points = new_points
        score.save()
        messages.success(request, "Pontuação atualizada com sucesso!")
        return redirect('ranking_geral')
    return render(request, 'gamification/edit_score.html', {'score': score})

@user_passes_test(lambda u: u.role == 'admin')  # Apenas administradores podem excluir
def delete_score(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    score.delete()
    messages.success(request, "Pontuação excluída com sucesso!")
    return redirect('ranking_geral')

def broker_dashboard(request):
    challenges = Challenge.objects.filter(participants=request.user)
    return render(request, 'gamification/broker_dashboard.html', {
        'challenges': challenges,
        'buttons': [
            {'name': 'Visualizar Ranking Geral', 'url': 'ranking'},
        ]
    })
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role', 'broker')  # Define um papel padrão para novos usuários

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe!')
        else:
            # Cria o usuário com senha criptografada
            User.objects.create(
                username=username,
                password=make_password(password),
                role=role,
            )
            messages.success(request, 'Usuário cadastrado com sucesso! Faça login para continuar.')
        return redirect('login')

    return render(request, 'gamification/register.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cpf = request.POST.get('cpf')
        role = request.POST.get('role', 'broker')  # Define o papel padrão como 'broker'

        # Verifica se o CPF está preenchido
        if not cpf or len(cpf) != 11:
            messages.error(request, 'CPF é obrigatório e deve conter 11 dígitos.')
            return render(request, 'gamification/register.html')

        # Verifica se o CPF já existe
        if User.objects.filter(cpf=cpf).exists():
            messages.error(request, 'CPF já cadastrado.')
            return render(request, 'gamification/register.html')

        # Verifica se o usuário já existe
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Usuário já existe.')
        else:
            # Cria o novo usuário
            user = User.objects.create_user(
                username=username,
                password=password,
                cpf=cpf,
                role=role,
            )
            login(request, user)  # Faz login automático após registro
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('dashboard')  # Redireciona para o dashboard

    return render(request, 'gamification/register.html')


@user_passes_test(lambda u: u.role == 'admin')
def edit_score(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    if request.method == 'POST':
        new_points = request.POST.get('points')
        score.points = new_points
        score.save()
        messages.success(request, "Pontuação atualizada com sucesso!")
        return redirect('ranking')  # Certifique-se de que 'ranking_geral' existe
    return render(request, 'gamification/edit_score.html', {'score': score})  # Certifique-se de que 'ranking_geral' existe no urls.py

def add_points(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    if request.method == 'POST':
        points = request.POST.get('points')
        try:
            points = int(points)
            score.points += points  # Adiciona os pontos ao score atual
            score.save()
            messages.success(request, f'{points} pontos adicionados ao usuário {score.user.username} com sucesso!')
        except ValueError:
            messages.error(request, 'Insira um valor válido para os pontos.')
        return redirect('ranking')  # Redireciona para o ranking geral
    return render(request, 'gamification/add_points.html', {'score': score})

@user_passes_test(lambda u: u.role == 'admin')  # Apenas administradores podem excluir
def delete_broker_from_ranking(request, score_id):
    score = get_object_or_404(Score, id=score_id)
    user = score.user
    if request.method == 'POST':
        score.delete()
        messages.success(request, f'O corretor {user.username} foi removido do ranking com sucesso!')
        return redirect('ranking_geral')  # Redireciona para o ranking geral
    return render(request, 'gamification/confirm_delete_broker.html', {'user': user})

