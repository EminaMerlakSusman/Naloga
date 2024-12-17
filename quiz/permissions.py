from rest_framework import permissions

from quiz.models import Question
from quiz.enums import UserGroups

class IsQuestionOwnerOrAdmin(permissions.BasePermission):
    """
    Only allow admins or owners of Questions to edit the Questions
    """
    def has_object_permission(self, request, view, obj):
        # Everyone has read perms
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.groups.filter(name=UserGroups.ADMIN_USER.value).exists():
            return True

        return obj.owner.pk == request.user.pk
    
    
class IsChoiceOwnerOrAdmin(permissions.BasePermission):
    """
    Only allow admins or owners of parent questions to edit choices
    """
    def has_permission(self, request, view):
        """ Permission checks for list and create """
        if request.user.groups.filter(name=UserGroups.ADMIN_USER.value).exists():
            return True
 
        if request.method == 'POST':
            question_id = request.data.get('question')
            if question_id:
                try:
                    question = Question.objects.get(id=question_id)
                    return question.owner == request.user # User can edit only choices for their own questions
                except Question.DoesNotExist:
                    return False
                
        return True
    
    def has_object_permission(self, request, view, obj):
        """ Permission checks for RUD actions """
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.groups.filter(name=UserGroups.ADMIN_USER.value).exists():
            return True
        
        return obj.question.owner.pk == request.user.pk