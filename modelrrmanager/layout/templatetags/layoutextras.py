from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    print(dictionary)
    print(key)
    return dictionary.get(key)
