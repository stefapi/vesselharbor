# app/api/environments.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..models import Element
from ..models.network import Network
from ..models.vm import VM
from ..models.storage_pool import StoragePool
from ..models.volume import Volume
from ..models.domain import Domain
from ..models.container_node import ContainerNode
from ..models.container_cluster import ContainerCluster
from ..models.stack import Stack
from ..models.application import Application
from ..schema.environment import EnvironmentCreate, EnvironmentOut
from ..schema.physical_host import PhysicalHostOut
from ..schema.element import ElementOut
from ..schema.network import NetworkOut
from ..schema.vm import VMOut
from ..schema.storage_pool import StoragePoolOut
from ..schema.volume import VolumeOut
from ..schema.domain import DomainOut
from ..schema.container_node import ContainerNodeOut
from ..schema.container_cluster import ContainerClusterOut
from ..schema.stack import StackOut
from ..schema.application import ApplicationOut
from ..models.environment import Environment
from ..models.organization import Organization
from ..models.user import User
from ..database.session import SessionLocal
from ..repositories import environment_repo, group_repo, function_repo, tag_repo, physical_host_repo
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

@router.get(
    "/{environment_id}/physical-hosts",
    response_model=dict,
    summary="Liste des hôtes physiques d'un environnement",
    description="Renvoie la liste des hôtes physiques associés à un environnement si l'utilisateur y a accès.",
    responses={
        200: {"description": "Liste des hôtes physiques récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"}
    }
)
def get_environment_physical_hosts(
    environment_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    environment = environment_repo.get_environment(db, environment_id)
    if not environment:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")
    if not permissions.has_permission(db, current_user, environment.organization_id, "env:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante")

    physical_hosts = physical_host_repo.list_physical_hosts_by_environment(db, environment_id, skip, limit)
    return response.success_response(
        [PhysicalHostOut.model_validate(host) for host in physical_hosts],
        "Liste des hôtes physiques récupérée"
    )

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

    # TODO ajouter un generate codename ici
    environment = environment_repo.create_environment(
        db,
        name=env.name,
        organization_id=env.organization_id,
        description=env.description
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
        # Get the user from the same session as the policy to avoid session conflicts
        user_in_session = db.query(User).get(current_user.id)
        policy.users.append(user_in_session)

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
    environment.description = env.description
    # We don't update organization_id as it would require additional permission checks and might break relationships

    db.commit()
    db.refresh(environment)

    audit.log_action(db, current_user.id, "Mise à jour environnement", f"Environnement '{environment.name}' mis à jour")
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


@router.get(
    "/{environment_id}/elements",
    response_model=dict,
    summary="Lister les éléments d'un environnement",
    description="Liste les éléments d'un environnement avec pagination et filtrage par nom et type.",
    responses={
        200: {"description": "Liste des éléments récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
        400: {"description": "Type d'élément invalide"},
    }
)
def list_elements(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    element_type: Optional[str] = Query(None, description="Type d'élément à filtrer (network, vm, storage_pool, volume, domain, container_node, container_cluster, stack, application)")
):
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les éléments")

    query = db.query(Element).filter(Element.environment_id == environment_id)

    # Filtrer par type d'élément si spécifié
    if element_type:
        if element_type == "network":
            query = query.join(Network, Element.id == Network.element_id)
        elif element_type == "vm":
            query = query.join(VM, Element.id == VM.element_id)
        elif element_type == "storage_pool":
            query = query.join(StoragePool, Element.id == StoragePool.element_id)
        elif element_type == "volume":
            query = query.join(Volume, Element.id == Volume.element_id)
        elif element_type == "domain":
            query = query.join(Domain, Element.id == Domain.element_id)
        elif element_type == "container_node":
            query = query.join(ContainerNode, Element.id == ContainerNode.element_id)
        elif element_type == "container_cluster":
            query = query.join(ContainerCluster, Element.id == ContainerCluster.element_id)
        elif element_type == "stack":
            query = query.join(Stack, Element.id == Stack.element_id)
        elif element_type == "application":
            query = query.join(Application, Element.id == Application.element_id)
        else:
            raise HTTPException(status_code=400, detail=f"Type d'élément invalide: {element_type}")

    # Filtrer par nom si spécifié
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Appliquer la pagination
    elements = query.offset(skip).limit(limit).all()

    # Convertir les éléments en ElementOut pour la sérialisation
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Liste des éléments récupérée")

@router.get(
    "/{environment_id}/tags",
    response_model=dict,
    summary="Lister les tags d'un environnement",
    description="Récupère tous les tags associés à un environnement.",
    responses={
        200: {"description": "Tags récupérés avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"}
    }
)
def list_environment_tags(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que l'environnement existe
    environment = db.query(Environment).filter(Environment.id == environment_id).first()
    if not environment:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions sur l'organisation de l'environnement
    org_id = environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "env:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour accéder à cet environnement")

    # Convertir les objets Tag en TagOut pour une sérialisation correcte
    from ..schema.tag import TagOut
    serializable_tags = [TagOut.model_validate(tag) for tag in environment.tags]

    return response.success_response(serializable_tags, "Tags de l'environnement récupérés avec succès")


@router.post(
    "/{environment_id}/tags/{tag_id}",
    response_model=dict,
    summary="Ajouter un tag à un environnement",
    description="Associe un tag existant à un environnement.",
    responses={
        200: {"description": "Tag ajouté à l'environnement avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement ou tag non trouvé"}
    }
)
def add_tag_to_environment(
    environment_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que l'environnement existe
    environment = db.query(Environment).filter(Environment.id == environment_id).first()
    if not environment:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions sur l'organisation de l'environnement
    org_id = environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "env:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour modifier cet environnement")

    # Vérifier que le tag existe
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")

    # Vérifier si le tag est déjà associé à l'environnement
    if tag in environment.tags:
        return response.success_response(environment, "Le tag est déjà associé à cet environnement")

    # Ajouter le tag à l'environnement
    environment.tags.append(tag)
    db.commit()

    audit.log_action(db, current_user.id, "Ajout tag à environnement", f"Tag '{tag.value}' ajouté à l'environnement '{environment.name}'")
    return response.success_response(environment, "Tag ajouté à l'environnement avec succès")

@router.delete(
    "/{environment_id}/tags/{tag_id}",
    response_model=dict,
    summary="Retirer un tag d'un environnement",
    description="Retire l'association entre un tag et un environnement.",
    responses={
        200: {"description": "Tag retiré de l'environnement avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement ou tag non trouvé"}
    }
)
def remove_tag_from_environment(
    environment_id: int,
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Vérifier que l'environnement existe
    environment = db.query(Environment).filter(Environment.id == environment_id).first()
    if not environment:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions sur l'organisation de l'environnement
    org_id = environment.organization_id
    if not permissions.has_permission(db, current_user, org_id, "env:update"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour modifier cet environnement")

    # Vérifier que le tag existe
    tag = tag_repo.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag non trouvé")

    # Vérifier si le tag est associé à l'environnement
    if tag not in environment.tags:
        return response.success_response(environment, "Le tag n'est pas associé à cet environnement")

    # Retirer le tag de l'environnement
    environment.tags.remove(tag)
    db.commit()

    audit.log_action(db, current_user.id, "Retrait tag d'environnement", f"Tag '{tag.value}' retiré de l'environnement '{environment.name}'")
    return response.success_response(environment, "Tag retiré de l'environnement avec succès")

@router.get(
    "/{environment_id}/networks",
    response_model=dict,
    summary="Lister les réseaux d'un environnement",
    description="Liste les éléments de type réseau dans un environnement avec pagination et filtrage par nom.",
    responses={
        200: {"description": "Liste des réseaux récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
    }
)
def list_networks(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Vérifier que l'environnement existe
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les réseaux")

    # Construire la requête pour récupérer les éléments de type réseau
    query = db.query(Element).join(Network, Element.id == Network.element_id).filter(Element.environment_id == environment_id)

    # Filtrer par nom si spécifié
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Appliquer la pagination
    elements = query.offset(skip).limit(limit).all()

    # Convertir les éléments en ElementOut pour la sérialisation
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Liste des réseaux récupérée")

@router.get(
    "/{environment_id}/vms",
    response_model=dict,
    summary="Lister les machines virtuelles d'un environnement",
    description="Liste les éléments de type machine virtuelle dans un environnement avec pagination et filtrage par nom.",
    responses={
        200: {"description": "Liste des machines virtuelles récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
    }
)
def list_vms(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Vérifier que l'environnement existe
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les machines virtuelles")

    # Construire la requête pour récupérer les éléments de type VM
    query = db.query(Element).join(VM, Element.id == VM.element_id).filter(Element.environment_id == environment_id)

    # Filtrer par nom si spécifié
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Appliquer la pagination
    elements = query.offset(skip).limit(limit).all()

    # Convertir les éléments en ElementOut pour la sérialisation
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Liste des machines virtuelles récupérée")

@router.get(
    "/{environment_id}/storage-pools",
    response_model=dict,
    summary="Lister les pools de stockage d'un environnement",
    description="Liste les éléments de type pool de stockage dans un environnement avec pagination et filtrage par nom.",
    responses={
        200: {"description": "Liste des pools de stockage récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
    }
)
def list_storage_pools(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Vérifier que l'environnement existe
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les pools de stockage")

    # Construire la requête pour récupérer les éléments de type StoragePool
    query = db.query(Element).join(StoragePool, Element.id == StoragePool.element_id).filter(Element.environment_id == environment_id)

    # Filtrer par nom si spécifié
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Appliquer la pagination
    elements = query.offset(skip).limit(limit).all()

    # Convertir les éléments en ElementOut pour la sérialisation
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Liste des pools de stockage récupérée")

@router.get(
    "/{environment_id}/volumes",
    response_model=dict,
    summary="Lister les volumes d'un environnement",
    description="Liste les éléments de type volume dans un environnement avec pagination et filtrage par nom.",
    responses={
        200: {"description": "Liste des volumes récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
    }
)
def list_volumes(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Vérifier que l'environnement existe
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les volumes")

    # Construire la requête pour récupérer les éléments de type Volume
    query = db.query(Element).join(Volume, Element.id == Volume.element_id).filter(Element.environment_id == environment_id)

    # Filtrer par nom si spécifié
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Appliquer la pagination
    elements = query.offset(skip).limit(limit).all()

    # Convertir les éléments en ElementOut pour la sérialisation
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Liste des volumes récupérée")

@router.get(
    "/{environment_id}/domains",
    response_model=dict,
    summary="Lister les domaines d'un environnement",
    description="Liste les éléments de type domaine dans un environnement avec pagination et filtrage par nom.",
    responses={
        200: {"description": "Liste des domaines récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
    }
)
def list_domains(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Vérifier que l'environnement existe
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les domaines")

    # Construire la requête pour récupérer les éléments de type Domain
    query = db.query(Element).join(Domain, Element.id == Domain.element_id).filter(Element.environment_id == environment_id)

    # Filtrer par nom si spécifié
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Appliquer la pagination
    elements = query.offset(skip).limit(limit).all()

    # Convertir les éléments en ElementOut pour la sérialisation
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Liste des domaines récupérée")

@router.get(
    "/{environment_id}/container-nodes",
    response_model=dict,
    summary="Lister les noeuds de conteneur d'un environnement",
    description="Liste les éléments de type noeud de conteneur dans un environnement avec pagination et filtrage par nom.",
    responses={
        200: {"description": "Liste des noeuds de conteneur récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
    }
)
def list_container_nodes(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Vérifier que l'environnement existe
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les noeuds de conteneur")

    # Construire la requête pour récupérer les éléments de type ContainerNode
    query = db.query(Element).join(ContainerNode, Element.id == ContainerNode.element_id).filter(Element.environment_id == environment_id)

    # Filtrer par nom si spécifié
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Appliquer la pagination
    elements = query.offset(skip).limit(limit).all()

    # Convertir les éléments en ElementOut pour la sérialisation
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Liste des noeuds de conteneur récupérée")

@router.get(
    "/{environment_id}/container-clusters",
    response_model=dict,
    summary="Lister les clusters de conteneur d'un environnement",
    description="Liste les éléments de type cluster de conteneur dans un environnement avec pagination et filtrage par nom.",
    responses={
        200: {"description": "Liste des clusters de conteneur récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
    }
)
def list_container_clusters(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Vérifier que l'environnement existe
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les clusters de conteneur")

    # Construire la requête pour récupérer les éléments de type ContainerCluster
    query = db.query(Element).join(ContainerCluster, Element.id == ContainerCluster.element_id).filter(Element.environment_id == environment_id)

    # Filtrer par nom si spécifié
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Appliquer la pagination
    elements = query.offset(skip).limit(limit).all()

    # Convertir les éléments en ElementOut pour la sérialisation
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Liste des clusters de conteneur récupérée")

@router.get(
    "/{environment_id}/stacks",
    response_model=dict,
    summary="Lister les stacks d'un environnement",
    description="Liste les éléments de type stack dans un environnement avec pagination et filtrage par nom.",
    responses={
        200: {"description": "Liste des stacks récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
    }
)
def list_stacks(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Vérifier que l'environnement existe
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les stacks")

    # Construire la requête pour récupérer les éléments de type Stack
    query = db.query(Element).join(Stack, Element.id == Stack.element_id).filter(Element.environment_id == environment_id)

    # Filtrer par nom si spécifié
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Appliquer la pagination
    elements = query.offset(skip).limit(limit).all()

    # Convertir les éléments en ElementOut pour la sérialisation
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Liste des stacks récupérée")

@router.get(
    "/{environment_id}/applications",
    response_model=dict,
    summary="Lister les applications d'un environnement",
    description="Liste les éléments de type application dans un environnement avec pagination et filtrage par nom.",
    responses={
        200: {"description": "Liste des applications récupérée avec succès"},
        401: {"description": "Non authentifié"},
        403: {"description": "Permission insuffisante"},
        404: {"description": "Environnement non trouvé"},
    }
)
def list_applications(
    environment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None
):
    # Vérifier que l'environnement existe
    env = db.query(Environment).filter_by(id=environment_id).first()
    if not env:
        raise HTTPException(status_code=404, detail="Environnement non trouvé")

    # Vérifier les permissions
    if not permissions.has_permission(db, current_user, env.organization_id, "element:read"):
        raise HTTPException(status_code=403, detail="Permission insuffisante pour lister les applications")

    # Construire la requête pour récupérer les éléments de type Application
    query = db.query(Element).join(Application, Element.id == Application.element_id).filter(Element.environment_id == environment_id)

    # Filtrer par nom si spécifié
    if name:
        query = query.filter(Element.name.ilike(f"%{name}%"))

    # Appliquer la pagination
    elements = query.offset(skip).limit(limit).all()

    # Convertir les éléments en ElementOut pour la sérialisation
    serializable_elements = [ElementOut.model_validate(element) for element in elements]

    return response.success_response(serializable_elements, "Liste des applications récupérée")
