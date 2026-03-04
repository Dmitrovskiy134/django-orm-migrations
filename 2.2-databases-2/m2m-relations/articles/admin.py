from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()

        # Считаем количество основных тегов
        main_count = 0
        for form in self.forms:
            # Пропускаем пустые формы (которые пользователь не заполнял)
            if not form.cleaned_data or form.cleaned_data.get('DELETE'):
                continue

            if form.cleaned_data.get('is_main'):
                main_count += 1

        # Проверяем, что есть ровно один основной тег
        if main_count == 0:
            raise ValidationError('Укажите основной раздел')
        elif main_count > 1:
            raise ValidationError('Основным может быть только один раздел')


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1  # сколько пустых форм показывать
    autocomplete_fields = ['tag']  # удобный поиск тегов


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    list_display = ['title', 'published_at', 'display_tags']
    list_filter = ['published_at']
    search_fields = ['title', 'text']

    def display_tags(self, obj):
        """Отображает теги статьи в списке"""
        tags = [scope.tag.name for scope in obj.scopes.all()]
        return ", ".join(tags)

    display_tags.short_description = 'Разделы'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']