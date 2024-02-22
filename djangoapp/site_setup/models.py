from django.db import models
from utils.model_validators import validate_png
from utils.images import resize_image

# Create your models here.


class MenuLink(models.Model):
    class Meta:
        verbose_name = 'Menu Link'
        verbose_name_plural = 'Menu Links'

    text = models.CharField(max_length=50)
    # charfield usado para o usuário poder utilizar paths: /caminho/exemplo
    url_or_path = models.CharField(max_length=2048)
    new_tab = models.BooleanField(default=False)
    site_setup = models.ForeignKey(
        'SiteSetup', on_delete=models.CASCADE, blank=True, null=True,
        related_name='menu'
    )

    def __str__(self):
        return self.text


class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setups'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    favicon = models.ImageField(
        upload_to='assets/favicon/%Y/%m/',
        blank=True, default='',
        validators=[validate_png],
    )

    def save(self, *args, **kwargs):
        # pegando o nome do favicon antes de salvar:
        current_favicon_name = str(self.favicon.name)
        # devo chamar super para eu n reescrever o método, apenas acrescentar
        # uma funcionalidade
        super().save(*args, **kwargs)
        favicon_changed = False

        # lógica para eu redimensionar a imagem
        # somente se o favicon foi alterado
        # pega o nome depois de salvar e compara
        if self.favicon:
            favicon_changed = current_favicon_name != self.favicon.name

        if favicon_changed:
            resize_image(self.favicon, 32)

    def __str__(self):
        return self.title
