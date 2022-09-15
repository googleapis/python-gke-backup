# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from google.auth.transport.requests import AuthorizedSession  # type: ignore
import json  # type: ignore
import grpc  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.api_core import exceptions as core_exceptions
from google.api_core import retry as retries
from google.api_core import rest_helpers
from google.api_core import rest_streaming
from google.api_core import path_template
from google.api_core import gapic_v1

from google.protobuf import json_format
from google.api_core import operations_v1
from requests import __version__ as requests_version
import dataclasses
import re
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Union
import warnings

try:
    OptionalRetry = Union[retries.Retry, gapic_v1.method._MethodDefault]
except AttributeError:  # pragma: NO COVER
    OptionalRetry = Union[retries.Retry, object]  # type: ignore


from google.cloud.gke_backup_v1.types import backup
from google.cloud.gke_backup_v1.types import backup_plan
from google.cloud.gke_backup_v1.types import gkebackup
from google.cloud.gke_backup_v1.types import restore
from google.cloud.gke_backup_v1.types import restore_plan
from google.cloud.gke_backup_v1.types import volume
from google.longrunning import operations_pb2  # type: ignore

from .base import BackupForGKETransport, DEFAULT_CLIENT_INFO as BASE_DEFAULT_CLIENT_INFO


DEFAULT_CLIENT_INFO = gapic_v1.client_info.ClientInfo(
    gapic_version=BASE_DEFAULT_CLIENT_INFO.gapic_version,
    grpc_version=None,
    rest_version=requests_version,
)


class BackupForGKERestInterceptor:
    """Interceptor for BackupForGKE.

    Interceptors are used to manipulate requests, request metadata, and responses
    in arbitrary ways.
    Example use cases include:
    * Logging
    * Verifying requests according to service or custom semantics
    * Stripping extraneous information from responses

    These use cases and more can be enabled by injecting an
    instance of a custom subclass when constructing the BackupForGKERestTransport.

    .. code-block:: python
        class MyCustomBackupForGKEInterceptor(BackupForGKERestInterceptor):
            def pre_create_backup(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup(response):
                logging.log(f"Received response: {response}")

            def pre_create_backup_plan(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_backup_plan(response):
                logging.log(f"Received response: {response}")

            def pre_create_restore(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_restore(response):
                logging.log(f"Received response: {response}")

            def pre_create_restore_plan(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_create_restore_plan(response):
                logging.log(f"Received response: {response}")

            def pre_delete_backup(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup(response):
                logging.log(f"Received response: {response}")

            def pre_delete_backup_plan(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_backup_plan(response):
                logging.log(f"Received response: {response}")

            def pre_delete_restore(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_restore(response):
                logging.log(f"Received response: {response}")

            def pre_delete_restore_plan(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_delete_restore_plan(response):
                logging.log(f"Received response: {response}")

            def pre_get_backup(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup(response):
                logging.log(f"Received response: {response}")

            def pre_get_backup_plan(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_backup_plan(response):
                logging.log(f"Received response: {response}")

            def pre_get_restore(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_restore(response):
                logging.log(f"Received response: {response}")

            def pre_get_restore_plan(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_restore_plan(response):
                logging.log(f"Received response: {response}")

            def pre_get_volume_backup(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_volume_backup(response):
                logging.log(f"Received response: {response}")

            def pre_get_volume_restore(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_get_volume_restore(response):
                logging.log(f"Received response: {response}")

            def pre_list_backup_plans(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backup_plans(response):
                logging.log(f"Received response: {response}")

            def pre_list_backups(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_backups(response):
                logging.log(f"Received response: {response}")

            def pre_list_restore_plans(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_restore_plans(response):
                logging.log(f"Received response: {response}")

            def pre_list_restores(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_restores(response):
                logging.log(f"Received response: {response}")

            def pre_list_volume_backups(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_volume_backups(response):
                logging.log(f"Received response: {response}")

            def pre_list_volume_restores(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_list_volume_restores(response):
                logging.log(f"Received response: {response}")

            def pre_update_backup(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup(response):
                logging.log(f"Received response: {response}")

            def pre_update_backup_plan(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_backup_plan(response):
                logging.log(f"Received response: {response}")

            def pre_update_restore(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_restore(response):
                logging.log(f"Received response: {response}")

            def pre_update_restore_plan(request, metadata):
                logging.log(f"Received request: {request}")
                return request, metadata

            def post_update_restore_plan(response):
                logging.log(f"Received response: {response}")

        transport = BackupForGKERestTransport(interceptor=MyCustomBackupForGKEInterceptor())
        client = BackupForGKEClient(transport=transport)


    """

    def pre_create_backup(
        self,
        request: gkebackup.CreateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.CreateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_create_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_create_backup_plan(
        self,
        request: gkebackup.CreateBackupPlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.CreateBackupPlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_create_backup_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_create_restore(
        self,
        request: gkebackup.CreateRestoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.CreateRestoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_restore

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_create_restore(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_restore

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_create_restore_plan(
        self,
        request: gkebackup.CreateRestorePlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.CreateRestorePlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for create_restore_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_create_restore_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for create_restore_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup(
        self,
        request: gkebackup.DeleteBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.DeleteBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_delete_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_delete_backup_plan(
        self,
        request: gkebackup.DeleteBackupPlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.DeleteBackupPlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_delete_backup_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_delete_restore(
        self,
        request: gkebackup.DeleteRestoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.DeleteRestoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_restore

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_delete_restore(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_restore

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_delete_restore_plan(
        self,
        request: gkebackup.DeleteRestorePlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.DeleteRestorePlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for delete_restore_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_delete_restore_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for delete_restore_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup(
        self, request: gkebackup.GetBackupRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gkebackup.GetBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_backup(self, response: backup.Backup) -> backup.Backup:
        """Post-rpc interceptor for get_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_backup_plan(
        self,
        request: gkebackup.GetBackupPlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.GetBackupPlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_backup_plan(
        self, response: backup_plan.BackupPlan
    ) -> backup_plan.BackupPlan:
        """Post-rpc interceptor for get_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_restore(
        self, request: gkebackup.GetRestoreRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gkebackup.GetRestoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_restore

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_restore(self, response: restore.Restore) -> restore.Restore:
        """Post-rpc interceptor for get_restore

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_restore_plan(
        self,
        request: gkebackup.GetRestorePlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.GetRestorePlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_restore_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_restore_plan(
        self, response: restore_plan.RestorePlan
    ) -> restore_plan.RestorePlan:
        """Post-rpc interceptor for get_restore_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_volume_backup(
        self,
        request: gkebackup.GetVolumeBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.GetVolumeBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_volume_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_volume_backup(
        self, response: volume.VolumeBackup
    ) -> volume.VolumeBackup:
        """Post-rpc interceptor for get_volume_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_get_volume_restore(
        self,
        request: gkebackup.GetVolumeRestoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.GetVolumeRestoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for get_volume_restore

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_get_volume_restore(
        self, response: volume.VolumeRestore
    ) -> volume.VolumeRestore:
        """Post-rpc interceptor for get_volume_restore

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_backup_plans(
        self,
        request: gkebackup.ListBackupPlansRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.ListBackupPlansRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_backup_plans

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_backup_plans(
        self, response: gkebackup.ListBackupPlansResponse
    ) -> gkebackup.ListBackupPlansResponse:
        """Post-rpc interceptor for list_backup_plans

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_backups(
        self, request: gkebackup.ListBackupsRequest, metadata: Sequence[Tuple[str, str]]
    ) -> Tuple[gkebackup.ListBackupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_backups(
        self, response: gkebackup.ListBackupsResponse
    ) -> gkebackup.ListBackupsResponse:
        """Post-rpc interceptor for list_backups

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_restore_plans(
        self,
        request: gkebackup.ListRestorePlansRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.ListRestorePlansRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_restore_plans

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_restore_plans(
        self, response: gkebackup.ListRestorePlansResponse
    ) -> gkebackup.ListRestorePlansResponse:
        """Post-rpc interceptor for list_restore_plans

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_restores(
        self,
        request: gkebackup.ListRestoresRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.ListRestoresRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_restores

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_restores(
        self, response: gkebackup.ListRestoresResponse
    ) -> gkebackup.ListRestoresResponse:
        """Post-rpc interceptor for list_restores

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_volume_backups(
        self,
        request: gkebackup.ListVolumeBackupsRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.ListVolumeBackupsRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_volume_backups

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_volume_backups(
        self, response: gkebackup.ListVolumeBackupsResponse
    ) -> gkebackup.ListVolumeBackupsResponse:
        """Post-rpc interceptor for list_volume_backups

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_list_volume_restores(
        self,
        request: gkebackup.ListVolumeRestoresRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.ListVolumeRestoresRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for list_volume_restores

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_list_volume_restores(
        self, response: gkebackup.ListVolumeRestoresResponse
    ) -> gkebackup.ListVolumeRestoresResponse:
        """Post-rpc interceptor for list_volume_restores

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup(
        self,
        request: gkebackup.UpdateBackupRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.UpdateBackupRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_backup

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_update_backup(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_backup

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_update_backup_plan(
        self,
        request: gkebackup.UpdateBackupPlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.UpdateBackupPlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_backup_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_update_backup_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_backup_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_update_restore(
        self,
        request: gkebackup.UpdateRestoreRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.UpdateRestoreRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_restore

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_update_restore(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_restore

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response

    def pre_update_restore_plan(
        self,
        request: gkebackup.UpdateRestorePlanRequest,
        metadata: Sequence[Tuple[str, str]],
    ) -> Tuple[gkebackup.UpdateRestorePlanRequest, Sequence[Tuple[str, str]]]:
        """Pre-rpc interceptor for update_restore_plan

        Override in a subclass to manipulate the request or metadata
        before they are sent to the BackupForGKE server.
        """
        return request, metadata

    def post_update_restore_plan(
        self, response: operations_pb2.Operation
    ) -> operations_pb2.Operation:
        """Post-rpc interceptor for update_restore_plan

        Override in a subclass to manipulate the response
        after it is returned by the BackupForGKE server but before
        it is returned to user code.
        """
        return response


@dataclasses.dataclass
class BackupForGKERestStub:
    _session: AuthorizedSession
    _host: str
    _interceptor: BackupForGKERestInterceptor


class BackupForGKERestTransport(BackupForGKETransport):
    """REST backend transport for BackupForGKE.

    BackupForGKE allows Kubernetes administrators to configure,
    execute, and manage backup and restore operations for their GKE
    clusters.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends JSON representations of protocol buffers over HTTP/1.1

    NOTE: This REST transport functionality is currently in a beta
    state (preview). We welcome your feedback via an issue in this
    library's source repository. Thank you!
    """

    def __init__(
        self,
        *,
        host: str = "gkebackup.googleapis.com",
        credentials: ga_credentials.Credentials = None,
        credentials_file: str = None,
        scopes: Sequence[str] = None,
        client_cert_source_for_mtls: Callable[[], Tuple[bytes, bytes]] = None,
        quota_project_id: Optional[str] = None,
        client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
        always_use_jwt_access: Optional[bool] = False,
        url_scheme: str = "https",
        interceptor: Optional[BackupForGKERestInterceptor] = None,
        api_audience: Optional[str] = None,
    ) -> None:
        """Instantiate the transport.

        NOTE: This REST transport functionality is currently in a beta
        state (preview). We welcome your feedback via a GitHub issue in
        this library's repository. Thank you!

         Args:
             host (Optional[str]):
                  The hostname to connect to.
             credentials (Optional[google.auth.credentials.Credentials]): The
                 authorization credentials to attach to requests. These
                 credentials identify the application to the service; if none
                 are specified, the client will attempt to ascertain the
                 credentials from the environment.

             credentials_file (Optional[str]): A file with credentials that can
                 be loaded with :func:`google.auth.load_credentials_from_file`.
                 This argument is ignored if ``channel`` is provided.
             scopes (Optional(Sequence[str])): A list of scopes. This argument is
                 ignored if ``channel`` is provided.
             client_cert_source_for_mtls (Callable[[], Tuple[bytes, bytes]]): Client
                 certificate to configure mutual TLS HTTP channel. It is ignored
                 if ``channel`` is provided.
             quota_project_id (Optional[str]): An optional project to use for billing
                 and quota.
             client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                 The client info used to send a user-agent string along with
                 API requests. If ``None``, then default info will be used.
                 Generally, you only need to set this if you are developing
                 your own client library.
             always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                 be used for service account credentials.
             url_scheme: the protocol scheme for the API endpoint.  Normally
                 "https", but for testing or local servers,
                 "http" can be specified.
        """
        # Run the base constructor
        # TODO(yon-mg): resolve other ctor params i.e. scopes, quota, etc.
        # TODO: When custom host (api_endpoint) is set, `scopes` must *also* be set on the
        # credentials object
        maybe_url_match = re.match("^(?P<scheme>http(?:s)?://)?(?P<host>.*)$", host)
        if maybe_url_match is None:
            raise ValueError(
                f"Unexpected hostname structure: {host}"
            )  # pragma: NO COVER

        url_match_items = maybe_url_match.groupdict()

        host = f"{url_scheme}://{host}" if not url_match_items["scheme"] else host

        super().__init__(
            host=host,
            credentials=credentials,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )
        self._session = AuthorizedSession(
            self._credentials, default_host=self.DEFAULT_HOST
        )
        self._operations_client: Optional[operations_v1.AbstractOperationsClient] = None
        if client_cert_source_for_mtls:
            self._session.configure_mtls_channel(client_cert_source_for_mtls)
        self._interceptor = interceptor or BackupForGKERestInterceptor()
        self._prep_wrapped_messages(client_info)

    @property
    def operations_client(self) -> operations_v1.AbstractOperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Only create a new client if we do not already have one.
        if self._operations_client is None:
            http_options: Dict[str, List[Dict[str, str]]] = {}

            rest_transport = operations_v1.OperationsRestTransport(
                host=self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                scopes=self._scopes,
                http_options=http_options,
            )

            self._operations_client = operations_v1.AbstractOperationsClient(
                transport=rest_transport
            )

        # Return the client from cache.
        return self._operations_client

    class _CreateBackup(BackupForGKERestStub):
        def __hash__(self):
            return hash("CreateBackup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.CreateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup method over HTTP.

            Args:
                request (~.gkebackup.CreateBackupRequest):
                    The request object. Request message for CreateBackup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/backupPlans/*}/backups",
                    "body": "backup",
                },
            ]
            request, metadata = self._interceptor.pre_create_backup(request, metadata)
            pb_request = gkebackup.CreateBackupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_backup(resp)
            return resp

    class _CreateBackupPlan(BackupForGKERestStub):
        def __hash__(self):
            return hash("CreateBackupPlan")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "backupPlanId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.CreateBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create backup plan method over HTTP.

            Args:
                request (~.gkebackup.CreateBackupPlanRequest):
                    The request object. Request message for CreateBackupPlan.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/backupPlans",
                    "body": "backup_plan",
                },
            ]
            request, metadata = self._interceptor.pre_create_backup_plan(
                request, metadata
            )
            pb_request = gkebackup.CreateBackupPlanRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_backup_plan(resp)
            return resp

    class _CreateRestore(BackupForGKERestStub):
        def __hash__(self):
            return hash("CreateRestore")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "restoreId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.CreateRestoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create restore method over HTTP.

            Args:
                request (~.gkebackup.CreateRestoreRequest):
                    The request object. Request message for CreateRestore.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*/restorePlans/*}/restores",
                    "body": "restore",
                },
            ]
            request, metadata = self._interceptor.pre_create_restore(request, metadata)
            pb_request = gkebackup.CreateRestoreRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_restore(resp)
            return resp

    class _CreateRestorePlan(BackupForGKERestStub):
        def __hash__(self):
            return hash("CreateRestorePlan")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {
            "restorePlanId": "",
        }

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.CreateRestorePlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the create restore plan method over HTTP.

            Args:
                request (~.gkebackup.CreateRestorePlanRequest):
                    The request object. Request message for
                CreateRestorePlan.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "post",
                    "uri": "/v1/{parent=projects/*/locations/*}/restorePlans",
                    "body": "restore_plan",
                },
            ]
            request, metadata = self._interceptor.pre_create_restore_plan(
                request, metadata
            )
            pb_request = gkebackup.CreateRestorePlanRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_create_restore_plan(resp)
            return resp

    class _DeleteBackup(BackupForGKERestStub):
        def __hash__(self):
            return hash("DeleteBackup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.DeleteBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup method over HTTP.

            Args:
                request (~.gkebackup.DeleteBackupRequest):
                    The request object. Request message for DeleteBackup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/backupPlans/*/backups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_backup(request, metadata)
            pb_request = gkebackup.DeleteBackupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_backup(resp)
            return resp

    class _DeleteBackupPlan(BackupForGKERestStub):
        def __hash__(self):
            return hash("DeleteBackupPlan")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.DeleteBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete backup plan method over HTTP.

            Args:
                request (~.gkebackup.DeleteBackupPlanRequest):
                    The request object. Request message for DeleteBackupPlan.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/backupPlans/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_backup_plan(
                request, metadata
            )
            pb_request = gkebackup.DeleteBackupPlanRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_backup_plan(resp)
            return resp

    class _DeleteRestore(BackupForGKERestStub):
        def __hash__(self):
            return hash("DeleteRestore")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.DeleteRestoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete restore method over HTTP.

            Args:
                request (~.gkebackup.DeleteRestoreRequest):
                    The request object. Request message for DeleteRestore.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/restorePlans/*/restores/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_restore(request, metadata)
            pb_request = gkebackup.DeleteRestoreRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_restore(resp)
            return resp

    class _DeleteRestorePlan(BackupForGKERestStub):
        def __hash__(self):
            return hash("DeleteRestorePlan")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.DeleteRestorePlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the delete restore plan method over HTTP.

            Args:
                request (~.gkebackup.DeleteRestorePlanRequest):
                    The request object. Request message for
                DeleteRestorePlan.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "delete",
                    "uri": "/v1/{name=projects/*/locations/*/restorePlans/*}",
                },
            ]
            request, metadata = self._interceptor.pre_delete_restore_plan(
                request, metadata
            )
            pb_request = gkebackup.DeleteRestorePlanRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_delete_restore_plan(resp)
            return resp

    class _GetBackup(BackupForGKERestStub):
        def __hash__(self):
            return hash("GetBackup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.GetBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> backup.Backup:
            r"""Call the get backup method over HTTP.

            Args:
                request (~.gkebackup.GetBackupRequest):
                    The request object. Request message for GetBackup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.backup.Backup:
                    Represents a request to perform a
                single point-in-time capture of some
                portion of the state of a GKE cluster,
                the record of the backup operation
                itself, and an anchor for the underlying
                artifacts that comprise the Backup (the
                config backup and VolumeBackups). Next
                id: 28

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/backupPlans/*/backups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_backup(request, metadata)
            pb_request = gkebackup.GetBackupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = backup.Backup()
            pb_resp = backup.Backup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup(resp)
            return resp

    class _GetBackupPlan(BackupForGKERestStub):
        def __hash__(self):
            return hash("GetBackupPlan")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.GetBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> backup_plan.BackupPlan:
            r"""Call the get backup plan method over HTTP.

            Args:
                request (~.gkebackup.GetBackupPlanRequest):
                    The request object. Request message for GetBackupPlan.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.backup_plan.BackupPlan:
                    Defines the configuration and
                scheduling for a "line" of Backups.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/backupPlans/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_backup_plan(request, metadata)
            pb_request = gkebackup.GetBackupPlanRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = backup_plan.BackupPlan()
            pb_resp = backup_plan.BackupPlan.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_backup_plan(resp)
            return resp

    class _GetRestore(BackupForGKERestStub):
        def __hash__(self):
            return hash("GetRestore")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.GetRestoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> restore.Restore:
            r"""Call the get restore method over HTTP.

            Args:
                request (~.gkebackup.GetRestoreRequest):
                    The request object. Request message for GetRestore.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.restore.Restore:
                    Represents both a request to Restore
                some portion of a Backup into a target
                GKE cluster and a record of the restore
                operation itself. Next id: 18

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/restorePlans/*/restores/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_restore(request, metadata)
            pb_request = gkebackup.GetRestoreRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = restore.Restore()
            pb_resp = restore.Restore.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_restore(resp)
            return resp

    class _GetRestorePlan(BackupForGKERestStub):
        def __hash__(self):
            return hash("GetRestorePlan")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.GetRestorePlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> restore_plan.RestorePlan:
            r"""Call the get restore plan method over HTTP.

            Args:
                request (~.gkebackup.GetRestorePlanRequest):
                    The request object. Request message for GetRestorePlan.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.restore_plan.RestorePlan:
                    The configuration of a potential
                series of Restore operations to be
                performed against Backups belong to a
                particular BackupPlan. Next id: 11

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/restorePlans/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_restore_plan(
                request, metadata
            )
            pb_request = gkebackup.GetRestorePlanRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = restore_plan.RestorePlan()
            pb_resp = restore_plan.RestorePlan.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_restore_plan(resp)
            return resp

    class _GetVolumeBackup(BackupForGKERestStub):
        def __hash__(self):
            return hash("GetVolumeBackup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.GetVolumeBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume.VolumeBackup:
            r"""Call the get volume backup method over HTTP.

            Args:
                request (~.gkebackup.GetVolumeBackupRequest):
                    The request object. Request message for GetVolumeBackup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume.VolumeBackup:
                    Represents the backup of a specific
                persistent volume as a component of a
                Backup - both the record of the
                operation and a pointer to the
                underlying storage-specific artifacts.
                Next id: 14

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/backupPlans/*/backups/*/volumeBackups/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_volume_backup(
                request, metadata
            )
            pb_request = gkebackup.GetVolumeBackupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = volume.VolumeBackup()
            pb_resp = volume.VolumeBackup.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_volume_backup(resp)
            return resp

    class _GetVolumeRestore(BackupForGKERestStub):
        def __hash__(self):
            return hash("GetVolumeRestore")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.GetVolumeRestoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> volume.VolumeRestore:
            r"""Call the get volume restore method over HTTP.

            Args:
                request (~.gkebackup.GetVolumeRestoreRequest):
                    The request object. Request message for GetVolumeRestore.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.volume.VolumeRestore:
                    Represents the operation of restoring
                a volume from a VolumeBackup. Next id:
                13

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{name=projects/*/locations/*/restorePlans/*/restores/*/volumeRestores/*}",
                },
            ]
            request, metadata = self._interceptor.pre_get_volume_restore(
                request, metadata
            )
            pb_request = gkebackup.GetVolumeRestoreRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = volume.VolumeRestore()
            pb_resp = volume.VolumeRestore.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_get_volume_restore(resp)
            return resp

    class _ListBackupPlans(BackupForGKERestStub):
        def __hash__(self):
            return hash("ListBackupPlans")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.ListBackupPlansRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListBackupPlansResponse:
            r"""Call the list backup plans method over HTTP.

            Args:
                request (~.gkebackup.ListBackupPlansRequest):
                    The request object. Request message for ListBackupPlans.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListBackupPlansResponse:
                    Response message for ListBackupPlans.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/backupPlans",
                },
            ]
            request, metadata = self._interceptor.pre_list_backup_plans(
                request, metadata
            )
            pb_request = gkebackup.ListBackupPlansRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gkebackup.ListBackupPlansResponse()
            pb_resp = gkebackup.ListBackupPlansResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_backup_plans(resp)
            return resp

    class _ListBackups(BackupForGKERestStub):
        def __hash__(self):
            return hash("ListBackups")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.ListBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListBackupsResponse:
            r"""Call the list backups method over HTTP.

            Args:
                request (~.gkebackup.ListBackupsRequest):
                    The request object. Request message for ListBackups.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListBackupsResponse:
                    Response message for ListBackups.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/backupPlans/*}/backups",
                },
            ]
            request, metadata = self._interceptor.pre_list_backups(request, metadata)
            pb_request = gkebackup.ListBackupsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gkebackup.ListBackupsResponse()
            pb_resp = gkebackup.ListBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_backups(resp)
            return resp

    class _ListRestorePlans(BackupForGKERestStub):
        def __hash__(self):
            return hash("ListRestorePlans")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.ListRestorePlansRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListRestorePlansResponse:
            r"""Call the list restore plans method over HTTP.

            Args:
                request (~.gkebackup.ListRestorePlansRequest):
                    The request object. Request message for ListRestorePlans.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListRestorePlansResponse:
                    Response message for
                ListRestorePlans.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*}/restorePlans",
                },
            ]
            request, metadata = self._interceptor.pre_list_restore_plans(
                request, metadata
            )
            pb_request = gkebackup.ListRestorePlansRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gkebackup.ListRestorePlansResponse()
            pb_resp = gkebackup.ListRestorePlansResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_restore_plans(resp)
            return resp

    class _ListRestores(BackupForGKERestStub):
        def __hash__(self):
            return hash("ListRestores")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.ListRestoresRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListRestoresResponse:
            r"""Call the list restores method over HTTP.

            Args:
                request (~.gkebackup.ListRestoresRequest):
                    The request object. Request message for ListRestores.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListRestoresResponse:
                    Response message for ListRestores.
            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/restorePlans/*}/restores",
                },
            ]
            request, metadata = self._interceptor.pre_list_restores(request, metadata)
            pb_request = gkebackup.ListRestoresRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gkebackup.ListRestoresResponse()
            pb_resp = gkebackup.ListRestoresResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_restores(resp)
            return resp

    class _ListVolumeBackups(BackupForGKERestStub):
        def __hash__(self):
            return hash("ListVolumeBackups")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.ListVolumeBackupsRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListVolumeBackupsResponse:
            r"""Call the list volume backups method over HTTP.

            Args:
                request (~.gkebackup.ListVolumeBackupsRequest):
                    The request object. Request message for
                ListVolumeBackups.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListVolumeBackupsResponse:
                    Response message for
                ListVolumeBackups.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/backupPlans/*/backups/*}/volumeBackups",
                },
            ]
            request, metadata = self._interceptor.pre_list_volume_backups(
                request, metadata
            )
            pb_request = gkebackup.ListVolumeBackupsRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gkebackup.ListVolumeBackupsResponse()
            pb_resp = gkebackup.ListVolumeBackupsResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_volume_backups(resp)
            return resp

    class _ListVolumeRestores(BackupForGKERestStub):
        def __hash__(self):
            return hash("ListVolumeRestores")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.ListVolumeRestoresRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> gkebackup.ListVolumeRestoresResponse:
            r"""Call the list volume restores method over HTTP.

            Args:
                request (~.gkebackup.ListVolumeRestoresRequest):
                    The request object. Request message for
                ListVolumeRestores.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.gkebackup.ListVolumeRestoresResponse:
                    Response message for
                ListVolumeRestores.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "get",
                    "uri": "/v1/{parent=projects/*/locations/*/restorePlans/*/restores/*}/volumeRestores",
                },
            ]
            request, metadata = self._interceptor.pre_list_volume_restores(
                request, metadata
            )
            pb_request = gkebackup.ListVolumeRestoresRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = gkebackup.ListVolumeRestoresResponse()
            pb_resp = gkebackup.ListVolumeRestoresResponse.pb(resp)

            json_format.Parse(response.content, pb_resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_list_volume_restores(resp)
            return resp

    class _UpdateBackup(BackupForGKERestStub):
        def __hash__(self):
            return hash("UpdateBackup")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.UpdateBackupRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update backup method over HTTP.

            Args:
                request (~.gkebackup.UpdateBackupRequest):
                    The request object. Request message for UpdateBackup.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{backup.name=projects/*/locations/*/backupPlans/*/backups/*}",
                    "body": "backup",
                },
            ]
            request, metadata = self._interceptor.pre_update_backup(request, metadata)
            pb_request = gkebackup.UpdateBackupRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_backup(resp)
            return resp

    class _UpdateBackupPlan(BackupForGKERestStub):
        def __hash__(self):
            return hash("UpdateBackupPlan")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.UpdateBackupPlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update backup plan method over HTTP.

            Args:
                request (~.gkebackup.UpdateBackupPlanRequest):
                    The request object. Request message for UpdateBackupPlan.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{backup_plan.name=projects/*/locations/*/backupPlans/*}",
                    "body": "backup_plan",
                },
            ]
            request, metadata = self._interceptor.pre_update_backup_plan(
                request, metadata
            )
            pb_request = gkebackup.UpdateBackupPlanRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_backup_plan(resp)
            return resp

    class _UpdateRestore(BackupForGKERestStub):
        def __hash__(self):
            return hash("UpdateRestore")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.UpdateRestoreRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update restore method over HTTP.

            Args:
                request (~.gkebackup.UpdateRestoreRequest):
                    The request object. Request message for UpdateRestore.
                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{restore.name=projects/*/locations/*/restorePlans/*/restores/*}",
                    "body": "restore",
                },
            ]
            request, metadata = self._interceptor.pre_update_restore(request, metadata)
            pb_request = gkebackup.UpdateRestoreRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_restore(resp)
            return resp

    class _UpdateRestorePlan(BackupForGKERestStub):
        def __hash__(self):
            return hash("UpdateRestorePlan")

        __REQUIRED_FIELDS_DEFAULT_VALUES: Dict[str, str] = {}

        @classmethod
        def _get_unset_required_fields(cls, message_dict):
            return {
                k: v
                for k, v in cls.__REQUIRED_FIELDS_DEFAULT_VALUES.items()
                if k not in message_dict
            }

        def __call__(
            self,
            request: gkebackup.UpdateRestorePlanRequest,
            *,
            retry: OptionalRetry = gapic_v1.method.DEFAULT,
            timeout: float = None,
            metadata: Sequence[Tuple[str, str]] = (),
        ) -> operations_pb2.Operation:
            r"""Call the update restore plan method over HTTP.

            Args:
                request (~.gkebackup.UpdateRestorePlanRequest):
                    The request object. Request message for
                UpdateRestorePlan.

                retry (google.api_core.retry.Retry): Designation of what errors, if any,
                    should be retried.
                timeout (float): The timeout for this request.
                metadata (Sequence[Tuple[str, str]]): Strings which should be
                    sent along with the request as metadata.

            Returns:
                ~.operations_pb2.Operation:
                    This resource represents a
                long-running operation that is the
                result of a network API call.

            """

            http_options: List[Dict[str, str]] = [
                {
                    "method": "patch",
                    "uri": "/v1/{restore_plan.name=projects/*/locations/*/restorePlans/*}",
                    "body": "restore_plan",
                },
            ]
            request, metadata = self._interceptor.pre_update_restore_plan(
                request, metadata
            )
            pb_request = gkebackup.UpdateRestorePlanRequest.pb(request)
            transcoded_request = path_template.transcode(http_options, pb_request)

            # Jsonify the request body

            body = json_format.MessageToJson(
                transcoded_request["body"],
                including_default_value_fields=False,
                use_integers_for_enums=False,
            )
            uri = transcoded_request["uri"]
            method = transcoded_request["method"]

            # Jsonify the query params
            query_params = json.loads(
                json_format.MessageToJson(
                    transcoded_request["query_params"],
                    including_default_value_fields=False,
                    use_integers_for_enums=False,
                )
            )
            query_params.update(self._get_unset_required_fields(query_params))

            # Send the request
            headers = dict(metadata)
            headers["Content-Type"] = "application/json"
            response = getattr(self._session, method)(
                "{host}{uri}".format(host=self._host, uri=uri),
                timeout=timeout,
                headers=headers,
                params=rest_helpers.flatten_query_params(query_params, strict=True),
                data=body,
            )

            # In case of error, raise the appropriate core_exceptions.GoogleAPICallError exception
            # subclass.
            if response.status_code >= 400:
                raise core_exceptions.from_http_response(response)

            # Return the response
            resp = operations_pb2.Operation()
            json_format.Parse(response.content, resp, ignore_unknown_fields=True)
            resp = self._interceptor.post_update_restore_plan(resp)
            return resp

    @property
    def create_backup(
        self,
    ) -> Callable[[gkebackup.CreateBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_backup_plan(
        self,
    ) -> Callable[[gkebackup.CreateBackupPlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_restore(
        self,
    ) -> Callable[[gkebackup.CreateRestoreRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRestore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def create_restore_plan(
        self,
    ) -> Callable[[gkebackup.CreateRestorePlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._CreateRestorePlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup(
        self,
    ) -> Callable[[gkebackup.DeleteBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_backup_plan(
        self,
    ) -> Callable[[gkebackup.DeleteBackupPlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_restore(
        self,
    ) -> Callable[[gkebackup.DeleteRestoreRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRestore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def delete_restore_plan(
        self,
    ) -> Callable[[gkebackup.DeleteRestorePlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._DeleteRestorePlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup(self) -> Callable[[gkebackup.GetBackupRequest], backup.Backup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_backup_plan(
        self,
    ) -> Callable[[gkebackup.GetBackupPlanRequest], backup_plan.BackupPlan]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_restore(self) -> Callable[[gkebackup.GetRestoreRequest], restore.Restore]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRestore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_restore_plan(
        self,
    ) -> Callable[[gkebackup.GetRestorePlanRequest], restore_plan.RestorePlan]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetRestorePlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_volume_backup(
        self,
    ) -> Callable[[gkebackup.GetVolumeBackupRequest], volume.VolumeBackup]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVolumeBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def get_volume_restore(
        self,
    ) -> Callable[[gkebackup.GetVolumeRestoreRequest], volume.VolumeRestore]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._GetVolumeRestore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backup_plans(
        self,
    ) -> Callable[
        [gkebackup.ListBackupPlansRequest], gkebackup.ListBackupPlansResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackupPlans(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_backups(
        self,
    ) -> Callable[[gkebackup.ListBackupsRequest], gkebackup.ListBackupsResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_restore_plans(
        self,
    ) -> Callable[
        [gkebackup.ListRestorePlansRequest], gkebackup.ListRestorePlansResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRestorePlans(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_restores(
        self,
    ) -> Callable[[gkebackup.ListRestoresRequest], gkebackup.ListRestoresResponse]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListRestores(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_volume_backups(
        self,
    ) -> Callable[
        [gkebackup.ListVolumeBackupsRequest], gkebackup.ListVolumeBackupsResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVolumeBackups(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def list_volume_restores(
        self,
    ) -> Callable[
        [gkebackup.ListVolumeRestoresRequest], gkebackup.ListVolumeRestoresResponse
    ]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._ListVolumeRestores(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup(
        self,
    ) -> Callable[[gkebackup.UpdateBackupRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackup(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_backup_plan(
        self,
    ) -> Callable[[gkebackup.UpdateBackupPlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateBackupPlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_restore(
        self,
    ) -> Callable[[gkebackup.UpdateRestoreRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRestore(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def update_restore_plan(
        self,
    ) -> Callable[[gkebackup.UpdateRestorePlanRequest], operations_pb2.Operation]:
        # The return type is fine, but mypy isn't sophisticated enough to determine what's going on here.
        # In C++ this would require a dynamic_cast
        return self._UpdateRestorePlan(self._session, self._host, self._interceptor)  # type: ignore

    @property
    def kind(self) -> str:
        return "rest"

    def close(self):
        self._session.close()


__all__ = ("BackupForGKERestTransport",)
