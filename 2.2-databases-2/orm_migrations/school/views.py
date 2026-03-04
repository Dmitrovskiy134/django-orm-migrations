from django.shortcuts import render
from .models import Student


def students_list(request):
    template = 'school/students_list.html'

    # Получаем всех учеников с сортировкой по классу
    # prefetch_related оптимизирует запросы к базе данных
    students = Student.objects.all().order_by('group').prefetch_related('teachers')

    context = {
        'object_list': students,
    }

    return render(request, template, context)