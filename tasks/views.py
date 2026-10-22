from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import TaskForm
from .models import Task


def task_list(request):
    show = request.GET.get('show', 'all')     # reads ?show=... from the URL

    tasks = Task.objects.all()
    if show == 'active':
        tasks = tasks.filter(completed=False)
    elif show == 'done':
        tasks = tasks.filter(completed=True)

    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'show': show})


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {'heading': 'Add a task'}

    def form_valid(self, form):                       # runs when the form is valid
        messages.success(self.request, 'Task added!')
        return super().form_valid(form)               # let Django save + redirect


class TaskUpdateView(UpdateView):
    model = Task                                      # finds the task by <int:pk> (404 if missing)
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:list')
    extra_context = {'heading': 'Edit task'}

    def form_valid(self, form):
        messages.success(self.request, 'Task updated!')
        return super().form_valid(form)


@require_POST
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk)     # find the task by its id
    task.completed = not task.completed       # True → False, False → True
    task.save()                               # write the change to the database
    if task.completed:
        messages.success(request, f'"{task.title}" marked as done ✓')
    else:
        messages.info(request, f'"{task.title}" marked as not done')
    return redirect('tasks:list')             # go back to the list


class TaskDeleteView(DeleteView):
    model = Task                              # GET → tasks/task_confirm_delete.html, POST → delete
    success_url = reverse_lazy('tasks:list')

    def form_valid(self, form):
        messages.success(self.request, f'"{self.object.title}" deleted.')
        return super().form_valid(form)
