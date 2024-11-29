from flask import Blueprint
from flask.views import MethodView
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as core_helpers
import ckan.lib.base as base
from flask import request
from ckanext.multiuploader.controllers import UploadController
from ckan.types import Context, Response
from typing import Any, Optional, Union
from ckan.common import _, config, g, request, current_user
import ckan.lib.navl.dictization_functions as dict_fns

log = __import__("logging").getLogger(__name__)


blueprint = Blueprint(
    "multiuploader", __name__, url_defaults={"package_type": "dataset"}
)


class MultiUploaderView(MethodView):
    def post(self, package_type: str, id: str) -> Union[str, Response]:
        context: Context = {"user": current_user.name, "auth_user_obj": current_user}
        # data = clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(request.form))))
        try:
            pkg_dict = toolkit.get_action("package_show")({}, {"id": id})
        except (toolkit.ObjectNotFound, toolkit.NotAuthorized):
            base.abort(404, "Resource not found")
        try:
            data_dict = toolkit.get_action("package_show")(context, {"id": id})
        except toolkit.NotAuthorized:
            return base.abort(403, _("Unauthorized to update dataset"))
        except toolkit.NotFound:
            return base.abort(
                404, _("The dataset {id} could not be found.").format(id=id)
            )
        return toolkit.redirect_to("{}.read".format(package_type), id=id)

    def get(
        self,
        package_type: str,
        id: str,
        data: Optional[dict[str, Any]] = None,
        errors: Optional[dict[str, Any]] = None,
        error_summary: Optional[dict[str, Any]] = None,
    ) -> str:
        # get resources for sidebar
        context: Context = {"user": current_user.name, "auth_user_obj": current_user}
        try:
            pkg_dict = toolkit.get_action("package_show")(context, {"id": id})
        except toolkit.NotFound:
            return base.abort(
                404, _("The dataset {id} could not be found.").format(id=id)
            )
        try:
            toolkit.check_access(
                "resource_create", context, {"package_id": pkg_dict["id"]}
            )
        except toolkit.NotAuthorized:
            return base.abort(
                403, _("Unauthorized to create a resource for this package")
            )

        package_type = pkg_dict["type"] or package_type

        errors = errors or {}
        error_summary = error_summary or {}
        extra_vars: dict[str, Any] = {
            "data": data,
            "errors": errors,
            "error_summary": error_summary,
            # u'action': u'new',
            "resource_form_snippet": "multiuploader/snippets/multiupload_form.html",
            "dataset_type": package_type,
            "pkg_name": id,
            "pkg_dict": pkg_dict,
        }
        template = "package/new_resource_not_draft.html"
        if pkg_dict["state"].startswith("draft"):
            extra_vars["stage"] = ["complete", "active"]
            template = "package/new_resource.html"
        return base.render(template, extra_vars)


blueprint.add_url_rule(
    "/dataset/<id>/resource/multiupload",
    view_func=MultiUploaderView.as_view(str("resource_view")),
)

blueprint.add_url_rule(
    "/multiuploader/upload_resources",
    "upload_resources",
    UploadController.upload_resources,
    methods=["POST"],
)

blueprint.add_url_rule(
    "/multiuploader/delete_uploaded_resources",
    "delete_uploaded_resources",
    UploadController.delete_uploaded_resources,
    methods=["POST"],
)


def get_blueprint():
    return blueprint
