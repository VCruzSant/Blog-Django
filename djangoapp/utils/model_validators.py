from django.core.exceptions import ValidationError


def validate_png(img):
    # se ele não termina com png faça:
    if not img.name.lower().endswith('.png'):
        raise ValidationError('Image must be .png')
