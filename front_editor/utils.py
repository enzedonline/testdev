def is_in_group(user, group_name):
    if user.id==None:
        return False
    else:
        return user.groups.get_queryset().filter(name=group_name).exists() 

def user_has_perms(user, model, permissions):
    """
    Check if a user has all the specified permissions for a given model.
    
    Args:
        user (User): The user to check permissions for.
        model (models.Model): The model to check permissions against.
        permissions (list): A list of permission codenames (e.g., ['add', 'change']).
    
    Returns:
        bool: True if the user has all specified permissions, False otherwise.
    """
    app_label = model._meta.app_label
    model_name = model._meta.model_name
    permission_labels = []

    for perm in permissions:
        permission_labels += [f'{app_label}.{perm}_{model_name}']

    return user.has_perms(permission_labels)
