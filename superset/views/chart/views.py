# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
from flask_appbuilder import expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _

from superset import security_manager
from superset.constants import MODEL_VIEW_RW_METHOD_PERMISSION_MAP, RouteMethod
from superset.models.slice import Slice
from superset.superset_typing import FlaskResponse
from superset.utils import core as utils
from superset.views.base import DeleteMixin, SupersetModelView
from superset.views.chart.mixin import SliceMixin


class SliceModelView(SliceMixin, SupersetModelView, DeleteMixin):  # pylint: disable=too-many-ancestors
    route_base = "/chart"
    datamodel = SQLAInterface(Slice)
    include_route_methods = RouteMethod.CRUD_SET | {
        RouteMethod.DOWNLOAD,
        RouteMethod.API_READ,
        RouteMethod.API_DELETE,
    }
    class_permission_name = "Chart"
    method_permission_name = MODEL_VIEW_RW_METHOD_PERMISSION_MAP

    def pre_add(self, item: "SliceModelView") -> None:
        utils.validate_json(item.params)

    def pre_update(self, item: "SliceModelView") -> None:
        utils.validate_json(item.params)
        security_manager.raise_for_ownership(item)

    def pre_delete(self, item: "SliceModelView") -> None:
        security_manager.raise_for_ownership(item)

    @expose(
        "/add",
        methods=(
            "GET",
            "POST",
        ),
    )
    @has_access
    def add(self) -> FlaskResponse:
        return super().render_app_template()

    @expose("/list/")
    @has_access
    def list(self) -> FlaskResponse:
        return super().render_app_template()


class SliceAsync(SliceModelView):  # pylint: disable=too-many-ancestors
    route_base = "/sliceasync"
    include_route_methods = {RouteMethod.API_READ}

    list_columns = [
        "changed_on",
        "changed_on_humanized",
        "creator",
        "datasource_id",
        "datasource_link",
        "datasource_url",
        "datasource_name_text",
        "datasource_type",
        "description",
        "description_markeddown",
        "edit_url",
        "icons",
        "id",
        "modified",
        "owners",
        "params",
        "slice_link",
        "slice_name",
        "slice_url",
        "viz_type",
    ]
    label_columns = {"icons": " ", "slice_link": _("Chart")}
