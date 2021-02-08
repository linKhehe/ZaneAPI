from .tokens import Token


class Project:

    def __init__(self, redis, project_id):
        self._redis = redis
        self.id = project_id

        self._name = None
        self._description = None
        self._owner_id = None

    @property
    def name(self):
        if self._name is None:
            self._name = self._redis.hget(self.id, "name").decode()
        return self._name

    @property
    def description(self):
        if self._description is None:
            self._description = self._redis.hget(self.id, "description").decode()
        return self._description

    @property
    def owner_id(self):
        if self._owner_id is None:
            self._owner_id = self._redis.hget(self.id, "owner_id").decode()
        return self._owner_id

    @property
    def token(self):
        return Token(self._redis, self.id)

    @classmethod
    def create(cls, redis, project_id=id, name=name, description=description, owner_id=owner_id):
        redis.hset(project_id, "name", name, dict(description=description, owner_id=owner_id))
        redis.rpush(f"{owner_id}:projects", project_id)

        return cls(redis, project_id)

    def delete(self):
        self._redis.lrem(f"{self.owner_id}:projects", 0, self.id)
        self._redis.delete(self.id)

        self._name = None
        self._description = None
        self._owner_id = None

    def edit(self, name=name, description=description):
        self._name = name or self._name
        self._description = description or self._description

        self._redis.hset(self.id, "owner_id", self.owner_id, dict(name=name, description=description))
