# encoding: utf-8

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.multiuploadform.controllers import UploadController
from ckanext.multiuploadform import views


class multiuploadformPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, "templates")
        toolkit.add_public_directory(config_, "public")
        toolkit.add_resource("fanstatic", "multiuploadform")
        toolkit.add_resource("public/statics", "ckanext-multiuploadform")

    # IBlueprint

    def get_blueprint(self):
        return views.get_blueprint()

    # ITemplateHelpers

    def get_helpers(self):
        return {
            "cancel_dataset_is_enabled": UploadController.cancel_dataset_plugin_is_enabled,
            "get_max_upload_size": UploadController.get_upload_limit,
        }
