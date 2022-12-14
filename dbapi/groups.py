from core_app.models import LateremGroupMembership, LateremGroup, LateremUser, LateremWork
from extratypes import DBHybrid
from .tasks import Work

class Member(DBHybrid):
    __dbmodel__ = LateremUser

    def __init__(self, dbobj, group):
        super().__init__(dbobj)
        self.group = group
        self.dbmembership = LateremGroupMembership.objects.get(user=dbobj,
                                                               group=group.dbmodel)               
    
    def get_permission(self, permission):
        if self.dbmembership.is_group_admin:
            return True
        elif permission.startswith('can'):
            return self.dbmembership.__getattribute__(permission)
        else:
            return False

class Group(DBHybrid):
    __dbmodel__ = LateremGroup

    def get_members(self):
        return [Member(x, self) for x in LateremUser.objects.filter(lateremgroupmembership__group=self.dbmodel)]
    
    def get_works(self):
        return [Work(x) for x in LateremWork.objects.filter(lateremassignment__group=self.dbmodel)]
    
    def add_member(self, user, **permissions):
        membership = LateremGroupMembership.objects.create(user=user.dbmodel,
                                                           group=self.dbmodel,
                                                           **permissions)
        membership.save()
        member = Member(user.dbmodel, self)
        return member
    
    def remove_member(self, user):
        membership = LateremGroupMembership.objects.get(user=user.dbmodel,
                                                        group=self.dbmodel
                                                        )
        membership.delete()

    def set_global_permission(self, **permissions):
        for key, value in permissions.items():
            self.dbmodel.__setattr__(key, value)

    

    