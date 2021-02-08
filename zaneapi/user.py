from .project import Project


class User:

    def __init__(self, redis, **data):
        self._redis = redis

        self.id = data.get("id")
        self._username = data.get("username")
        self._discriminator = data.get("discriminator")
        self._avatar = data.get("avatar")
        self._verified_email = data.get("verified")
        self._email = data.get("email")
        self._flags = data.get("flags")
        self._premium_type = data.get("premium_type")
        self._public_flags = data.get("public_flags")

    @property
    def username(self):
        return self._username or self._redis.hget(self.id, "username").decode()

    @property
    def discriminator(self):
        return self._discriminator or self._redis.hget(self.id, "discriminator").decode()

    @property
    def avatar(self):
        return self._avatar or self._redis.hget(self.id, "avatar").decode()

    @property
    def verified_email(self):
        return self._verified_email or bool(self._redis.hget(self.id, "verified_email"))

    @property
    def email(self):
        return self._email or self._redis.hget(self.id, "email").decode()

    @property
    def flags(self):
        return self._flags or self._redis.hget(self.id, "flags").decode()

    @property
    def premium_type(self):
        return self._discriminator or self._redis.hget(self.id, "premium_type").decode()

    @property
    def public_flags(self):
        return self._public_flags or self._redis.hget(self.id, "public_flags").decode()

    @property
    def avatar_url(self):
        return f"https://cdn.discordapp.com/avatars/{self.id}/{self.avatar}.png"

    @property
    def is_banned(self):
        return bool(int(self._redis.hget(self.id, "is_banned")))

    @property
    def is_admin(self):
        return bool(int(self._redis.hget(self.id, "is_admin")))

    def get_projects(self):
        project_ids = self._redis.lrange(f"{self.id}:projects", 0, 9)
        return [Project(self._redis, project_id.decode()) for project_id in project_ids]

    def is_registered(self):
        if self.id is None:
            return False
        return self._redis.exists(self.id)

    def save(self, **data):
        for k, v in data.items():
            if type(v) is bool:
                data[k] = int(v)

        self._redis.hset(self.id, "id", self.id, data)

    def register(self, **data):
        self.save(**data)
        self._redis.incr("user_count")

        return self

    def has_project_permissions(self, project):
        return project.owner_id == self.id or self.is_admin
