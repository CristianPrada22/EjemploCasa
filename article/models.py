from distutils.text_file import TextFile
from email.mime import image
from django.db import models
from mptt.models import MPTTModel
from django.shortcuts import reverse
from django.utils.translation import ugettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields
from ckeditor.fields import RichTextField
# Create your models here.

class Category(MPTTModel):
    name = models.CharField(
        verbose_name = _('Name'), 
        max_length=150, 
        help_text=_("Name of category or subcategory")
    )
    parent = models.ForeignKey(
        'self',
        verbose_name=_('Parent'),
        on_delete=models.CASCADE,
        related_name='children',
        null=True,
        blank=True
    )
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = [ 'tree_id', 'lft' ]
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

class Article(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(
            verbose_name=_('Name'), 
            max_length=200, 
            help_text=_('Name of the articles')
        ),
        title = models.CharField(
            verbose_name=_('Title'),
            max_length=200, 
            help_text=_('Title of the  news or articles')
        ),
        abstract = models.TextField(
            verbose_name=_('Abstract'), 
            max_length=500, 
            help_text=_('Here you must write the abstract of the articles')
        ),
        content = RichTextField(
            verbose_name=_('Content'), 
            help_text=_('Here you must write the description of the article or news.')
        ),
        notes = RichTextField(
            verbose_name=_('Notes'), 
            help_text=_('Here you must write the notes of the article or news.')
        ),
        links = RichTextField(
            verbose_name=_('Links'), 
            help_text=_('Here you must write the links of the article or news.')
        ),
        more_information = RichTextField(
            verbose_name=_('More information'), 
            help_text=_('Here you must write the More information of the article or news.')
        ),
        contacts = RichTextField(
            verbose_name=_('Contacts'), 
            help_text=_('Here you must write the contacts.')
        ),
        tags = RichTextField(
            verbose_name=_('Tags'), 
            help_text=_('Here you must write the tags.')
        )

    )
    id = models.AutoField(primary_key = True)
    category = models.ForeignKey(
        Category,
        verbose_name= _('Category'),
        on_delete= models.CASCADE,
        blank=True,
        null=True
    )
    image = models.ImageField(
        verbose_name = _('Image'), 
        upload_to='article')
    date_created = models.DateTimeField(
        verbose_name = _('Date created'), 
        auto_now_add=True)
    date_updated = models.DateTimeField(
        verbose_name = _('Date updated'), 
        auto_now=True)
    active = models.BooleanField(
        verbose_name = _('Active'), 
        default=False, 
        help_text=_("Field to know if the article is active or not active"))
    

    class Meta:
        ordering = ['pk']
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

    def __str__(self):
        """Return title of article."""
        return self.name
    
    def get_absolute_url(self):
        return reverse("article:article-detail", kwargs={'id': self.id})