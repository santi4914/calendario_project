"""Custom template filters for the `notas` app."""
from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Return dict value for key or None. Works with dict-like objects.

    Usage in template: `{{ mydict|get_item:somekey }}`
    """
    if dictionary is None:
        return None
    # Try dict.get first (works for real dicts and QueryDict-like objects)
    try:
        return dictionary.get(key)
    except Exception:
        # Fallback to __getitem__ for mappings that don't implement get
        try:
            return dictionary[key]
        except Exception:
            return None
