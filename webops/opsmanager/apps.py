from django.apps import AppConfig
from .register import _register
from django.conf import settings
import imp
import importlib
 
class OpsAppConfig(AppConfig):

    name = 'opsmanager'
    verbose_name = 'OpsManager'
    loaded = False
 
    def ready(self):
        #TODO (maybe): this could go elsewhere, for example in apps.py?
        if self.loaded:
            return

        for app in settings.INSTALLED_APPS:
            # For each app, we need to look for an webops.py inside that app's
            # package. We can't use os.path here -- recall that modules may be
            # imported different ways (think zip files) -- so we need to get
            # the app's __path__ and look for admin.py on that path.

            # Step 1: find out the app's __path__ Import errors here will (and
            # should) bubble up, but a missing __path__ (which is legal, but weird)
            # fails silently -- apps that do weird things with __path__ might
            # need to roll their own admin registration.
            try:
                app_path = importlib.import_module(app).__path__
            except AttributeError:
                continue

            # Step 2: use imp.find_module to find the app's webops.py. For some
            # reason imp.find_module raises ImportError if the app can't be found
            # but doesn't actually try to import the module. So skip this app if
            # its webops.py doesn't exist
            try:
                imp.find_module('webops', app_path)
            except ImportError:
                continue

            # Step 3: import the app's admin file. If this has errors we want them
            # to bubble up.
            importlib.import_module("%s.webops" % app)
        # autodiscover was successful, reset loading flag.
        self.loaded = True
         
                