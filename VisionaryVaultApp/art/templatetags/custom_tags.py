from django import template

register = template.Library()


@register.filter
def has_permission(user, perm):
    return user.has_perm(perm)


@register.simple_tag
def is_user_banned_or_inactive(user):
    """
    Returns True if the user is banned (in 'Banned Users' group) or inactive.
    """
    if user.is_authenticated:
        return user.groups.filter(name='Banned users').exists()
    return False
