def has_permission(db, user, target_env: int, permission: str) -> bool:
    """
    Vérifie si l'utilisateur possède la permission demandée dans l'environnement cible.

    Un utilisateur a la permission si :
      - Il est superadmin,
      - OU s'il possède une affectation (UserAssignment) dont le groupe s'applique à l'environnement cible
        (soit le groupe est global, soit group.environment_id == target_env)
        ET que ce groupe possède une fonction dont le nom est "admin" (pour accès total)
        ou dont le nom correspond à la permission demandée.
    """
    if user.is_superadmin:
        return True

    for assignment in user.user_assignments:
        group = assignment.group
        if not group:
            continue
        # Le groupe est applicable s'il est global ou spécifique à l'environnement cible.
        if group.environment_id is None or group.environment_id == target_env:
            # Vérifier les fonctions du groupe
            for func in group.functions:
                if func.name == "admin" or func.name == permission:
                    return True
    return False
