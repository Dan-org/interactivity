from django import forms
from django.contrib import admin

from models import ActionLog, SupplementLog, Interactivity, InteractivityExercise, InteractivityWork, SessionAlias, InteractivitySession

### Custom Admins ###
class SessionAdmin(admin.ModelAdmin):
    pass

class InteractivitySessionAdmin(admin.ModelAdmin):
    #fields = ('session_id', 'user', 'activity_type', 'exercise_path', 'activity_url', 'created')
    #list_display = ('__unicode__', 'some_other_field')
    readonly_fields = ['created']
    pass
    

admin.site.register(Interactivity)
admin.site.register(InteractivityExercise)
admin.site.register(InteractivityWork)
admin.site.register(ActionLog)
admin.site.register(SupplementLog)

admin.site.register(SessionAlias, SessionAdmin)
admin.site.register(InteractivitySession, InteractivitySessionAdmin)