class AuthRouter(object):
    """
    A router to control all database operations on models in the
    troca application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read troca models go to nonrel_troca_db.
        """
        if model._meta.app_label == 'nonrel_troca_app':
            return 'nonrel_troca_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write troca models go to nonrel_troca_db.
        """
        if model._meta.app_label == 'nonrel_troca_app':
            return 'nonrel_troca_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the troca app is involved.
        """
        if obj1._meta.app_label == 'nonrel_troca_app' or \
           obj2._meta.app_label == 'nonrel_troca_app':
           return True
        return None

    def allow_syncdb(self, db, model):
        """
        Make sure the troca app only appears in the 'nonrel_troca_db'
        database.
        """
        if db == 'nonrel_troca_db':
            return model._meta.app_label == 'nonrel_troca_app'
        elif model._meta.app_label == 'nonrel_troca_app':
            return False
        return None