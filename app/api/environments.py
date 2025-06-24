# app/api/environments.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..schema.environment import EnvironmentCreate, EnvironmentOut
from ..models.environment import Environment
from ..models.organization import Organization
from ..models.user import User
from ..database.session import SessionLocal
from ..repositories import environment_repo, group_repo, function_repo
from ..api.users import get_current_user
from ..helper import permissions, audit, response
from ..helper.animalname import generate_codename

router = APIRouter(prefix="/environments", tags=["environments"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
    "",
    response_model=dict,
    summary="Lister les environnements",
    description="Liste les environnements filtrés par nom ou organisation (superadmins voient tout, les autres uniquement ce qu'ils ont le droit de lire).",
    responses={
        200: {
            "description": "Liste des environnements récupérée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Liste des environnements récupérée",
                        "data": [
                            {
                                "id": 1,
                                "name": "Production",
                                "description": "Environnement de production",
                                "organization_id": 1,
                                "organization": {
                                    "id": 1,
                                    "name": "ACME Corp",
                                    "description": "Organisation principale"
                                },
                                "elements": [],
                                "rules": [],
                                "users": [],
                                "groups_with_access": []
                            },
                            {
                                "id": 2,
                                "name": "Développement",
                                "description": "Environnement de développement",
                                "organization_id": 1,
                                "organization": {
                                    "id": 1,
                                    "name": "ACME Corp",
                                    "description": "Organisation principale"
                                },
                                "elements": [],
                                "rules": [],
                                "users": [],
                                "groups_with_access": []
                            }
                        ]
                    }
                }
            }
        },
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"}
    }
)
def list_environments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    organization_name: Optional[str] = None
):
    query = db.query(Environment).join(Organization)

    if name:
        query = query.filter(Environment.name.ilike(f"%{name}%"))
    if organization_name:
        query = query.filter(Organization.name.ilike(f"%{organization_name}%"))

    environments = query.offset(skip).limit(limit).all()

    # filtrage des droits
    if not current_user.is_superadmin:
        environments = [
            env for env in environments
            if permissions.has_permission(db, current_user, env.organization_id, "env:read")
        ]

    return response.success_response(environments, "Liste des environnements récupérée")

@router.get(
    "/{environment_id}",
    response_model=dict,
    summary="Détail d’un environnement",
    description="Renvoie les détails d’un environnement si l’utilisateur y a accès.",
    responses={
        200: {"description": "Environnement récupéré avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"}
    }
)
def get_environment(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")
    if not permissions.has_permission(db, current_user, environment.organization_id, "env:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")
    return response.success_response(environment, "Environnement récupéré")

@router.post(
    "",
    response_model=dict,
    summary="Créer un environnement",
    description="Crée un environnement rattaché à une organisation. Associe une policy d’admin au créateur si nécessaire.",
    responses={
        200: {"description": "Environnement créé avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        500: {"description": "La fonction 'admin' est manquante"}
    }
)
def create_environment(
    env: EnvironmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not permissions.has_permission(db, current_user, env.organization_id, "env:create"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour créer un environnement")

    environment = environment_repo.create_environment(
        db,
        name=env.name,
        organization_id=env.organization_id
    )

    # Création du groupe Admins pour cet environnement (optionnel si politique d'accès déjà prévue)
    admin_group = group_repo.create_group(
        db,
        name="Admins",
        description="Groupe admin par défaut",
        organization_id=env.organization_id
    )

    # Fonction 'admin'
    admin_function = function_repo.get_function_by_name(db, "admin")
    if not admin_function:
        raise HTTPException(status_code=500, detail="La fonction 'admin' est manquante")

    group_repo.add_function_to_group(db, admin_group, admin_function)

    # Vérification : est-ce que l'utilisateur est admin de l'environnement via un groupe/policy ?
    is_already_admin = permissions.has_permission(db, current_user, environment.id, "env:update")

    if not is_already_admin:
        # On crée une policy "creator" avec rule `admin` sur cet env
        from ..models.policy import Policy
        from ..models.rule import Rule
        from ..repositories import policy_repo

        policy_name = f"Policy {environment.name} - creator"
        policy = policy_repo.create_policy(
            db,
            name=policy_name,
            organization_id=env.organization_id,
            description=f"Policy automatique pour le créateur de l’environnement {environment.name}"
        )

        # Ajout de la rule sur cet environnement
        rule = Rule(policy=policy, environment_id=environment.id, function=admin_function)
        db.add(rule)

        # Ajout de l’utilisateur à la policy
        policy.users.append(current_user)

        db.commit()
        db.refresh(policy)

    audit.log_action(
        db,
        current_user.id,
        "Création environnement",
        f"Environnement '{environment.name}' créé (ID {environment.id})"
    )

    return response.success_response(environment, "Environnement créé avec succès")

@router.put(
    "/{environment_id}",
    response_model=dict,
    summary="Mettre à jour un environnement",
    description="Met à jour un environnement s’il existe et si l’utilisateur a les droits.",
    responses={
        200: {"description": "Environnement mis à jour avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"}
    }
)
def update_environment(
    environment_id: int,
    env: EnvironmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    if not permissions.has_permission(db, current_user, environment.organization_id, "env:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")

    environment.name = env.name
    db.commit()
    db.refresh(environment)

    audit.log_action(db, current_user.id, "Mise à jour environnement", f"Nom mis à jour en {env.name}")
    return response.success_response(environment, "Environnement mis à jour")

@router.delete(
    "/{environment_id}",
    response_model=dict,
    summary="Supprimer un environnement",
    description="Supprime un environnement si l’utilisateur a les droits requis.",
    responses={
        200: {"description": "Environnement supprimé avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"}
    }
)
def delete_environment(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    if not permissions.has_permission(db, current_user, environment.organization_id, "env:delete"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")

    environment_repo.delete_environment(db, environment)

    audit.log_action(db, current_user.id, "Suppression environnement", f"Suppression de l’environnement {environment.name}")
    return response.success_response(None, "Environnement supprimé")

@router.get(
    "/generate-name",
    response_model=dict,
    summary="Générer un nom aléatoire",
    description="Génère un nom unique à partir d'un animal ou d'un adjectif.",
    responses={
        200: {"description": "Nom généré avec succès"},
        401: {"description": "Non authentifié"}
    }
)
def generate_environment_codename(
    current_user: User = Depends(get_current_user),
    prefix_length: int = Query(0, ge=0, le=6),
    use_adjective: bool = Query(True),
    use_adverb: bool = Query(False),
    suffix_length: int = Query(0, ge=0, le=6),
    separator: str = Query("-", max_length=2),
    style: Optional[str] = Query(None)
):
    name = generate_codename(
        prefix_length=prefix_length,
        use_adjective=use_adjective,
        use_adverb=use_adverb,
        suffix_length=suffix_length,
        separator=separator,
        style=style
    )
    return response.success_response(name, "Nom généré avec succès")

@router.get(
    "/{environment_id}/users",
    response_model=dict,
    summary="Utilisateurs liés à un environnement",
    description="Renvoie tous les utilisateurs ayant accès à un environnement via une policy (via les rules).",
    responses={
        200: {"description": "Utilisateurs récupérés avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"}
    }
)
def get_environment_users(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    if not permissions.has_permission(db, current_user, environment.organization_id, "env:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")

    return response.success_response(environment.users, "Utilisateurs récupérés")
