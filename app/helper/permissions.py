def has_permission(db, user, target_env: int= None, permission: str = None, target_element:int =None) -> bool:
    """
    Vérifie si l'utilisateur possède la permission demandée dans l'environnement cible ou sur l'élément cible.

    Un utilisateur a la permission si :
      - Il est superadmin,
      - OU s'il appartient à une organisation et:
        - Il appartient à un groupe qui s'applique à cette organisation et à ce user: on retient les policy associées
        - Il a des policy qui s'appliquent à ce user: on retient ces policy

        Pour chaque policy retenue, on vérifie les règles associées:
        - Si la fonction est "admin", l'utilisateur a tous les droits
        - Sinon, on vérifie que la fonction correspond à la permission demandée et que l'environnement
          ou l'élément sur lequel s'applique la règle correspond à celui passé en paramètre

    Les règles peuvent s'appliquer soit:
    - à un environnement (si environment_id n'est pas None dans la rule)
    - à un élément (si element_id n'est pas None dans la rule)
    - à tous les environnements et tous les éléments si les deux sont None

    Par ailleurs:
    - si target_env est None on regardera les règles par rapport à target_element
    - si target_element est None on regardera les règles par rapport à target_env
    - si target_env et target_element sont None, on retournera faux sauf si les deux éléments des règles sont à None
    """
    # Si l'utilisateur est superadmin, il a tous les droits
    if user.is_superadmin:
        return True

    # Récupérer toutes les policies applicables à l'utilisateur
    applicable_policies = set()

    # Pour chaque organisation de l'utilisateur
    for organization in user.organizations:
        # Policies des groupes de l'utilisateur dans cette organisation
        for group in user.groups:
            if group.organization_id == organization.id:
                for policy in group.policies:
                    if policy.organization_id == organization.id:
                        applicable_policies.add(policy)

        # Policies directement associées à l'utilisateur
        for policy in user.policies:
            if policy.organization_id == organization.id:
                applicable_policies.add(policy)

    # Vérifier les règles de chaque policy applicable
    for policy in applicable_policies:
        for rule in policy.rules:
            # Vérifier que la fonction correspond à la permission demandée
            if rule.function.name == permission or rule.function.name == "admin":
                # Cas où les deux sont None: la règle s'applique à tous les environnements et éléments
                if rule.environment_id is None and rule.element_id is None:
                    return True

                # Cas où target_env et target_element sont tous les deux None
                if target_env is None and target_element is None:
                    # On retourne False sauf si les deux éléments des règles sont à None
                    return rule.environment_id is None and rule.element_id is None

                # Cas où target_element est None: on vérifie par rapport à target_env
                if target_element is None:
                    if rule.environment_id == target_env:
                        return True

                # Cas où target_env est None: on vérifie par rapport à target_element
                elif target_env is None:
                    if rule.element_id == target_element.id:
                        return True
                    if rule.environment_id == target_element.environment_id:
                        return True

                # Cas où les deux sont spécifiés
                else:
                    # Si la règle s'applique directement à l'élément
                    if rule.element_id == target_element.id:
                        return True
                    # Si la règle s'applique à l'environnement de l'élément ou à l'environnement cible
                    if rule.environment_id == target_element.environment_id or rule.environment_id == target_env:
                        return True

    return False
