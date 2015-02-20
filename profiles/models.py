import json

from django.db import models


class TypeObjectManager(models.Manager):
    """Allow for easier as well as safer retrieval of instances of type
    objects via the model's encoded code constants.

    The column name to query is specified on the concrete class via the class
    attribute 'code_field_name'.

    """
    code_field_name = None

    def __init__(self, code_field_name=None):
        super(TypeObjectManager, self).__init__()
        self.code_field_name = code_field_name or self.code_field_name

    def get_type_object_queryset(self, code):
        return self.filter(**{self.code_field_name: code})

    def __getattr__(self, key):
        if key != 'model':
            # (If requested attr is 'model', then manager must not have
            # 'model', and below `self.model` would go recursive.)
            try:
                code = getattr(self.model, key.upper())
            except AttributeError:
                pass
            else:
                if self.code_field_name is None:
                    raise NotImplementedError(
                        "%s.code_field_name must be defined"
                        % self.__class__.__name__
                    )
                return self.get_type_object_queryset(code).get()

        raise AttributeError("'%s' object has no attribute '%s'"
                             % (self.__class__.__name__, key))


class CodedObjectManager(TypeObjectManager):

    code_field_name = 'code'


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CodedTypeModel(BaseModel):
    name = models.CharField(max_length=45)
    code = models.CharField(max_length=45, unique=True)

    objects = CodedObjectManager()

    def __unicode__(self):
        return u'%s' % self.name

    class Meta(object):
        abstract = True


class Profile(BaseModel):
    screen_name = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    _user_json = models.TextField(blank=True)

    @property
    def user_json(self):
        return json.loads(self._user_json)
    @user_json.setter
    def user_json(self, value):
        self._user_json = json.dumps(value)
    

class Status(BaseModel):
    profile = models.ForeignKey(Profile)
    status_id = models.CharField(max_length=18)
    _status_json = models.TextField(blank=True)

    @property
    def status_json(self):
        return json.loads(self._status_json)
    @status_json.setter
    def status_json(self, value):
        self._status_json = json.dumps(value)
