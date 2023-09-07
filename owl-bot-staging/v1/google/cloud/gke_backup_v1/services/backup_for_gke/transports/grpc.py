# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
import warnings
from typing import Callable, Dict, Optional, Sequence, Tuple, Union

from google.api_core import grpc_helpers
from google.api_core import operations_v1
from google.api_core import gapic_v1
import google.auth                         # type: ignore
from google.auth import credentials as ga_credentials  # type: ignore
from google.auth.transport.grpc import SslCredentials  # type: ignore

import grpc  # type: ignore

from google.cloud.gke_backup_v1.types import backup
from google.cloud.gke_backup_v1.types import backup_plan
from google.cloud.gke_backup_v1.types import gkebackup
from google.cloud.gke_backup_v1.types import restore
from google.cloud.gke_backup_v1.types import restore_plan
from google.cloud.gke_backup_v1.types import volume
from google.cloud.location import locations_pb2 # type: ignore
from google.iam.v1 import iam_policy_pb2  # type: ignore
from google.iam.v1 import policy_pb2  # type: ignore
from google.longrunning import operations_pb2 # type: ignore
from .base import BackupForGKETransport, DEFAULT_CLIENT_INFO


class BackupForGKEGrpcTransport(BackupForGKETransport):
    """gRPC backend transport for BackupForGKE.

    BackupForGKE allows Kubernetes administrators to configure,
    execute, and manage backup and restore operations for their GKE
    clusters.

    This class defines the same methods as the primary client, so the
    primary client can load the underlying transport implementation
    and call it.

    It sends protocol buffers over the wire using gRPC (which is built on
    top of HTTP/2); the ``grpcio`` package must be installed.
    """
    _stubs: Dict[str, Callable]

    def __init__(self, *,
            host: str = 'gkebackup.googleapis.com',
            credentials: Optional[ga_credentials.Credentials] = None,
            credentials_file: Optional[str] = None,
            scopes: Optional[Sequence[str]] = None,
            channel: Optional[grpc.Channel] = None,
            api_mtls_endpoint: Optional[str] = None,
            client_cert_source: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
            ssl_channel_credentials: Optional[grpc.ChannelCredentials] = None,
            client_cert_source_for_mtls: Optional[Callable[[], Tuple[bytes, bytes]]] = None,
            quota_project_id: Optional[str] = None,
            client_info: gapic_v1.client_info.ClientInfo = DEFAULT_CLIENT_INFO,
            always_use_jwt_access: Optional[bool] = False,
            api_audience: Optional[str] = None,
            ) -> None:
        """Instantiate the transport.

        Args:
            host (Optional[str]):
                 The hostname to connect to.
            credentials (Optional[google.auth.credentials.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify the application to the service; if none
                are specified, the client will attempt to ascertain the
                credentials from the environment.
                This argument is ignored if ``channel`` is provided.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is ignored if ``channel`` is provided.
            scopes (Optional(Sequence[str])): A list of scopes. This argument is
                ignored if ``channel`` is provided.
            channel (Optional[grpc.Channel]): A ``Channel`` instance through
                which to make calls.
            api_mtls_endpoint (Optional[str]): Deprecated. The mutual TLS endpoint.
                If provided, it overrides the ``host`` argument and tries to create
                a mutual TLS channel with client SSL credentials from
                ``client_cert_source`` or application default SSL credentials.
            client_cert_source (Optional[Callable[[], Tuple[bytes, bytes]]]):
                Deprecated. A callback to provide client SSL certificate bytes and
                private key bytes, both in PEM format. It is ignored if
                ``api_mtls_endpoint`` is None.
            ssl_channel_credentials (grpc.ChannelCredentials): SSL credentials
                for the grpc channel. It is ignored if ``channel`` is provided.
            client_cert_source_for_mtls (Optional[Callable[[], Tuple[bytes, bytes]]]):
                A callback to provide client certificate bytes and private key bytes,
                both in PEM format. It is used to configure a mutual TLS channel. It is
                ignored if ``channel`` or ``ssl_channel_credentials`` is provided.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            client_info (google.api_core.gapic_v1.client_info.ClientInfo):
                The client info used to send a user-agent string along with
                API requests. If ``None``, then default info will be used.
                Generally, you only need to set this if you're developing
                your own client library.
            always_use_jwt_access (Optional[bool]): Whether self signed JWT should
                be used for service account credentials.

        Raises:
          google.auth.exceptions.MutualTLSChannelError: If mutual TLS transport
              creation failed for any reason.
          google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """
        self._grpc_channel = None
        self._ssl_channel_credentials = ssl_channel_credentials
        self._stubs: Dict[str, Callable] = {}
        self._operations_client: Optional[operations_v1.OperationsClient] = None

        if api_mtls_endpoint:
            warnings.warn("api_mtls_endpoint is deprecated", DeprecationWarning)
        if client_cert_source:
            warnings.warn("client_cert_source is deprecated", DeprecationWarning)

        if channel:
            # Ignore credentials if a channel was passed.
            credentials = False
            # If a channel was explicitly provided, set it.
            self._grpc_channel = channel
            self._ssl_channel_credentials = None

        else:
            if api_mtls_endpoint:
                host = api_mtls_endpoint

                # Create SSL credentials with client_cert_source or application
                # default SSL credentials.
                if client_cert_source:
                    cert, key = client_cert_source()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )
                else:
                    self._ssl_channel_credentials = SslCredentials().ssl_credentials

            else:
                if client_cert_source_for_mtls and not ssl_channel_credentials:
                    cert, key = client_cert_source_for_mtls()
                    self._ssl_channel_credentials = grpc.ssl_channel_credentials(
                        certificate_chain=cert, private_key=key
                    )

        # The base transport sets the host, credentials and scopes
        super().__init__(
            host=host,
            credentials=credentials,
            credentials_file=credentials_file,
            scopes=scopes,
            quota_project_id=quota_project_id,
            client_info=client_info,
            always_use_jwt_access=always_use_jwt_access,
            api_audience=api_audience,
        )

        if not self._grpc_channel:
            self._grpc_channel = type(self).create_channel(
                self._host,
                # use the credentials which are saved
                credentials=self._credentials,
                # Set ``credentials_file`` to ``None`` here as
                # the credentials that we saved earlier should be used.
                credentials_file=None,
                scopes=self._scopes,
                ssl_credentials=self._ssl_channel_credentials,
                quota_project_id=quota_project_id,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )

        # Wrap messages. This must be done after self._grpc_channel exists
        self._prep_wrapped_messages(client_info)

    @classmethod
    def create_channel(cls,
                       host: str = 'gkebackup.googleapis.com',
                       credentials: Optional[ga_credentials.Credentials] = None,
                       credentials_file: Optional[str] = None,
                       scopes: Optional[Sequence[str]] = None,
                       quota_project_id: Optional[str] = None,
                       **kwargs) -> grpc.Channel:
        """Create and return a gRPC channel object.
        Args:
            host (Optional[str]): The host for the channel to use.
            credentials (Optional[~.Credentials]): The
                authorization credentials to attach to requests. These
                credentials identify this application to the service. If
                none are specified, the client will attempt to ascertain
                the credentials from the environment.
            credentials_file (Optional[str]): A file with credentials that can
                be loaded with :func:`google.auth.load_credentials_from_file`.
                This argument is mutually exclusive with credentials.
            scopes (Optional[Sequence[str]]): A optional list of scopes needed for this
                service. These are only used when credentials are not specified and
                are passed to :func:`google.auth.default`.
            quota_project_id (Optional[str]): An optional project to use for billing
                and quota.
            kwargs (Optional[dict]): Keyword arguments, which are passed to the
                channel creation.
        Returns:
            grpc.Channel: A gRPC channel object.

        Raises:
            google.api_core.exceptions.DuplicateCredentialArgs: If both ``credentials``
              and ``credentials_file`` are passed.
        """

        return grpc_helpers.create_channel(
            host,
            credentials=credentials,
            credentials_file=credentials_file,
            quota_project_id=quota_project_id,
            default_scopes=cls.AUTH_SCOPES,
            scopes=scopes,
            default_host=cls.DEFAULT_HOST,
            **kwargs
        )

    @property
    def grpc_channel(self) -> grpc.Channel:
        """Return the channel designed to connect to this service.
        """
        return self._grpc_channel

    @property
    def operations_client(self) -> operations_v1.OperationsClient:
        """Create the client designed to process long-running operations.

        This property caches on the instance; repeated calls return the same
        client.
        """
        # Quick check: Only create a new client if we do not already have one.
        if self._operations_client is None:
            self._operations_client = operations_v1.OperationsClient(
                self.grpc_channel
            )

        # Return the client from cache.
        return self._operations_client

    @property
    def create_backup_plan(self) -> Callable[
            [gkebackup.CreateBackupPlanRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the create backup plan method over gRPC.

        Creates a new BackupPlan in a given location.

        Returns:
            Callable[[~.CreateBackupPlanRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_backup_plan' not in self._stubs:
            self._stubs['create_backup_plan'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/CreateBackupPlan',
                request_serializer=gkebackup.CreateBackupPlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_backup_plan']

    @property
    def list_backup_plans(self) -> Callable[
            [gkebackup.ListBackupPlansRequest],
            gkebackup.ListBackupPlansResponse]:
        r"""Return a callable for the list backup plans method over gRPC.

        Lists BackupPlans in a given location.

        Returns:
            Callable[[~.ListBackupPlansRequest],
                    ~.ListBackupPlansResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_backup_plans' not in self._stubs:
            self._stubs['list_backup_plans'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/ListBackupPlans',
                request_serializer=gkebackup.ListBackupPlansRequest.serialize,
                response_deserializer=gkebackup.ListBackupPlansResponse.deserialize,
            )
        return self._stubs['list_backup_plans']

    @property
    def get_backup_plan(self) -> Callable[
            [gkebackup.GetBackupPlanRequest],
            backup_plan.BackupPlan]:
        r"""Return a callable for the get backup plan method over gRPC.

        Retrieve the details of a single BackupPlan.

        Returns:
            Callable[[~.GetBackupPlanRequest],
                    ~.BackupPlan]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_backup_plan' not in self._stubs:
            self._stubs['get_backup_plan'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/GetBackupPlan',
                request_serializer=gkebackup.GetBackupPlanRequest.serialize,
                response_deserializer=backup_plan.BackupPlan.deserialize,
            )
        return self._stubs['get_backup_plan']

    @property
    def update_backup_plan(self) -> Callable[
            [gkebackup.UpdateBackupPlanRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the update backup plan method over gRPC.

        Update a BackupPlan.

        Returns:
            Callable[[~.UpdateBackupPlanRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_backup_plan' not in self._stubs:
            self._stubs['update_backup_plan'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/UpdateBackupPlan',
                request_serializer=gkebackup.UpdateBackupPlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_backup_plan']

    @property
    def delete_backup_plan(self) -> Callable[
            [gkebackup.DeleteBackupPlanRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the delete backup plan method over gRPC.

        Deletes an existing BackupPlan.

        Returns:
            Callable[[~.DeleteBackupPlanRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_backup_plan' not in self._stubs:
            self._stubs['delete_backup_plan'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/DeleteBackupPlan',
                request_serializer=gkebackup.DeleteBackupPlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_backup_plan']

    @property
    def create_backup(self) -> Callable[
            [gkebackup.CreateBackupRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the create backup method over gRPC.

        Creates a Backup for the given BackupPlan.

        Returns:
            Callable[[~.CreateBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_backup' not in self._stubs:
            self._stubs['create_backup'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/CreateBackup',
                request_serializer=gkebackup.CreateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_backup']

    @property
    def list_backups(self) -> Callable[
            [gkebackup.ListBackupsRequest],
            gkebackup.ListBackupsResponse]:
        r"""Return a callable for the list backups method over gRPC.

        Lists the Backups for a given BackupPlan.

        Returns:
            Callable[[~.ListBackupsRequest],
                    ~.ListBackupsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_backups' not in self._stubs:
            self._stubs['list_backups'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/ListBackups',
                request_serializer=gkebackup.ListBackupsRequest.serialize,
                response_deserializer=gkebackup.ListBackupsResponse.deserialize,
            )
        return self._stubs['list_backups']

    @property
    def get_backup(self) -> Callable[
            [gkebackup.GetBackupRequest],
            backup.Backup]:
        r"""Return a callable for the get backup method over gRPC.

        Retrieve the details of a single Backup.

        Returns:
            Callable[[~.GetBackupRequest],
                    ~.Backup]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_backup' not in self._stubs:
            self._stubs['get_backup'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/GetBackup',
                request_serializer=gkebackup.GetBackupRequest.serialize,
                response_deserializer=backup.Backup.deserialize,
            )
        return self._stubs['get_backup']

    @property
    def update_backup(self) -> Callable[
            [gkebackup.UpdateBackupRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the update backup method over gRPC.

        Update a Backup.

        Returns:
            Callable[[~.UpdateBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_backup' not in self._stubs:
            self._stubs['update_backup'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/UpdateBackup',
                request_serializer=gkebackup.UpdateBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_backup']

    @property
    def delete_backup(self) -> Callable[
            [gkebackup.DeleteBackupRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the delete backup method over gRPC.

        Deletes an existing Backup.

        Returns:
            Callable[[~.DeleteBackupRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_backup' not in self._stubs:
            self._stubs['delete_backup'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/DeleteBackup',
                request_serializer=gkebackup.DeleteBackupRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_backup']

    @property
    def list_volume_backups(self) -> Callable[
            [gkebackup.ListVolumeBackupsRequest],
            gkebackup.ListVolumeBackupsResponse]:
        r"""Return a callable for the list volume backups method over gRPC.

        Lists the VolumeBackups for a given Backup.

        Returns:
            Callable[[~.ListVolumeBackupsRequest],
                    ~.ListVolumeBackupsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_volume_backups' not in self._stubs:
            self._stubs['list_volume_backups'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/ListVolumeBackups',
                request_serializer=gkebackup.ListVolumeBackupsRequest.serialize,
                response_deserializer=gkebackup.ListVolumeBackupsResponse.deserialize,
            )
        return self._stubs['list_volume_backups']

    @property
    def get_volume_backup(self) -> Callable[
            [gkebackup.GetVolumeBackupRequest],
            volume.VolumeBackup]:
        r"""Return a callable for the get volume backup method over gRPC.

        Retrieve the details of a single VolumeBackup.

        Returns:
            Callable[[~.GetVolumeBackupRequest],
                    ~.VolumeBackup]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_volume_backup' not in self._stubs:
            self._stubs['get_volume_backup'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/GetVolumeBackup',
                request_serializer=gkebackup.GetVolumeBackupRequest.serialize,
                response_deserializer=volume.VolumeBackup.deserialize,
            )
        return self._stubs['get_volume_backup']

    @property
    def create_restore_plan(self) -> Callable[
            [gkebackup.CreateRestorePlanRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the create restore plan method over gRPC.

        Creates a new RestorePlan in a given location.

        Returns:
            Callable[[~.CreateRestorePlanRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_restore_plan' not in self._stubs:
            self._stubs['create_restore_plan'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/CreateRestorePlan',
                request_serializer=gkebackup.CreateRestorePlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_restore_plan']

    @property
    def list_restore_plans(self) -> Callable[
            [gkebackup.ListRestorePlansRequest],
            gkebackup.ListRestorePlansResponse]:
        r"""Return a callable for the list restore plans method over gRPC.

        Lists RestorePlans in a given location.

        Returns:
            Callable[[~.ListRestorePlansRequest],
                    ~.ListRestorePlansResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_restore_plans' not in self._stubs:
            self._stubs['list_restore_plans'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/ListRestorePlans',
                request_serializer=gkebackup.ListRestorePlansRequest.serialize,
                response_deserializer=gkebackup.ListRestorePlansResponse.deserialize,
            )
        return self._stubs['list_restore_plans']

    @property
    def get_restore_plan(self) -> Callable[
            [gkebackup.GetRestorePlanRequest],
            restore_plan.RestorePlan]:
        r"""Return a callable for the get restore plan method over gRPC.

        Retrieve the details of a single RestorePlan.

        Returns:
            Callable[[~.GetRestorePlanRequest],
                    ~.RestorePlan]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_restore_plan' not in self._stubs:
            self._stubs['get_restore_plan'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/GetRestorePlan',
                request_serializer=gkebackup.GetRestorePlanRequest.serialize,
                response_deserializer=restore_plan.RestorePlan.deserialize,
            )
        return self._stubs['get_restore_plan']

    @property
    def update_restore_plan(self) -> Callable[
            [gkebackup.UpdateRestorePlanRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the update restore plan method over gRPC.

        Update a RestorePlan.

        Returns:
            Callable[[~.UpdateRestorePlanRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_restore_plan' not in self._stubs:
            self._stubs['update_restore_plan'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/UpdateRestorePlan',
                request_serializer=gkebackup.UpdateRestorePlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_restore_plan']

    @property
    def delete_restore_plan(self) -> Callable[
            [gkebackup.DeleteRestorePlanRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the delete restore plan method over gRPC.

        Deletes an existing RestorePlan.

        Returns:
            Callable[[~.DeleteRestorePlanRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_restore_plan' not in self._stubs:
            self._stubs['delete_restore_plan'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/DeleteRestorePlan',
                request_serializer=gkebackup.DeleteRestorePlanRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_restore_plan']

    @property
    def create_restore(self) -> Callable[
            [gkebackup.CreateRestoreRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the create restore method over gRPC.

        Creates a new Restore for the given RestorePlan.

        Returns:
            Callable[[~.CreateRestoreRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'create_restore' not in self._stubs:
            self._stubs['create_restore'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/CreateRestore',
                request_serializer=gkebackup.CreateRestoreRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['create_restore']

    @property
    def list_restores(self) -> Callable[
            [gkebackup.ListRestoresRequest],
            gkebackup.ListRestoresResponse]:
        r"""Return a callable for the list restores method over gRPC.

        Lists the Restores for a given RestorePlan.

        Returns:
            Callable[[~.ListRestoresRequest],
                    ~.ListRestoresResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_restores' not in self._stubs:
            self._stubs['list_restores'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/ListRestores',
                request_serializer=gkebackup.ListRestoresRequest.serialize,
                response_deserializer=gkebackup.ListRestoresResponse.deserialize,
            )
        return self._stubs['list_restores']

    @property
    def get_restore(self) -> Callable[
            [gkebackup.GetRestoreRequest],
            restore.Restore]:
        r"""Return a callable for the get restore method over gRPC.

        Retrieves the details of a single Restore.

        Returns:
            Callable[[~.GetRestoreRequest],
                    ~.Restore]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_restore' not in self._stubs:
            self._stubs['get_restore'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/GetRestore',
                request_serializer=gkebackup.GetRestoreRequest.serialize,
                response_deserializer=restore.Restore.deserialize,
            )
        return self._stubs['get_restore']

    @property
    def update_restore(self) -> Callable[
            [gkebackup.UpdateRestoreRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the update restore method over gRPC.

        Update a Restore.

        Returns:
            Callable[[~.UpdateRestoreRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'update_restore' not in self._stubs:
            self._stubs['update_restore'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/UpdateRestore',
                request_serializer=gkebackup.UpdateRestoreRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['update_restore']

    @property
    def delete_restore(self) -> Callable[
            [gkebackup.DeleteRestoreRequest],
            operations_pb2.Operation]:
        r"""Return a callable for the delete restore method over gRPC.

        Deletes an existing Restore.

        Returns:
            Callable[[~.DeleteRestoreRequest],
                    ~.Operation]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'delete_restore' not in self._stubs:
            self._stubs['delete_restore'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/DeleteRestore',
                request_serializer=gkebackup.DeleteRestoreRequest.serialize,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs['delete_restore']

    @property
    def list_volume_restores(self) -> Callable[
            [gkebackup.ListVolumeRestoresRequest],
            gkebackup.ListVolumeRestoresResponse]:
        r"""Return a callable for the list volume restores method over gRPC.

        Lists the VolumeRestores for a given Restore.

        Returns:
            Callable[[~.ListVolumeRestoresRequest],
                    ~.ListVolumeRestoresResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'list_volume_restores' not in self._stubs:
            self._stubs['list_volume_restores'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/ListVolumeRestores',
                request_serializer=gkebackup.ListVolumeRestoresRequest.serialize,
                response_deserializer=gkebackup.ListVolumeRestoresResponse.deserialize,
            )
        return self._stubs['list_volume_restores']

    @property
    def get_volume_restore(self) -> Callable[
            [gkebackup.GetVolumeRestoreRequest],
            volume.VolumeRestore]:
        r"""Return a callable for the get volume restore method over gRPC.

        Retrieve the details of a single VolumeRestore.

        Returns:
            Callable[[~.GetVolumeRestoreRequest],
                    ~.VolumeRestore]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if 'get_volume_restore' not in self._stubs:
            self._stubs['get_volume_restore'] = self.grpc_channel.unary_unary(
                '/google.cloud.gkebackup.v1.BackupForGKE/GetVolumeRestore',
                request_serializer=gkebackup.GetVolumeRestoreRequest.serialize,
                response_deserializer=volume.VolumeRestore.deserialize,
            )
        return self._stubs['get_volume_restore']

    def close(self):
        self.grpc_channel.close()

    @property
    def delete_operation(
        self,
    ) -> Callable[[operations_pb2.DeleteOperationRequest], None]:
        r"""Return a callable for the delete_operation method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "delete_operation" not in self._stubs:
            self._stubs["delete_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/DeleteOperation",
                request_serializer=operations_pb2.DeleteOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["delete_operation"]

    @property
    def cancel_operation(
        self,
    ) -> Callable[[operations_pb2.CancelOperationRequest], None]:
        r"""Return a callable for the cancel_operation method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "cancel_operation" not in self._stubs:
            self._stubs["cancel_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/CancelOperation",
                request_serializer=operations_pb2.CancelOperationRequest.SerializeToString,
                response_deserializer=None,
            )
        return self._stubs["cancel_operation"]

    @property
    def get_operation(
        self,
    ) -> Callable[[operations_pb2.GetOperationRequest], operations_pb2.Operation]:
        r"""Return a callable for the get_operation method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_operation" not in self._stubs:
            self._stubs["get_operation"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/GetOperation",
                request_serializer=operations_pb2.GetOperationRequest.SerializeToString,
                response_deserializer=operations_pb2.Operation.FromString,
            )
        return self._stubs["get_operation"]

    @property
    def list_operations(
        self,
    ) -> Callable[[operations_pb2.ListOperationsRequest], operations_pb2.ListOperationsResponse]:
        r"""Return a callable for the list_operations method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_operations" not in self._stubs:
            self._stubs["list_operations"] = self.grpc_channel.unary_unary(
                "/google.longrunning.Operations/ListOperations",
                request_serializer=operations_pb2.ListOperationsRequest.SerializeToString,
                response_deserializer=operations_pb2.ListOperationsResponse.FromString,
            )
        return self._stubs["list_operations"]

    @property
    def list_locations(
        self,
    ) -> Callable[[locations_pb2.ListLocationsRequest], locations_pb2.ListLocationsResponse]:
        r"""Return a callable for the list locations method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "list_locations" not in self._stubs:
            self._stubs["list_locations"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/ListLocations",
                request_serializer=locations_pb2.ListLocationsRequest.SerializeToString,
                response_deserializer=locations_pb2.ListLocationsResponse.FromString,
            )
        return self._stubs["list_locations"]

    @property
    def get_location(
        self,
    ) -> Callable[[locations_pb2.GetLocationRequest], locations_pb2.Location]:
        r"""Return a callable for the list locations method over gRPC.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_location" not in self._stubs:
            self._stubs["get_location"] = self.grpc_channel.unary_unary(
                "/google.cloud.location.Locations/GetLocation",
                request_serializer=locations_pb2.GetLocationRequest.SerializeToString,
                response_deserializer=locations_pb2.Location.FromString,
            )
        return self._stubs["get_location"]

    @property
    def set_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.SetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the set iam policy method over gRPC.
        Sets the IAM access control policy on the specified
        function. Replaces any existing policy.
        Returns:
            Callable[[~.SetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "set_iam_policy" not in self._stubs:
            self._stubs["set_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/SetIamPolicy",
                request_serializer=iam_policy_pb2.SetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["set_iam_policy"]

    @property
    def get_iam_policy(
        self,
    ) -> Callable[[iam_policy_pb2.GetIamPolicyRequest], policy_pb2.Policy]:
        r"""Return a callable for the get iam policy method over gRPC.
        Gets the IAM access control policy for a function.
        Returns an empty policy if the function exists and does
        not have a policy set.
        Returns:
            Callable[[~.GetIamPolicyRequest],
                    ~.Policy]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "get_iam_policy" not in self._stubs:
            self._stubs["get_iam_policy"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/GetIamPolicy",
                request_serializer=iam_policy_pb2.GetIamPolicyRequest.SerializeToString,
                response_deserializer=policy_pb2.Policy.FromString,
            )
        return self._stubs["get_iam_policy"]

    @property
    def test_iam_permissions(
        self,
    ) -> Callable[
        [iam_policy_pb2.TestIamPermissionsRequest], iam_policy_pb2.TestIamPermissionsResponse
    ]:
        r"""Return a callable for the test iam permissions method over gRPC.
        Tests the specified permissions against the IAM access control
        policy for a function. If the function does not exist, this will
        return an empty set of permissions, not a NOT_FOUND error.
        Returns:
            Callable[[~.TestIamPermissionsRequest],
                    ~.TestIamPermissionsResponse]:
                A function that, when called, will call the underlying RPC
                on the server.
        """
        # Generate a "stub function" on-the-fly which will actually make
        # the request.
        # gRPC handles serialization and deserialization, so we just need
        # to pass in the functions for each.
        if "test_iam_permissions" not in self._stubs:
            self._stubs["test_iam_permissions"] = self.grpc_channel.unary_unary(
                "/google.iam.v1.IAMPolicy/TestIamPermissions",
                request_serializer=iam_policy_pb2.TestIamPermissionsRequest.SerializeToString,
                response_deserializer=iam_policy_pb2.TestIamPermissionsResponse.FromString,
            )
        return self._stubs["test_iam_permissions"]

    @property
    def kind(self) -> str:
        return "grpc"


__all__ = (
    'BackupForGKEGrpcTransport',
)
