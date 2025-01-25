# Desafio Portal de Gamificação

Este projeto é um portal de gamificação desenvolvido para permitir que administradores criem campanhas e desafios, enquanto corretores participam e acumulam pontos para competir em rankings. O objetivo principal é engajar os usuários por meio de desafios e recompensas.

## **Funcionalidades Principais**

### **Para Administradores:**
- Criar campanhas com detalhes como nome, descrição, data de início e término.
- Criar desafios vinculados a campanhas, com pontuações específicas e regras de avaliação.
- Gerenciar usuários (adicionar, editar e excluir).
- Visualizar e editar rankings de pontuação.

### **Para Corretores:**
- Visualizar campanhas e desafios atribuídos.
- Aceitar desafios e participar para acumular pontos.
- Visualizar seu ranking no leaderboard.

---

## **Tecnologias Utilizadas**
- **Backend:** Python, Django
- **Frontend:** HTML, CSS (Bootstrap)
- **Banco de Dados:** MySQL
- **Controle de Versão:** Git
- **Deploy:** (Se aplicável, adicionar detalhes do deploy)

---

## **Instalação e Configuração**

### **Pré-requisitos**
1. Python 3.10 ou superior.
2. MySQL configurado e rodando.
3. Node.js (opcional, para gerenciamento de dependências do frontend).

### **Passos para Configuração**
1. Clone o repositório:
   ```bash
   git clone https://github.com/Ricar66/Desafio_Portal_Gamificacao.git
   ```
2. Entre no diretório do projeto:
   ```bash
   cd Desafio_Portal_Gamificacao
   ```
3. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # No Windows
   source .venv/bin/activate  # No macOS/Linux
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
5. Configure o banco de dados no arquivo `settings.py`.
6. Aplique as migrações:
   ```bash
   python manage.py migrate
   ```
7. Crie um superusuário para acesso administrativo:
   ```bash
   python manage.py createsuperuser
   ```
8. Inicie o servidor:
   ```bash
   python manage.py runserver
   ```

---

## **Uso do Portal**
1. Acesse o portal em [http://localhost:8000](http://localhost:8000).
2. Faça login como administrador ou corretor.
3. Navegue pelas funcionalidades de acordo com seu papel no sistema.

---

## **Estrutura do Projeto**

- **`gamification/`**: Aplicação principal do projeto.
  - **`models.py`**: Contém os modelos principais como `User`, `Campaign`, `Challenge` e `Score`.
  - **`views.py`**: Lida com as requisições e as respostas.
  - **`urls.py`**: Configura as rotas do sistema.
- **`templates/`**: Contém os arquivos HTML para as páginas do sistema.
- **`static/`**: Contém os arquivos CSS, JS e imagens do projeto.

---

## **Contribuições**
Contribuições são bem-vindas! Siga os passos abaixo para contribuir:
1. Faça um fork do projeto.
2. Crie uma nova branch para suas alterações:
   ```bash
   git checkout -b minha-feature
   ```
3. Commit suas alterações:
   ```bash
   git commit -m "Descrição da minha feature"
   ```
4. Envie para o repositório remoto:
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request.

---

## **Licença**
Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais informações.
