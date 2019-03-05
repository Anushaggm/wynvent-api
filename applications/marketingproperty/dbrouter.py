

class MasterSlaveRouter(object):

    def db_for_read(self, model, **hints):
        "Point all operations on marketing_property models to 'properties'"
        if model._meta.app_label == 'marketingproperty':
            return 'properties'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to properties.
        """
        if model._meta.app_label == 'marketingproperty':
            return 'properties'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a both models in marketing_property app"
        if obj1._meta.app_label == 'marketingproperty' and obj2._meta.app_label == 'marketingproperty':
            return True
        # Allow if neither is marketing_property app
        elif 'marketingproperty' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    # def allow_syncdb(self, db, model):
    #     if db == 'properties' or model._meta.app_label == "marketingproperty":
    #         return False # we're not using syncdb on our legacy database
    #     else: # but all other models/databases are fine
    #         return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'properties'
        database.
        """
        if app_label == 'marketingproperty':
            return db == 'properties'
        return None