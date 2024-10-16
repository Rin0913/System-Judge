from models import User, WGConf


class UserRepository:

    def __init__(self, logger=None):
        self.logger = logger

    def init_app(self, app, logger):
        app.user_repository = self
        self.logger = logger

    def create(self, uid):
        user = User(name=uid)
        user.save()
        return user.id

    def __query(self, uid):
        return User.objects(name=uid).first()

    def query(self, uid):
        user = self.__query(uid)
        if user:
            return user.to_mongo().to_dict()
        return None

    def set_credential(self, uid, credential):
        user = self.__query(uid)
        if user:
            user.update(credential=credential)
            return True
        return False

    def set_wireguard(self, uid, wireguard_id, user_conf, judge_conf):
        user = self.__query(uid)
        if user:
            wg_conf = WGConf(id=wireguard_id,
                             user_conf=user_conf,
                             judge_conf=judge_conf)
            user.update(wireguard_conf=wg_conf)
            return True
        return False

    def revoke_wireguard(self, uid):
        user = self.__query(uid)
        if user:
            user.wireguard_conf = None
            user.save()
            return True
        return False

    def filter_used_wg_id(self, pool):
        user_documents = User.objects(wireguard_conf__exists=True)

        for user in user_documents:
            pool.remove(user['wireguard_conf']['id'])

        return pool
