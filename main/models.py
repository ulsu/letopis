from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import datetime


class Task(models.Model):
    IMPORTANCE_LEVELS = (
        (0, "Very low"),
        (1, "Low"),
        (2, "Middle"),
        (3, "High"),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    parent = models.ForeignKey('Task', null=True, blank=True, related_name='children')
    _performers = models.ManyToManyField(User)
    importance = models.IntegerField(choices=IMPORTANCE_LEVELS)

    def performers(self):
        return list(set(self.parent.performers() + self._performers.all())) if self.parent else self._performers.all()

    def category_chain(self):
        if self.parent:
            return '%s - %s' % (self.parent.title, self.title )
        else:
            return ''


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_chain', 'importance')
admin.site.register(Task, TaskAdmin)


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name='comments')
    parent = models.ForeignKey('Comment', null=True, related_name='children')
    user = models.ForeignKey(User, related_name='comments')
    datetime = models.DateTimeField(default=datetime.datetime.now())
    text = models.TextField()


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'datetime', 'text')
admin.site.register(Comment, CommentAdmin)