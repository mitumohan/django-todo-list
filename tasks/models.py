from datetime import date

from django.db import models


class Task(models.Model):
    """One thing to do, e.g. "Buy milk"."""

    class Priority(models.IntegerChoices):
        # stored value, label shown to the user
        HIGH = 1, 'High'
        MEDIUM = 2, 'Medium'
        LOW = 3, 'Low'

    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM)
    due_date = models.DateField(null=True, blank=True)   # optional
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # unfinished first, then High → Low (1, 2, 3 sorts correctly), then newest
        ordering = ['completed', 'priority', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return (
            self.due_date is not None
            and not self.completed
            and self.due_date < date.today()
        )
