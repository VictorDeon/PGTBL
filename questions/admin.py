from django.contrib import admin
from .models import (
    Question, ExerciseSubmission, IRATSubmission, GRATSubmission
)

admin.site.register(Question)
admin.site.register(ExerciseSubmission)
admin.site.register(IRATSubmission)
admin.site.register(GRATSubmission)
