"""
Tests API TaskFlow - Atelier 1 Starter

Apprenez en faisant ! Ce fichier vous montre comment écrire des tests, puis vous en écrirez de similaires.

Structure de chaque test :
1. ARRANGE - Préparer les données de test
2. ACT - Faire la requête API
3. ASSERT - Vérifier la réponse
"""

import pytest


# =============================================================================
# PARTIE 1 : TESTS EXEMPLES (Apprenez de ceux-ci !)
# =============================================================================

def test_root_endpoint(client):
    """
    EXEMPLE : Tester un point de terminaison GET simple.

    Ce test vous montre le pattern de base :
    1. Faire une requête avec client.get()
    2. Vérifier le code de statut
    3. Vérifier les données de la réponse
    """
    # ACT : Faire une requête GET
    response = client.get("/")

    # ASSERT : Vérifier la réponse
    assert response.status_code == 200
    assert "Welcome to TaskFlow API" in response.json()["message"]


def test_health_check(client):
    """EXEMPLE : Un autre test de point de terminaison GET simple."""
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task(client):
    """
    EXEMPLE : Tester un point de terminaison POST (création de données).

    Pattern pour les requêtes POST :
    1. Préparer les données comme un dictionnaire Python
    2. Les envoyer avec client.post()
    3. Vérifier le code de statut (201 = Créé)
    4. Vérifier les données retournées
    """
    # ARRANGE : Préparer les données
    new_task = {
        "title": "Acheter des courses",
        "description": "Lait, œufs, pain"
    }

    # ACT : Envoyer la requête POST
    response = client.post("/tasks", json=new_task)

    # ASSERT : Vérifier la réponse
    assert response.status_code == 201  # 201 = Créé

    task = response.json()
    assert task["title"] == "Acheter des courses"
    assert task["description"] == "Lait, œufs, pain"
    assert task["status"] == "todo"  # Valeur par défaut
    assert "id" in task  # Le serveur génère un ID


def test_list_tasks(client):
    """
    EXEMPLE : Tester GET avec préparation de données.

    Parfois vous devez créer des données d'abord, puis tester leur listage.
    """
    # ARRANGE : Créer quelques tâches d'abord
    client.post("/tasks", json={"title": "Tâche 1"})
    client.post("/tasks", json={"title": "Tâche 2"})

    # ACT : Obtenir la liste des tâches
    response = client.get("/tasks")

    # ASSERT : Vérifier qu'on a bien les deux tâches
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_get_task_by_id(client):
    """
    EXEMPLE : Tester GET pour une ressource spécifique.

    Pattern :
    1. Créer une tâche d'abord
    2. Obtenir son ID depuis la réponse
    3. Utiliser cet ID pour récupérer la tâche
    """
    # ARRANGE : Créer une tâche
    create_response = client.post("/tasks", json={"title": "Trouve-moi"})
    task_id = create_response.json()["id"]

    # ACT : Obtenir la tâche spécifique
    response = client.get(f"/tasks/{task_id}")

    # ASSERT : Vérifier qu'on a la bonne tâche
    assert response.status_code == 200
    assert response.json()["title"] == "Trouve-moi"


# =============================================================================
# PARTIE 2 : À VOUS ! Complétez ces tests
# =============================================================================

# EXERCICE 1 : Écrire un test pour SUPPRIMER une tâche
# Pattern : Créer → Supprimer → Vérifier qu'elle a disparu
def test_delete_task(client):
    """
    VOTRE TÂCHE : Écrire un test qui supprime une tâche.

    Étapes :
    1. Créer une tâche (comme dans test_create_task)
    2. Obtenir son ID
    3. Envoyer une requête DELETE : client.delete(f"/tasks/{task_id}")
    4. Vérifier que le code de statut est 204 (No Content)
    5. Essayer de GET la tâche à nouveau → devrait retourner 404 (Not Found)

    Astuce : Regardez test_get_task_by_id pour voir comment créer et obtenir l'ID
    """
    # TODO : Écrivez votre test ici !
    create_task = client.post("/tasks", json={'title':"tâche 1"})
    task_id = create_task.json()["id"]

    response_delete = client.delete(f"/tasks/{task_id}")
    assert response_delete.status_code == 204

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404



# EXERCICE 2 : Écrire un test pour METTRE À JOUR une tâche
# Pattern : Créer → Mettre à jour → Vérifier les changements
def test_update_task(client):
    """
    VOTRE TÂCHE : Écrire un test qui met à jour le titre d'une tâche.

    Étapes :
    1. Créer une tâche avec le titre "Titre Original"
    2. Obtenir son ID
    3. Envoyer une requête PUT : client.put(f"/tasks/{task_id}", json={"title": "Nouveau Titre"})
    4. Vérifier que le code de statut est 200
    5. Vérifier que la réponse contient le nouveau titre

    Astuce : Les requêtes PUT sont comme les POST, mais elles modifient des données existantes
    """
    # TODO : Écrivez votre test ici !
    create_task = client.post("/tasks", json={"title":"Titre Original"})
    task_id = create_task.json()["id"]

    request = client.put(f"/tasks/{task_id}", json={"title":"Titre Modified"})
    assert request.status_code == 200

    task = request.json()
    assert task["title"] == "Titre Modified"



def test_update_task_status(client):
    create_response = client.post("/tasks", json={
        "title": "Titre Original",
        "status": "todo",
    })
    task_id = create_response.json()["id"]

    update_response = client.put(f"/tasks/{task_id}", json={
        "status": "done"
    })
    assert update_response.status_code == 200

    updated_task = update_response.json()
    assert updated_task["status"] == "done"
    assert updated_task["title"] == "Titre Original"


def test_update_nonexistent_task(client):
    update_response = client.put("/tasks/9999", json={"status": "done"})
    assert update_response.status_code == 404


# EXERCICE 3 : Tester la validation - un titre vide devrait échouer
def test_create_task_empty_title(client):
    """
    VOTRE TÂCHE : Tester que créer une tâche avec un titre vide échoue.

    Étapes :
    1. Essayer de créer une tâche avec title = ""
    2. Vérifier que le code de statut est 422 (Erreur de Validation)

    Astuce : Regardez test_create_task, mais attendez-vous à un échec !
    """
    # TODO : Écrivez votre test ici !
    create_task = client.post("/tasks", json={"title":""})
    assert create_task.status_code == 422


def test_delete_nonexistent_task_returns_404(client):
    """Deleting a task that doesn't exist should return 404."""
    # TODO: Votre code ici
    # 1. Essayer de supprimer une tâche avec un ID qui n'existe pas (ex: 9999)
    # 2. Vérifier que ça retourne 404
    # 3. Vérifier le message d'erreur contient "not found"

    create_task = client.delete("/tasks/9999")
    assert create_task.status_code == 404

    body = create_task.json()
    assert "detail" in body
    assert body["detail"] == "Task 9999 not found"


# EXERCICE 4 : Tester la validation - priorité invalide
def test_update_task_with_invalid_priority(client):
    """
    VOTRE TÂCHE : Tester qu'on ne peut pas mettre à jour une tâche avec une priorité invalide.

    Étapes :
    1. Créer une tâche valide
    2. Essayer de la mettre à jour avec priority="urgent" (invalide)
    3. Vérifier que le code de statut est 422 (Erreur de Validation)

    Rappel : Les priorités valides sont "low", "medium", "high" (voir TaskPriority dans app.py)
    """
    # TODO : Écrivez votre test ici !
    create_task = client.post("/tasks", json={"title":"title", "priority":"medium"})
    id = create_task.json()["id"]

    upadte_task = client.put(f"/tasks/{id}", json={"priority":"urgent"})
    assert upadte_task.status_code == 422



# EXERCICE 5 : Tester l'erreur 404
def test_get_nonexistent_task(client):
    """
    VOTRE TÂCHE : Tester qu'obtenir une tâche qui n'existe pas retourne 404.

    Étapes :
    1. Essayer d'obtenir une tâche avec un faux ID : client.get("/tasks/999")
    2. Vérifier que le code de statut est 404 (Not Found)
    """
    # TODO : Écrivez votre test ici !
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_filter_by_multiple_criteria(client):

    task1 = client.post("/tasks", json={
        "title": "Tâche 1",
        "status": "todo",
        "priority": "high"
    })
    task2 = client.post("/tasks", json={
        "title": "Tâche 2",
        "status": "in_progress",
        "priority": "medium"
    })
    task3 = client.post("/tasks", json={
        "title": "Tâche 3",
        "status": "todo",
        "priority": "low"
    })

    assert task1.status_code == 201
    assert task2.status_code == 201
    assert task3.status_code == 201

    response = client.get("/tasks", params={"status": "todo", "priority": "high"})
    assert response.status_code == 200

    tasks = response.json()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Tâche 1"
    assert tasks[0]["status"] == "todo"
    assert tasks[0]["priority"] == "high"



# =============================================================================
# EXERCICES BONUS (Si vous finissez en avance !)
# =============================================================================

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "BROKEN"  # ❌Bug volontaire

# =============================================================================
# ASTUCES & CONSEILS
# =============================================================================

"""
PATTERNS COURANTS :

1. Tester POST (Créer) :
   response = client.post("/tasks", json={"title": "..."})
   assert response.status_code == 201

2. Tester GET (Lire) :
   response = client.get("/tasks")
   assert response.status_code == 200

3. Tester PUT (Mettre à jour) :
   response = client.put(f"/tasks/{id}", json={"title": "..."})
   assert response.status_code == 200

4. Tester DELETE (Supprimer) :
   response = client.delete(f"/tasks/{id}")
   assert response.status_code == 204

5. Tester les erreurs de validation :
   response = client.post("/tasks", json={"bad": "data"})
   assert response.status_code == 422

6. Tester les erreurs 404 :
   response = client.get("/tasks/999")
   assert response.status_code == 404

CODES DE STATUT COURANTS :
- 200 : OK (GET/PUT réussi)
- 201 : Créé (POST réussi)
- 204 : Pas de Contenu (DELETE réussi)
- 404 : Non Trouvé (la ressource n'existe pas)
- 422 : Erreur de Validation (données invalides)

RAPPELEZ-VOUS :
- La fixture `client` est automatiquement fournie par conftest.py
- La base de données est automatiquement nettoyée avant/après chaque test
- Les tests doivent être indépendants (ne pas dépendre d'autres tests)
"""


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
