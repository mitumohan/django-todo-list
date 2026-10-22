from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskViewTests(TestCase):

    def test_create_task(self):
        response = self.client.post(reverse('tasks:create'), {'title': 'Buy milk', 'priority': 2})
        self.assertRedirects(response, reverse('tasks:list'))
        self.assertEqual(Task.objects.get().title, 'Buy milk')

    def test_empty_title_is_rejected(self):
        self.client.post(reverse('tasks:create'), {'title': '', 'priority': 2})
        self.assertEqual(Task.objects.count(), 0)

    def test_toggle_marks_done(self):
        task = Task.objects.create(title='Read')
        self.client.post(reverse('tasks:toggle', args=[task.pk]))
        task.refresh_from_db()
        self.assertTrue(task.completed)

    def test_toggle_rejects_get(self):
        task = Task.objects.create(title='Read')
        response = self.client.get(reverse('tasks:toggle', args=[task.pk]))
        self.assertEqual(response.status_code, 405)   # Method Not Allowed

    def test_filter_active_hides_done_tasks(self):
        Task.objects.create(title='Open task')
        Task.objects.create(title='Finished task', completed=True)
        response = self.client.get(reverse('tasks:list') + '?show=active')
        self.assertContains(response, 'Open task')
        self.assertNotContains(response, 'Finished task')

    def test_delete(self):
        task = Task.objects.create(title='Bye')
        self.client.post(reverse('tasks:delete', args=[task.pk]))
        self.assertFalse(Task.objects.exists())

    def test_edit_changes_title(self):
        task = Task.objects.create(title='Old')
        self.client.post(reverse('tasks:edit', args=[task.pk]), {'title': 'New', 'priority': 2})
        task.refresh_from_db()
        self.assertEqual(task.title, 'New')

    def test_edit_missing_task_is_404(self):
        response = self.client.get(reverse('tasks:edit', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_get_delete_does_not_delete(self):
        task = Task.objects.create(title='Stay')
        response = self.client.get(reverse('tasks:delete', args=[task.pk]))
        self.assertContains(response, 'Are you sure')
        self.assertEqual(Task.objects.count(), 1)

    def test_success_message_after_create(self):
        response = self.client.post(
            reverse('tasks:create'), {'title': 'Buy milk', 'priority': 2}, follow=True
        )
        self.assertContains(response, 'Task added!')


class TaskModelTests(TestCase):

    def test_past_due_date_is_overdue(self):
        task = Task(title='x', due_date=date.today() - timedelta(days=1))
        self.assertTrue(task.is_overdue)

    def test_future_due_date_is_not_overdue(self):
        task = Task(title='x', due_date=date.today() + timedelta(days=1))
        self.assertFalse(task.is_overdue)

    def test_no_due_date_is_not_overdue(self):
        task = Task(title='x')
        self.assertFalse(task.is_overdue)

    def test_completed_task_is_not_overdue(self):
        task = Task(title='x', due_date=date.today() - timedelta(days=1), completed=True)
        self.assertFalse(task.is_overdue)
