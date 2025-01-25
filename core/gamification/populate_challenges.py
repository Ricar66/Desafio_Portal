from django.core.management.base import BaseCommand
from gamification.models import Challenge, User, Score

class Command(BaseCommand):
    help = 'Popula o banco de dados com desafios e pontuações fictícias'

    def handle(self, *args, **kwargs):
        # Adicionando desafios
        superacao = Challenge.objects.create(
            title="Superação 2025",
            description="Participe do desafio para alcançar metas incríveis em 2025!",
            points=500
        )
        vendas = Challenge.objects.create(
            title="Vendas Extraordinárias",
            description="Um desafio para os melhores vendedores do mês!",
            points=300
        )

        # Criando usuários fictícios
        joao = User.objects.create(username="João Silva")
        maria = User.objects.create(username="Maria Santos")
        ana = User.objects.create(username="Ana Oliveira")
        carlos = User.objects.create(username="Carlos Souza")
        fernanda = User.objects.create(username="Fernanda Lima")

        # Adicionando pontuações
        Score.objects.create(user=joao, challenge=superacao, points=450)
        Score.objects.create(user=maria, challenge=superacao, points=420)
        Score.objects.create(user=ana, challenge=superacao, points=380)
        Score.objects.create(user=carlos, challenge=superacao, points=350)
        Score.objects.create(user=joao, challenge=vendas, points=280)
        Score.objects.create(user=carlos, challenge=vendas, points=260)
        Score.objects.create(user=ana, challenge=vendas, points=240)
        Score.objects.create(user=fernanda, challenge=vendas, points=230)

        self.stdout.write(self.style.SUCCESS('Banco de dados populado com sucesso!'))
