def user_roles(request):
    if not request.user.is_authenticated:
        return {'user_roles': []}

    groups = list(request.user.groups.values_list('name', flat=True))
    if request.user.is_superuser and 'Admin' not in groups:
        groups.insert(0, 'Admin')
    return {'user_roles': groups}
