from django.apps import apps
from django.db import models
from django.db.models import QuerySet, UniqueConstraint
from django.db.models.functions import Lower
from django.forms.models import ModelChoiceIterator
from validators import ValidationError
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


class CategoryQuerySet(QuerySet):
    def root_nodes(self):
        # categories with no parent
        return self.filter(parents__isnull=True)

    def with_word(self, word):
        # categories with word (string or instance)
        if isinstance(word, str):
            try:
                word = Word.objects.get(text__iexact=word)
            except Word.DoesNotExist:
                return self.none()
        elif not isinstance(word, Word):
            return self.none()
        return self.filter(words=word).distinct()

    def descendant_words(self, category):
        # all words in category or any descendant category
        all_cats = [category] + list(category.descendants)
        return Word.objects.filter(category__in=all_cats).distinct()
    
    def exclude_category_and_descendants(self, category):
        # all categories except category or any descendant category
        return self.exclude(id__in={category.id, *[c.id for c in category.descendants]})
    
class CategoryManager(models.Manager):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db)

    def root_nodes(self):
        return self.get_queryset().root_nodes()

    def with_word(self, word):
        return self.get_queryset().with_word(word)

    def descendant_words(self, category):
        return self.get_queryset().descendant_words(category)
    
    def exclude_category_and_descendants(self, category):
        return self.get_queryset().exclude_category_and_descendants(category)

    def dag_edges(self, start_node=None):
        if start_node:
            categories = {start_node, *start_node.descendants}
        else:
            categories = self.all()

        edges = []
        for cat in categories:
            for parent in cat.parents.all():
                if not start_node or parent in categories:
                    edges.append({"data": {"source": str(parent.pk), "target": str(cat.pk)}})
            for word in cat.words.all():
                edges.append({"data": {"source": str(cat.pk), "target": f"word-{word.pk}"}})
        
        return edges

    def dag_nodes(self, start_node=None):
        if start_node:
            categories = {start_node, *start_node.descendants}
        else:
            categories = self.all()

        nodes = [{"data": {"id": str(cat.pk), "label": cat.name}} for cat in categories]
        
        for cat in categories:
            for word in cat.words.all():
                nodes.append({"data": {"id": f"word-{word.pk}", "label": word.text}})
        
        return nodes
    
    def dag_cytograph_data(self, start_node=None):
        # https://js.cytoscape.org/
        return self.dag_nodes(start_node) + self.dag_edges(start_node)
    
class CategoryParentFieldPanel(FieldPanel):
    """
    A custom FieldPanel that restricts the queryset of a category field to exclude
    the current instance and its descendants. This is useful for preventing cyclic
    relationships in hierarchical category structures.
    """
    class BoundPanel(FieldPanel.BoundPanel):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            if self.instance.pk:
                qs = apps.get_model('core', 'Category').objects.exclude_category_and_descendants(self.instance)
                self.form.fields[self.field_name].queryset = qs
                self.form.fields[self.field_name].widget.choices = ModelChoiceIterator(self.form.fields[self.field_name])
            pass


@register_snippet    
class Category(models.Model):
    objects = CategoryManager()

    name = models.CharField(max_length=255, unique=True)
    parents = models.ManyToManyField('self', symmetrical=False, related_name='children', blank=True, verbose_name="Parent Categories")
    words = models.ManyToManyField("Word", related_name="categories", blank=True)

    panels = [
        "name",
        CategoryParentFieldPanel("parents"),
        "words"
    ]

    def __str__(self):
        return self.name

    @property
    def ancestors(self):
        ancestors = set()
        def recurse(category):
            for parent in category.parents.all():
                if parent not in ancestors:
                    ancestors.add(parent)
                    recurse(parent)
        recurse(self)
        return ancestors

    @property
    def descendants(self):
        descendants = set()
        def recurse(category):
            for child in category.children.all():
                if child not in descendants:
                    descendants.add(child)
                    recurse(child)
        recurse(self)
        return descendants
    
    @property
    def all_words(self):
        return Category.objects.descendant_words(self)
    
    def clean(self):
        if self.pk and self in self.descendants:
            # circular relationship
            raise ValidationError("A category cannot be a descendant of itself.")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

class WordManager(models.Manager):
    def get_or_create_ci(self, text):
        # get or create case insensitive
        return self.get_or_create(text__iexact=text, defaults={'text': text})
    
@register_snippet        
class Word(models.Model):
    objects = WordManager()

    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text
    
    class Meta:
        ordering = ["text"]
        constraints = [ # unique, regardles of case
            UniqueConstraint(Lower('text'), name='word_text_ci_unique')
        ]        