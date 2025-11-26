
# TaskFlow Backend

Service backend FastAPI avec stockage progressif :
- **Atelier 1-2** : Stockage en mémoire (dictionnaire Python simple)
- **Atelier 3** : Migration vers PostgreSQL pour la persistance

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.11+
- [Gestionnaire de paquets UV](https://docs.astral.sh/uv/)
- PostgreSQL (optionnel - seulement pour Atelier 3)

### Installation

```bash
# Installer les dépendances
uv sync

# Copier les variables d'environnement (optionnel)
cp .env.example .env
```

### Lancement Local

#### Pour Atelier 1 & 2 : Stockage en Mémoire (Le Plus Simple)

```bash
# Démarrer le serveur (utilise un dictionnaire Python en mémoire)
uv run uvicorn src.app:app --reload
```

L'API sera disponible sur :

- **API** : <http://localhost:8000>
- **Documentation** : <http://localhost:8000/docs>
- **Health Check** : <http://localhost:8000/health>

**Important :** Les données sont **perdues** quand vous arrêtez le serveur. C'est normal pour Atelier 1-2 !

#### Pour Atelier 3 : Avec PostgreSQL (Comme en Production)

1. **Démarrer PostgreSQL avec Docker :**

```bash
docker run --name taskflow-postgres \
  -e POSTGRES_DB=taskflow_dev \
  -e POSTGRES_USER=taskflow \
  -e POSTGRES_PASSWORD=dev_password \
  -p 5432:5432 \
  -d postgres:15
```

2. **Modifier app.py pour utiliser la base de données :**

Vous devrez modifier `src/app.py` pour utiliser `database.py` et `models.py` au lieu du stockage en mémoire. Voir le guide de migration dans l'Atelier 3.

3. **Mettre à jour .env :**

```bash
DATABASE_URL=postgresql://taskflow:dev_password@localhost:5432/taskflow_dev
```

4. **Démarrer le serveur :**

```bash
uv run uvicorn src.app:app --reload
```

### Gestion de la Base de Données

#### Pour Atelier 1 & 2 : Rien à Faire !

Le stockage en mémoire ne nécessite aucune configuration. Les données sont automatiquement nettoyées entre les tests.

#### Pour Atelier 3 : Initialiser PostgreSQL

La base de données sera automatiquement initialisée au démarrage de l'application. Pour initialiser manuellement :

```bash
uv run python src/db_init.py
```

#### Réinitialiser la Base (Développement Uniquement)

⚠️ **Attention** : Cela supprimera toutes les données !

```bash
uv run python src/db_init.py --reset
```

### Lancement des Tests

```bash
# Lancer tous les tests
uv run pytest

# Lancer avec couverture de code
uv run pytest --cov=src --cov-report=html

# Lancer un fichier de test spécifique
uv run pytest tests/test_api.py -v

# Lancer avec sortie détaillée
uv run pytest -vv
```

Les tests utilisent le stockage en mémoire, donc aucune base de données n'est nécessaire pour les tests !

## 📁 Structure du Projet

```text
backend/
├── src/
│   ├── app.py           # Application FastAPI & endpoints (stockage en mémoire)
│   ├── database.py      # Configuration base de données (Atelier 3)
│   ├── models.py        # Modèles SQLAlchemy ORM (Atelier 3)
│   ├── db_init.py       # Scripts d'initialisation DB (Atelier 3)
│   └── __init__.py
├── tests/
│   ├── conftest.py      # Fixtures pytest & configuration
│   ├── test_api.py      # Tests des endpoints API (19 tests)
│   └── __init__.py
├── pyproject.toml       # Dépendances & configuration
├── .env.example         # Template variables d'environnement
├── .gitignore
└── README.md
```

**Note :** Les fichiers `database.py`, `models.py` et `db_init.py` sont prêts pour l'Atelier 3 mais **non utilisés** dans Atelier 1-2.

## 🗄️ Stockage des Données

### Atelier 1 & 2 : Stockage en Mémoire

Les tâches sont stockées dans un simple dictionnaire Python :

```python
tasks_db: Dict[int, Task] = {}
next_id = 1  # Auto-incrémentation des IDs
```

**Avantages :**
- Simple à comprendre
- Aucune configuration nécessaire
- Parfait pour apprendre les tests

**Inconvénient :**
- Les données sont perdues au redémarrage (c'est intentionnel !)

### Atelier 3 : Base de Données PostgreSQL

**Table : tasks**

| Colonne | Type | Contraintes |
|--------|------|-------------|
| id | Integer | PRIMARY KEY |
| title | String(200) | NOT NULL |
| description | String(1000) | NULL |
| status | Enum | NOT NULL, DEFAULT 'todo' |
| priority | Enum | NOT NULL, DEFAULT 'medium' |
| assignee | String(100) | NULL |
| due_date | DateTime | NULL |
| created_at | DateTime | NOT NULL, DEFAULT now() |
| updated_at | DateTime | NOT NULL, ON UPDATE now() |

**Enums :**
- **TaskStatus** : `todo`, `in_progress`, `done`
- **TaskPriority** : `low`, `medium`, `high`

## 🔧 Configuration

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Environment
ENVIRONMENT=development

# Database
DATABASE_URL=sqlite:///./taskflow.db

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Debug
DEBUG=true
LOG_LEVEL=INFO
```

### Render Production Variables

In Render dashboard, set:

```bash
ENVIRONMENT=production
DATABASE_URL=<provided-by-render>
CORS_ORIGINS=https://taskflow-frontend-XXXX.onrender.com
DEBUG=false
```

## 📚 API Endpoints

### Health Check

```bash
GET /health
```

### Tasks

```bash
# List all tasks
GET /tasks
GET /tasks?status=todo
GET /tasks?priority=high&assignee=john

# Create task
POST /tasks
Content-Type: application/json
{
  "title": "New task",
  "description": "Task description",
  "status": "todo",
  "priority": "medium"
}

# Get task
GET /tasks/{task_id}

# Update task
PUT /tasks/{task_id}
Content-Type: application/json
{
  "status": "in_progress",
  "assignee": "alice"
}

# Delete task
DELETE /tasks/{task_id}
```

## 🧪 Testing

### Test Configuration

Tests use:
- **In-memory SQLite** database
- **Fresh database** for each test
- **Dependency injection** override for test DB

### Writing Tests

```python
def test_create_task(client):
    """Test creating a task."""
    response = client.post("/tasks", json={
        "title": "Test task",
        "status": "todo",
        "priority": "high"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
```

### Database Fixtures

```python
def test_with_database(db_session):
    """Test using database directly."""
    task = TaskModel(id="1", title="Test")
    db_session.add(task)
    db_session.commit()

    result = db_session.query(TaskModel).first()
    assert result.title == "Test"
```

## 🚀 Deployment

### Render Configuration

**Build Command:**
```bash
pip install uv && uv sync
```

**Start Command:**
```bash
uv run uvicorn src.app:app --host 0.0.0.0 --port $PORT
```

### Database Setup on Render

1. Create PostgreSQL database on Render
2. Add `DATABASE_URL` environment variable to web service
3. Deploy - tables are created automatically on startup

## 🔍 Debugging

### Check Database Connection

```bash
curl http://localhost:8000/health
```

Should return `"database": "connected"`.

### Access PostgreSQL

```bash
# Via Docker
docker exec -it taskflow-postgres psql -U taskflow -d taskflow_dev

# Via Render (get command from dashboard)
PGPASSWORD=<password> psql -h <host> -U <user> <database>
```

### SQL Queries

```sql
-- List all tasks
SELECT * FROM tasks;

-- Count tasks by status
SELECT status, COUNT(*) FROM tasks GROUP BY status;

-- Show table schema
\d tasks
```

## 📝 Common Commands

```bash
# Development
uv run uvicorn src.app:app --reload        # Start dev server
uv run pytest -v                           # Run tests
uv run pytest --cov=src                    # Test with coverage

# Database
uv run python src/db_init.py               # Initialize DB
uv run python src/db_init.py --reset       # Reset DB

# Dependencies
uv add <package>                           # Add dependency
uv sync                                    # Install dependencies
uv lock                                    # Update lock file
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'sqlalchemy'"

**Solution:**
```bash
uv sync
```

### Issue: "Relation 'tasks' does not exist"

**Solution:** Tables not created. Restart the app or run:
```bash
uv run python src/db_init.py
```

### Issue: "Connection refused" to PostgreSQL

**Solution:** Check that PostgreSQL is running:
```bash
docker ps  # Should show taskflow-postgres
```

### Issue: Tests fail with database errors

**Solution:** Tests use in-memory DB. Check `conftest.py` fixtures are correct.

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [UV Package Manager](https://docs.astral.sh/uv/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📄 License

Educational material for workshops.

---

**Version 2.2.0** - With PostgreSQL Integration 🚀
