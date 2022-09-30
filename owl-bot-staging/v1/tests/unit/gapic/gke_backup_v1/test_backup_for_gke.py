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
import os
# try/except added for compatibility with python < 3.8
try:
    from unittest import mock
    from unittest.mock import AsyncMock  # pragma: NO COVER
except ImportError:  # pragma: NO COVER
    import mock

import grpc
from grpc.experimental import aio
from collections.abc import Iterable
from google.protobuf import json_format
import json
import math
import pytest
from proto.marshal.rules.dates import DurationRule, TimestampRule
from proto.marshal.rules import wrappers
from requests import Response
from requests import Request, PreparedRequest
from requests.sessions import Session
from google.protobuf import json_format

from google.api_core import client_options
from google.api_core import exceptions as core_exceptions
from google.api_core import future
from google.api_core import gapic_v1
from google.api_core import grpc_helpers
from google.api_core import grpc_helpers_async
from google.api_core import operation
from google.api_core import operation_async  # type: ignore
from google.api_core import operations_v1
from google.api_core import path_template
from google.auth import credentials as ga_credentials
from google.auth.exceptions import MutualTLSChannelError
from google.cloud.gke_backup_v1.services.backup_for_gke import BackupForGKEAsyncClient
from google.cloud.gke_backup_v1.services.backup_for_gke import BackupForGKEClient
from google.cloud.gke_backup_v1.services.backup_for_gke import pagers
from google.cloud.gke_backup_v1.services.backup_for_gke import transports
from google.cloud.gke_backup_v1.types import backup
from google.cloud.gke_backup_v1.types import backup as gcg_backup
from google.cloud.gke_backup_v1.types import backup_plan
from google.cloud.gke_backup_v1.types import backup_plan as gcg_backup_plan
from google.cloud.gke_backup_v1.types import common
from google.cloud.gke_backup_v1.types import gkebackup
from google.cloud.gke_backup_v1.types import restore
from google.cloud.gke_backup_v1.types import restore as gcg_restore
from google.cloud.gke_backup_v1.types import restore_plan
from google.cloud.gke_backup_v1.types import restore_plan as gcg_restore_plan
from google.cloud.gke_backup_v1.types import volume
from google.longrunning import operations_pb2
from google.oauth2 import service_account
from google.protobuf import field_mask_pb2  # type: ignore
from google.protobuf import timestamp_pb2  # type: ignore
import google.auth


def client_cert_source_callback():
    return b"cert bytes", b"key bytes"


# If default endpoint is localhost, then default mtls endpoint will be the same.
# This method modifies the default endpoint so the client can produce a different
# mtls endpoint for endpoint testing purposes.
def modify_default_endpoint(client):
    return "foo.googleapis.com" if ("localhost" in client.DEFAULT_ENDPOINT) else client.DEFAULT_ENDPOINT


def test__get_default_mtls_endpoint():
    api_endpoint = "example.googleapis.com"
    api_mtls_endpoint = "example.mtls.googleapis.com"
    sandbox_endpoint = "example.sandbox.googleapis.com"
    sandbox_mtls_endpoint = "example.mtls.sandbox.googleapis.com"
    non_googleapi = "api.example.com"

    assert BackupForGKEClient._get_default_mtls_endpoint(None) is None
    assert BackupForGKEClient._get_default_mtls_endpoint(api_endpoint) == api_mtls_endpoint
    assert BackupForGKEClient._get_default_mtls_endpoint(api_mtls_endpoint) == api_mtls_endpoint
    assert BackupForGKEClient._get_default_mtls_endpoint(sandbox_endpoint) == sandbox_mtls_endpoint
    assert BackupForGKEClient._get_default_mtls_endpoint(sandbox_mtls_endpoint) == sandbox_mtls_endpoint
    assert BackupForGKEClient._get_default_mtls_endpoint(non_googleapi) == non_googleapi


@pytest.mark.parametrize("client_class,transport_name", [
    (BackupForGKEClient, "grpc"),
    (BackupForGKEAsyncClient, "grpc_asyncio"),
    (BackupForGKEClient, "rest"),
])
def test_backup_for_gke_client_from_service_account_info(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_info') as factory:
        factory.return_value = creds
        info = {"valid": True}
        client = client_class.from_service_account_info(info, transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'gkebackup.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://gkebackup.googleapis.com'
        )


@pytest.mark.parametrize("transport_class,transport_name", [
    (transports.BackupForGKEGrpcTransport, "grpc"),
    (transports.BackupForGKEGrpcAsyncIOTransport, "grpc_asyncio"),
    (transports.BackupForGKERestTransport, "rest"),
])
def test_backup_for_gke_client_service_account_always_use_jwt(transport_class, transport_name):
    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=True)
        use_jwt.assert_called_once_with(True)

    with mock.patch.object(service_account.Credentials, 'with_always_use_jwt_access', create=True) as use_jwt:
        creds = service_account.Credentials(None, None, None)
        transport = transport_class(credentials=creds, always_use_jwt_access=False)
        use_jwt.assert_not_called()


@pytest.mark.parametrize("client_class,transport_name", [
    (BackupForGKEClient, "grpc"),
    (BackupForGKEAsyncClient, "grpc_asyncio"),
    (BackupForGKEClient, "rest"),
])
def test_backup_for_gke_client_from_service_account_file(client_class, transport_name):
    creds = ga_credentials.AnonymousCredentials()
    with mock.patch.object(service_account.Credentials, 'from_service_account_file') as factory:
        factory.return_value = creds
        client = client_class.from_service_account_file("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        client = client_class.from_service_account_json("dummy/file/path.json", transport=transport_name)
        assert client.transport._credentials == creds
        assert isinstance(client, client_class)

        assert client.transport._host == (
            'gkebackup.googleapis.com:443'
            if transport_name in ['grpc', 'grpc_asyncio']
            else
            'https://gkebackup.googleapis.com'
        )


def test_backup_for_gke_client_get_transport_class():
    transport = BackupForGKEClient.get_transport_class()
    available_transports = [
        transports.BackupForGKEGrpcTransport,
        transports.BackupForGKERestTransport,
    ]
    assert transport in available_transports

    transport = BackupForGKEClient.get_transport_class("grpc")
    assert transport == transports.BackupForGKEGrpcTransport


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (BackupForGKEClient, transports.BackupForGKEGrpcTransport, "grpc"),
    (BackupForGKEAsyncClient, transports.BackupForGKEGrpcAsyncIOTransport, "grpc_asyncio"),
    (BackupForGKEClient, transports.BackupForGKERestTransport, "rest"),
])
@mock.patch.object(BackupForGKEClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BackupForGKEClient))
@mock.patch.object(BackupForGKEAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BackupForGKEAsyncClient))
def test_backup_for_gke_client_client_options(client_class, transport_class, transport_name):
    # Check that if channel is provided we won't create a new one.
    with mock.patch.object(BackupForGKEClient, 'get_transport_class') as gtc:
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials()
        )
        client = client_class(transport=transport)
        gtc.assert_not_called()

    # Check that if channel is provided via str we will create a new one.
    with mock.patch.object(BackupForGKEClient, 'get_transport_class') as gtc:
        client = client_class(transport=transport_name)
        gtc.assert_called()

    # Check the case api_endpoint is provided.
    options = client_options.ClientOptions(api_endpoint="squid.clam.whelk")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(transport=transport_name, client_options=options)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT is
    # "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(transport=transport_name)
            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=client.DEFAULT_MTLS_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case api_endpoint is not provided and GOOGLE_API_USE_MTLS_ENDPOINT has
    # unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "Unsupported"}):
        with pytest.raises(MutualTLSChannelError):
            client = client_class(transport=transport_name)

    # Check the case GOOGLE_API_USE_CLIENT_CERTIFICATE has unsupported value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "Unsupported"}):
        with pytest.raises(ValueError):
            client = client_class(transport=transport_name)

    # Check the case quota_project_id is provided
    options = client_options.ClientOptions(quota_project_id="octopus")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id="octopus",
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )
    # Check the case api_endpoint is provided
    options = client_options.ClientOptions(api_audience="https://language.googleapis.com")
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience="https://language.googleapis.com"
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,use_client_cert_env", [
    (BackupForGKEClient, transports.BackupForGKEGrpcTransport, "grpc", "true"),
    (BackupForGKEAsyncClient, transports.BackupForGKEGrpcAsyncIOTransport, "grpc_asyncio", "true"),
    (BackupForGKEClient, transports.BackupForGKEGrpcTransport, "grpc", "false"),
    (BackupForGKEAsyncClient, transports.BackupForGKEGrpcAsyncIOTransport, "grpc_asyncio", "false"),
    (BackupForGKEClient, transports.BackupForGKERestTransport, "rest", "true"),
    (BackupForGKEClient, transports.BackupForGKERestTransport, "rest", "false"),
])
@mock.patch.object(BackupForGKEClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BackupForGKEClient))
@mock.patch.object(BackupForGKEAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BackupForGKEAsyncClient))
@mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "auto"})
def test_backup_for_gke_client_mtls_env_auto(client_class, transport_class, transport_name, use_client_cert_env):
    # This tests the endpoint autoswitch behavior. Endpoint is autoswitched to the default
    # mtls endpoint, if GOOGLE_API_USE_CLIENT_CERTIFICATE is "true" and client cert exists.

    # Check the case client_cert_source is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        options = client_options.ClientOptions(client_cert_source=client_cert_source_callback)
        with mock.patch.object(transport_class, '__init__') as patched:
            patched.return_value = None
            client = client_class(client_options=options, transport=transport_name)

            if use_client_cert_env == "false":
                expected_client_cert_source = None
                expected_host = client.DEFAULT_ENDPOINT
            else:
                expected_client_cert_source = client_cert_source_callback
                expected_host = client.DEFAULT_MTLS_ENDPOINT

            patched.assert_called_once_with(
                credentials=None,
                credentials_file=None,
                host=expected_host,
                scopes=None,
                client_cert_source_for_mtls=expected_client_cert_source,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )

    # Check the case ADC client cert is provided. Whether client cert is used depends on
    # GOOGLE_API_USE_CLIENT_CERTIFICATE value.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
                with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=client_cert_source_callback):
                    if use_client_cert_env == "false":
                        expected_host = client.DEFAULT_ENDPOINT
                        expected_client_cert_source = None
                    else:
                        expected_host = client.DEFAULT_MTLS_ENDPOINT
                        expected_client_cert_source = client_cert_source_callback

                    patched.return_value = None
                    client = client_class(transport=transport_name)
                    patched.assert_called_once_with(
                        credentials=None,
                        credentials_file=None,
                        host=expected_host,
                        scopes=None,
                        client_cert_source_for_mtls=expected_client_cert_source,
                        quota_project_id=None,
                        client_info=transports.base.DEFAULT_CLIENT_INFO,
                        always_use_jwt_access=True,
                        api_audience=None,
                    )

    # Check the case client_cert_source and ADC client cert are not provided.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": use_client_cert_env}):
        with mock.patch.object(transport_class, '__init__') as patched:
            with mock.patch("google.auth.transport.mtls.has_default_client_cert_source", return_value=False):
                patched.return_value = None
                client = client_class(transport=transport_name)
                patched.assert_called_once_with(
                    credentials=None,
                    credentials_file=None,
                    host=client.DEFAULT_ENDPOINT,
                    scopes=None,
                    client_cert_source_for_mtls=None,
                    quota_project_id=None,
                    client_info=transports.base.DEFAULT_CLIENT_INFO,
                    always_use_jwt_access=True,
                    api_audience=None,
                )


@pytest.mark.parametrize("client_class", [
    BackupForGKEClient, BackupForGKEAsyncClient
])
@mock.patch.object(BackupForGKEClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BackupForGKEClient))
@mock.patch.object(BackupForGKEAsyncClient, "DEFAULT_ENDPOINT", modify_default_endpoint(BackupForGKEAsyncClient))
def test_backup_for_gke_client_get_mtls_endpoint_and_cert_source(client_class):
    mock_client_cert_source = mock.Mock()

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "true".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source == mock_client_cert_source

    # Test the case GOOGLE_API_USE_CLIENT_CERTIFICATE is "false".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "false"}):
        mock_client_cert_source = mock.Mock()
        mock_api_endpoint = "foo"
        options = client_options.ClientOptions(client_cert_source=mock_client_cert_source, api_endpoint=mock_api_endpoint)
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source(options)
        assert api_endpoint == mock_api_endpoint
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "never".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "never"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "always".
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_MTLS_ENDPOINT": "always"}):
        api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
        assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
        assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert doesn't exist.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=False):
            api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
            assert api_endpoint == client_class.DEFAULT_ENDPOINT
            assert cert_source is None

    # Test the case GOOGLE_API_USE_MTLS_ENDPOINT is "auto" and default cert exists.
    with mock.patch.dict(os.environ, {"GOOGLE_API_USE_CLIENT_CERTIFICATE": "true"}):
        with mock.patch('google.auth.transport.mtls.has_default_client_cert_source', return_value=True):
            with mock.patch('google.auth.transport.mtls.default_client_cert_source', return_value=mock_client_cert_source):
                api_endpoint, cert_source = client_class.get_mtls_endpoint_and_cert_source()
                assert api_endpoint == client_class.DEFAULT_MTLS_ENDPOINT
                assert cert_source == mock_client_cert_source


@pytest.mark.parametrize("client_class,transport_class,transport_name", [
    (BackupForGKEClient, transports.BackupForGKEGrpcTransport, "grpc"),
    (BackupForGKEAsyncClient, transports.BackupForGKEGrpcAsyncIOTransport, "grpc_asyncio"),
    (BackupForGKEClient, transports.BackupForGKERestTransport, "rest"),
])
def test_backup_for_gke_client_client_options_scopes(client_class, transport_class, transport_name):
    # Check the case scopes are provided.
    options = client_options.ClientOptions(
        scopes=["1", "2"],
    )
    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host=client.DEFAULT_ENDPOINT,
            scopes=["1", "2"],
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (BackupForGKEClient, transports.BackupForGKEGrpcTransport, "grpc", grpc_helpers),
    (BackupForGKEAsyncClient, transports.BackupForGKEGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
    (BackupForGKEClient, transports.BackupForGKERestTransport, "rest", None),
])
def test_backup_for_gke_client_client_options_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

def test_backup_for_gke_client_client_options_from_dict():
    with mock.patch('google.cloud.gke_backup_v1.services.backup_for_gke.transports.BackupForGKEGrpcTransport.__init__') as grpc_transport:
        grpc_transport.return_value = None
        client = BackupForGKEClient(
            client_options={'api_endpoint': 'squid.clam.whelk'}
        )
        grpc_transport.assert_called_once_with(
            credentials=None,
            credentials_file=None,
            host="squid.clam.whelk",
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )


@pytest.mark.parametrize("client_class,transport_class,transport_name,grpc_helpers", [
    (BackupForGKEClient, transports.BackupForGKEGrpcTransport, "grpc", grpc_helpers),
    (BackupForGKEAsyncClient, transports.BackupForGKEGrpcAsyncIOTransport, "grpc_asyncio", grpc_helpers_async),
])
def test_backup_for_gke_client_create_channel_credentials_file(client_class, transport_class, transport_name, grpc_helpers):
    # Check the case credentials file is provided.
    options = client_options.ClientOptions(
        credentials_file="credentials.json"
    )

    with mock.patch.object(transport_class, '__init__') as patched:
        patched.return_value = None
        client = client_class(client_options=options, transport=transport_name)
        patched.assert_called_once_with(
            credentials=None,
            credentials_file="credentials.json",
            host=client.DEFAULT_ENDPOINT,
            scopes=None,
            client_cert_source_for_mtls=None,
            quota_project_id=None,
            client_info=transports.base.DEFAULT_CLIENT_INFO,
            always_use_jwt_access=True,
            api_audience=None,
        )

    # test that the credentials from file are saved and used as the credentials.
    with mock.patch.object(
        google.auth, "load_credentials_from_file", autospec=True
    ) as load_creds, mock.patch.object(
        google.auth, "default", autospec=True
    ) as adc, mock.patch.object(
        grpc_helpers, "create_channel"
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        file_creds = ga_credentials.AnonymousCredentials()
        load_creds.return_value = (file_creds, None)
        adc.return_value = (creds, None)
        client = client_class(client_options=options, transport=transport_name)
        create_channel.assert_called_with(
            "gkebackup.googleapis.com:443",
            credentials=file_creds,
            credentials_file=None,
            quota_project_id=None,
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=None,
            default_host="gkebackup.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.CreateBackupPlanRequest,
  dict,
])
def test_create_backup_plan(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateBackupPlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_backup_plan_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup_plan),
            '__call__') as call:
        client.create_backup_plan()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateBackupPlanRequest()

@pytest.mark.asyncio
async def test_create_backup_plan_async(transport: str = 'grpc_asyncio', request_type=gkebackup.CreateBackupPlanRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateBackupPlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_backup_plan_async_from_dict():
    await test_create_backup_plan_async(request_type=dict)


def test_create_backup_plan_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.CreateBackupPlanRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup_plan),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_backup_plan_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.CreateBackupPlanRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup_plan),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_backup_plan_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_backup_plan(
            parent='parent_value',
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            backup_plan_id='backup_plan_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].backup_plan
        mock_val = gcg_backup_plan.BackupPlan(name='name_value')
        assert arg == mock_val
        arg = args[0].backup_plan_id
        mock_val = 'backup_plan_id_value'
        assert arg == mock_val


def test_create_backup_plan_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_backup_plan(
            gkebackup.CreateBackupPlanRequest(),
            parent='parent_value',
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            backup_plan_id='backup_plan_id_value',
        )

@pytest.mark.asyncio
async def test_create_backup_plan_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_backup_plan(
            parent='parent_value',
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            backup_plan_id='backup_plan_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].backup_plan
        mock_val = gcg_backup_plan.BackupPlan(name='name_value')
        assert arg == mock_val
        arg = args[0].backup_plan_id
        mock_val = 'backup_plan_id_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_backup_plan_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_backup_plan(
            gkebackup.CreateBackupPlanRequest(),
            parent='parent_value',
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            backup_plan_id='backup_plan_id_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.ListBackupPlansRequest,
  dict,
])
def test_list_backup_plans(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListBackupPlansResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_backup_plans(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListBackupPlansRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupPlansPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_backup_plans_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__') as call:
        client.list_backup_plans()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListBackupPlansRequest()

@pytest.mark.asyncio
async def test_list_backup_plans_async(transport: str = 'grpc_asyncio', request_type=gkebackup.ListBackupPlansRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListBackupPlansResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_backup_plans(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListBackupPlansRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupPlansAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_backup_plans_async_from_dict():
    await test_list_backup_plans_async(request_type=dict)


def test_list_backup_plans_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListBackupPlansRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__') as call:
        call.return_value = gkebackup.ListBackupPlansResponse()
        client.list_backup_plans(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_backup_plans_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListBackupPlansRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListBackupPlansResponse())
        await client.list_backup_plans(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_backup_plans_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListBackupPlansResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_backup_plans(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_backup_plans_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_backup_plans(
            gkebackup.ListBackupPlansRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_backup_plans_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListBackupPlansResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListBackupPlansResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_backup_plans(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_backup_plans_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_backup_plans(
            gkebackup.ListBackupPlansRequest(),
            parent='parent_value',
        )


def test_list_backup_plans_pager(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[],
                next_page_token='def',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_backup_plans(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, backup_plan.BackupPlan)
                   for i in results)
def test_list_backup_plans_pages(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[],
                next_page_token='def',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_backup_plans(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_backup_plans_async_pager():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[],
                next_page_token='def',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_backup_plans(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, backup_plan.BackupPlan)
                for i in responses)


@pytest.mark.asyncio
async def test_list_backup_plans_async_pages():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backup_plans),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[],
                next_page_token='def',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_backup_plans(request={})).pages: # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  gkebackup.GetBackupPlanRequest,
  dict,
])
def test_get_backup_plan(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = backup_plan.BackupPlan(
            name='name_value',
            uid='uid_value',
            description='description_value',
            cluster='cluster_value',
            etag='etag_value',
            deactivated=True,
            protected_pod_count=2036,
        )
        response = client.get_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetBackupPlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, backup_plan.BackupPlan)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.description == 'description_value'
    assert response.cluster == 'cluster_value'
    assert response.etag == 'etag_value'
    assert response.deactivated is True
    assert response.protected_pod_count == 2036


def test_get_backup_plan_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup_plan),
            '__call__') as call:
        client.get_backup_plan()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetBackupPlanRequest()

@pytest.mark.asyncio
async def test_get_backup_plan_async(transport: str = 'grpc_asyncio', request_type=gkebackup.GetBackupPlanRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(backup_plan.BackupPlan(
            name='name_value',
            uid='uid_value',
            description='description_value',
            cluster='cluster_value',
            etag='etag_value',
            deactivated=True,
            protected_pod_count=2036,
        ))
        response = await client.get_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetBackupPlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, backup_plan.BackupPlan)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.description == 'description_value'
    assert response.cluster == 'cluster_value'
    assert response.etag == 'etag_value'
    assert response.deactivated is True
    assert response.protected_pod_count == 2036


@pytest.mark.asyncio
async def test_get_backup_plan_async_from_dict():
    await test_get_backup_plan_async(request_type=dict)


def test_get_backup_plan_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetBackupPlanRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup_plan),
            '__call__') as call:
        call.return_value = backup_plan.BackupPlan()
        client.get_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_backup_plan_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetBackupPlanRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup_plan),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(backup_plan.BackupPlan())
        await client.get_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_backup_plan_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = backup_plan.BackupPlan()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_backup_plan(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_backup_plan_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_backup_plan(
            gkebackup.GetBackupPlanRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_backup_plan_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = backup_plan.BackupPlan()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(backup_plan.BackupPlan())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_backup_plan(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_backup_plan_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_backup_plan(
            gkebackup.GetBackupPlanRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.UpdateBackupPlanRequest,
  dict,
])
def test_update_backup_plan(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateBackupPlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_backup_plan_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup_plan),
            '__call__') as call:
        client.update_backup_plan()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateBackupPlanRequest()

@pytest.mark.asyncio
async def test_update_backup_plan_async(transport: str = 'grpc_asyncio', request_type=gkebackup.UpdateBackupPlanRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateBackupPlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_backup_plan_async_from_dict():
    await test_update_backup_plan_async(request_type=dict)


def test_update_backup_plan_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.UpdateBackupPlanRequest()

    request.backup_plan.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup_plan),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'backup_plan.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_backup_plan_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.UpdateBackupPlanRequest()

    request.backup_plan.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup_plan),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'backup_plan.name=name_value',
    ) in kw['metadata']


def test_update_backup_plan_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_backup_plan(
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].backup_plan
        mock_val = gcg_backup_plan.BackupPlan(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_backup_plan_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_backup_plan(
            gkebackup.UpdateBackupPlanRequest(),
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_backup_plan_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_backup_plan(
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].backup_plan
        mock_val = gcg_backup_plan.BackupPlan(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_backup_plan_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_backup_plan(
            gkebackup.UpdateBackupPlanRequest(),
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.DeleteBackupPlanRequest,
  dict,
])
def test_delete_backup_plan(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteBackupPlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_backup_plan_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup_plan),
            '__call__') as call:
        client.delete_backup_plan()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteBackupPlanRequest()

@pytest.mark.asyncio
async def test_delete_backup_plan_async(transport: str = 'grpc_asyncio', request_type=gkebackup.DeleteBackupPlanRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteBackupPlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_backup_plan_async_from_dict():
    await test_delete_backup_plan_async(request_type=dict)


def test_delete_backup_plan_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.DeleteBackupPlanRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup_plan),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_backup_plan_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.DeleteBackupPlanRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup_plan),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_backup_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_backup_plan_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_backup_plan(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_backup_plan_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_backup_plan(
            gkebackup.DeleteBackupPlanRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_backup_plan_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_backup_plan(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_backup_plan_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_backup_plan(
            gkebackup.DeleteBackupPlanRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.CreateBackupRequest,
  dict,
])
def test_create_backup(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup),
            '__call__') as call:
        client.create_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateBackupRequest()

@pytest.mark.asyncio
async def test_create_backup_async(transport: str = 'grpc_asyncio', request_type=gkebackup.CreateBackupRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_backup_async_from_dict():
    await test_create_backup_async(request_type=dict)


def test_create_backup_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.CreateBackupRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_backup_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.CreateBackupRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_backup_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_backup(
            parent='parent_value',
            backup=gcg_backup.Backup(name='name_value'),
            backup_id='backup_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].backup
        mock_val = gcg_backup.Backup(name='name_value')
        assert arg == mock_val
        arg = args[0].backup_id
        mock_val = 'backup_id_value'
        assert arg == mock_val


def test_create_backup_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_backup(
            gkebackup.CreateBackupRequest(),
            parent='parent_value',
            backup=gcg_backup.Backup(name='name_value'),
            backup_id='backup_id_value',
        )

@pytest.mark.asyncio
async def test_create_backup_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_backup(
            parent='parent_value',
            backup=gcg_backup.Backup(name='name_value'),
            backup_id='backup_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].backup
        mock_val = gcg_backup.Backup(name='name_value')
        assert arg == mock_val
        arg = args[0].backup_id
        mock_val = 'backup_id_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_backup_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_backup(
            gkebackup.CreateBackupRequest(),
            parent='parent_value',
            backup=gcg_backup.Backup(name='name_value'),
            backup_id='backup_id_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.ListBackupsRequest,
  dict,
])
def test_list_backups(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListBackupsResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListBackupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_backups_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__') as call:
        client.list_backups()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListBackupsRequest()

@pytest.mark.asyncio
async def test_list_backups_async(transport: str = 'grpc_asyncio', request_type=gkebackup.ListBackupsRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListBackupsResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListBackupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_backups_async_from_dict():
    await test_list_backups_async(request_type=dict)


def test_list_backups_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListBackupsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__') as call:
        call.return_value = gkebackup.ListBackupsResponse()
        client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_backups_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListBackupsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListBackupsResponse())
        await client.list_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_backups_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListBackupsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_backups(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_backups_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_backups(
            gkebackup.ListBackupsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_backups_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListBackupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListBackupsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_backups(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_backups_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_backups(
            gkebackup.ListBackupsRequest(),
            parent='parent_value',
        )


def test_list_backups_pager(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                    backup.Backup(),
                    backup.Backup(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListBackupsResponse(
                backups=[],
                next_page_token='def',
            ),
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                    backup.Backup(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_backups(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, backup.Backup)
                   for i in results)
def test_list_backups_pages(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                    backup.Backup(),
                    backup.Backup(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListBackupsResponse(
                backups=[],
                next_page_token='def',
            ),
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                    backup.Backup(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_backups(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_backups_async_pager():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                    backup.Backup(),
                    backup.Backup(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListBackupsResponse(
                backups=[],
                next_page_token='def',
            ),
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                    backup.Backup(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_backups(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, backup.Backup)
                for i in responses)


@pytest.mark.asyncio
async def test_list_backups_async_pages():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_backups),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                    backup.Backup(),
                    backup.Backup(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListBackupsResponse(
                backups=[],
                next_page_token='def',
            ),
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                    backup.Backup(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_backups(request={})).pages: # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  gkebackup.GetBackupRequest,
  dict,
])
def test_get_backup(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = backup.Backup(
            name='name_value',
            uid='uid_value',
            manual=True,
            delete_lock_days=1675,
            retain_days=1171,
            contains_volume_data=True,
            contains_secrets=True,
            state=backup.Backup.State.CREATING,
            state_reason='state_reason_value',
            resource_count=1520,
            volume_count=1312,
            size_bytes=1089,
            etag='etag_value',
            description='description_value',
            pod_count=971,
            config_backup_size_bytes=2539,
            all_namespaces=True,
        )
        response = client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, backup.Backup)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.manual is True
    assert response.delete_lock_days == 1675
    assert response.retain_days == 1171
    assert response.contains_volume_data is True
    assert response.contains_secrets is True
    assert response.state == backup.Backup.State.CREATING
    assert response.state_reason == 'state_reason_value'
    assert response.resource_count == 1520
    assert response.volume_count == 1312
    assert response.size_bytes == 1089
    assert response.etag == 'etag_value'
    assert response.description == 'description_value'
    assert response.pod_count == 971
    assert response.config_backup_size_bytes == 2539


def test_get_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup),
            '__call__') as call:
        client.get_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetBackupRequest()

@pytest.mark.asyncio
async def test_get_backup_async(transport: str = 'grpc_asyncio', request_type=gkebackup.GetBackupRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(backup.Backup(
            name='name_value',
            uid='uid_value',
            manual=True,
            delete_lock_days=1675,
            retain_days=1171,
            contains_volume_data=True,
            contains_secrets=True,
            state=backup.Backup.State.CREATING,
            state_reason='state_reason_value',
            resource_count=1520,
            volume_count=1312,
            size_bytes=1089,
            etag='etag_value',
            description='description_value',
            pod_count=971,
            config_backup_size_bytes=2539,
        ))
        response = await client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, backup.Backup)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.manual is True
    assert response.delete_lock_days == 1675
    assert response.retain_days == 1171
    assert response.contains_volume_data is True
    assert response.contains_secrets is True
    assert response.state == backup.Backup.State.CREATING
    assert response.state_reason == 'state_reason_value'
    assert response.resource_count == 1520
    assert response.volume_count == 1312
    assert response.size_bytes == 1089
    assert response.etag == 'etag_value'
    assert response.description == 'description_value'
    assert response.pod_count == 971
    assert response.config_backup_size_bytes == 2539


@pytest.mark.asyncio
async def test_get_backup_async_from_dict():
    await test_get_backup_async(request_type=dict)


def test_get_backup_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetBackupRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup),
            '__call__') as call:
        call.return_value = backup.Backup()
        client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_backup_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetBackupRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(backup.Backup())
        await client.get_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_backup_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = backup.Backup()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_backup(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_backup_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_backup(
            gkebackup.GetBackupRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_backup_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = backup.Backup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(backup.Backup())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_backup(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_backup_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_backup(
            gkebackup.GetBackupRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.UpdateBackupRequest,
  dict,
])
def test_update_backup(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup),
            '__call__') as call:
        client.update_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateBackupRequest()

@pytest.mark.asyncio
async def test_update_backup_async(transport: str = 'grpc_asyncio', request_type=gkebackup.UpdateBackupRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_backup_async_from_dict():
    await test_update_backup_async(request_type=dict)


def test_update_backup_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.UpdateBackupRequest()

    request.backup.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'backup.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_backup_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.UpdateBackupRequest()

    request.backup.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'backup.name=name_value',
    ) in kw['metadata']


def test_update_backup_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_backup(
            backup=gcg_backup.Backup(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].backup
        mock_val = gcg_backup.Backup(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_backup_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_backup(
            gkebackup.UpdateBackupRequest(),
            backup=gcg_backup.Backup(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_backup_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_backup(
            backup=gcg_backup.Backup(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].backup
        mock_val = gcg_backup.Backup(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_backup_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_backup(
            gkebackup.UpdateBackupRequest(),
            backup=gcg_backup.Backup(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.DeleteBackupRequest,
  dict,
])
def test_delete_backup(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup),
            '__call__') as call:
        client.delete_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteBackupRequest()

@pytest.mark.asyncio
async def test_delete_backup_async(transport: str = 'grpc_asyncio', request_type=gkebackup.DeleteBackupRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_backup_async_from_dict():
    await test_delete_backup_async(request_type=dict)


def test_delete_backup_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.DeleteBackupRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_backup_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.DeleteBackupRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_backup_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_backup(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_backup_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_backup(
            gkebackup.DeleteBackupRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_backup_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_backup(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_backup_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_backup(
            gkebackup.DeleteBackupRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.ListVolumeBackupsRequest,
  dict,
])
def test_list_volume_backups(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListVolumeBackupsResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_volume_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListVolumeBackupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVolumeBackupsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_volume_backups_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__') as call:
        client.list_volume_backups()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListVolumeBackupsRequest()

@pytest.mark.asyncio
async def test_list_volume_backups_async(transport: str = 'grpc_asyncio', request_type=gkebackup.ListVolumeBackupsRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListVolumeBackupsResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_volume_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListVolumeBackupsRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVolumeBackupsAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_volume_backups_async_from_dict():
    await test_list_volume_backups_async(request_type=dict)


def test_list_volume_backups_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListVolumeBackupsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__') as call:
        call.return_value = gkebackup.ListVolumeBackupsResponse()
        client.list_volume_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_volume_backups_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListVolumeBackupsRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListVolumeBackupsResponse())
        await client.list_volume_backups(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_volume_backups_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListVolumeBackupsResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_volume_backups(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_volume_backups_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_volume_backups(
            gkebackup.ListVolumeBackupsRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_volume_backups_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListVolumeBackupsResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListVolumeBackupsResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_volume_backups(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_volume_backups_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_volume_backups(
            gkebackup.ListVolumeBackupsRequest(),
            parent='parent_value',
        )


def test_list_volume_backups_pager(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[],
                next_page_token='def',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_volume_backups(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, volume.VolumeBackup)
                   for i in results)
def test_list_volume_backups_pages(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[],
                next_page_token='def',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_volume_backups(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_volume_backups_async_pager():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[],
                next_page_token='def',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_volume_backups(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, volume.VolumeBackup)
                for i in responses)


@pytest.mark.asyncio
async def test_list_volume_backups_async_pages():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_backups),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[],
                next_page_token='def',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_volume_backups(request={})).pages: # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  gkebackup.GetVolumeBackupRequest,
  dict,
])
def test_get_volume_backup(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.VolumeBackup(
            name='name_value',
            uid='uid_value',
            volume_backup_handle='volume_backup_handle_value',
            format_=volume.VolumeBackup.VolumeBackupFormat.GCE_PERSISTENT_DISK,
            storage_bytes=1403,
            disk_size_bytes=1611,
            state=volume.VolumeBackup.State.CREATING,
            state_message='state_message_value',
            etag='etag_value',
        )
        response = client.get_volume_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetVolumeBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, volume.VolumeBackup)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.volume_backup_handle == 'volume_backup_handle_value'
    assert response.format_ == volume.VolumeBackup.VolumeBackupFormat.GCE_PERSISTENT_DISK
    assert response.storage_bytes == 1403
    assert response.disk_size_bytes == 1611
    assert response.state == volume.VolumeBackup.State.CREATING
    assert response.state_message == 'state_message_value'
    assert response.etag == 'etag_value'


def test_get_volume_backup_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_backup),
            '__call__') as call:
        client.get_volume_backup()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetVolumeBackupRequest()

@pytest.mark.asyncio
async def test_get_volume_backup_async(transport: str = 'grpc_asyncio', request_type=gkebackup.GetVolumeBackupRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(volume.VolumeBackup(
            name='name_value',
            uid='uid_value',
            volume_backup_handle='volume_backup_handle_value',
            format_=volume.VolumeBackup.VolumeBackupFormat.GCE_PERSISTENT_DISK,
            storage_bytes=1403,
            disk_size_bytes=1611,
            state=volume.VolumeBackup.State.CREATING,
            state_message='state_message_value',
            etag='etag_value',
        ))
        response = await client.get_volume_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetVolumeBackupRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, volume.VolumeBackup)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.volume_backup_handle == 'volume_backup_handle_value'
    assert response.format_ == volume.VolumeBackup.VolumeBackupFormat.GCE_PERSISTENT_DISK
    assert response.storage_bytes == 1403
    assert response.disk_size_bytes == 1611
    assert response.state == volume.VolumeBackup.State.CREATING
    assert response.state_message == 'state_message_value'
    assert response.etag == 'etag_value'


@pytest.mark.asyncio
async def test_get_volume_backup_async_from_dict():
    await test_get_volume_backup_async(request_type=dict)


def test_get_volume_backup_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetVolumeBackupRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_backup),
            '__call__') as call:
        call.return_value = volume.VolumeBackup()
        client.get_volume_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_volume_backup_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetVolumeBackupRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_backup),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(volume.VolumeBackup())
        await client.get_volume_backup(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_volume_backup_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.VolumeBackup()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_volume_backup(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_volume_backup_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_volume_backup(
            gkebackup.GetVolumeBackupRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_volume_backup_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_backup),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.VolumeBackup()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(volume.VolumeBackup())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_volume_backup(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_volume_backup_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_volume_backup(
            gkebackup.GetVolumeBackupRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.CreateRestorePlanRequest,
  dict,
])
def test_create_restore_plan(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateRestorePlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_restore_plan_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore_plan),
            '__call__') as call:
        client.create_restore_plan()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateRestorePlanRequest()

@pytest.mark.asyncio
async def test_create_restore_plan_async(transport: str = 'grpc_asyncio', request_type=gkebackup.CreateRestorePlanRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateRestorePlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_restore_plan_async_from_dict():
    await test_create_restore_plan_async(request_type=dict)


def test_create_restore_plan_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.CreateRestorePlanRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore_plan),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_restore_plan_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.CreateRestorePlanRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore_plan),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_restore_plan_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_restore_plan(
            parent='parent_value',
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            restore_plan_id='restore_plan_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].restore_plan
        mock_val = gcg_restore_plan.RestorePlan(name='name_value')
        assert arg == mock_val
        arg = args[0].restore_plan_id
        mock_val = 'restore_plan_id_value'
        assert arg == mock_val


def test_create_restore_plan_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_restore_plan(
            gkebackup.CreateRestorePlanRequest(),
            parent='parent_value',
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            restore_plan_id='restore_plan_id_value',
        )

@pytest.mark.asyncio
async def test_create_restore_plan_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_restore_plan(
            parent='parent_value',
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            restore_plan_id='restore_plan_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].restore_plan
        mock_val = gcg_restore_plan.RestorePlan(name='name_value')
        assert arg == mock_val
        arg = args[0].restore_plan_id
        mock_val = 'restore_plan_id_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_restore_plan_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_restore_plan(
            gkebackup.CreateRestorePlanRequest(),
            parent='parent_value',
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            restore_plan_id='restore_plan_id_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.ListRestorePlansRequest,
  dict,
])
def test_list_restore_plans(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListRestorePlansResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_restore_plans(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListRestorePlansRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRestorePlansPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_restore_plans_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__') as call:
        client.list_restore_plans()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListRestorePlansRequest()

@pytest.mark.asyncio
async def test_list_restore_plans_async(transport: str = 'grpc_asyncio', request_type=gkebackup.ListRestorePlansRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListRestorePlansResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_restore_plans(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListRestorePlansRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRestorePlansAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_restore_plans_async_from_dict():
    await test_list_restore_plans_async(request_type=dict)


def test_list_restore_plans_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListRestorePlansRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__') as call:
        call.return_value = gkebackup.ListRestorePlansResponse()
        client.list_restore_plans(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_restore_plans_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListRestorePlansRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListRestorePlansResponse())
        await client.list_restore_plans(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_restore_plans_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListRestorePlansResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_restore_plans(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_restore_plans_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_restore_plans(
            gkebackup.ListRestorePlansRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_restore_plans_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListRestorePlansResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListRestorePlansResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_restore_plans(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_restore_plans_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_restore_plans(
            gkebackup.ListRestorePlansRequest(),
            parent='parent_value',
        )


def test_list_restore_plans_pager(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[],
                next_page_token='def',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_restore_plans(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, restore_plan.RestorePlan)
                   for i in results)
def test_list_restore_plans_pages(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[],
                next_page_token='def',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_restore_plans(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_restore_plans_async_pager():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[],
                next_page_token='def',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_restore_plans(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, restore_plan.RestorePlan)
                for i in responses)


@pytest.mark.asyncio
async def test_list_restore_plans_async_pages():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restore_plans),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[],
                next_page_token='def',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_restore_plans(request={})).pages: # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  gkebackup.GetRestorePlanRequest,
  dict,
])
def test_get_restore_plan(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = restore_plan.RestorePlan(
            name='name_value',
            uid='uid_value',
            description='description_value',
            backup_plan='backup_plan_value',
            cluster='cluster_value',
            etag='etag_value',
        )
        response = client.get_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetRestorePlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, restore_plan.RestorePlan)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.description == 'description_value'
    assert response.backup_plan == 'backup_plan_value'
    assert response.cluster == 'cluster_value'
    assert response.etag == 'etag_value'


def test_get_restore_plan_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore_plan),
            '__call__') as call:
        client.get_restore_plan()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetRestorePlanRequest()

@pytest.mark.asyncio
async def test_get_restore_plan_async(transport: str = 'grpc_asyncio', request_type=gkebackup.GetRestorePlanRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(restore_plan.RestorePlan(
            name='name_value',
            uid='uid_value',
            description='description_value',
            backup_plan='backup_plan_value',
            cluster='cluster_value',
            etag='etag_value',
        ))
        response = await client.get_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetRestorePlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, restore_plan.RestorePlan)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.description == 'description_value'
    assert response.backup_plan == 'backup_plan_value'
    assert response.cluster == 'cluster_value'
    assert response.etag == 'etag_value'


@pytest.mark.asyncio
async def test_get_restore_plan_async_from_dict():
    await test_get_restore_plan_async(request_type=dict)


def test_get_restore_plan_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetRestorePlanRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore_plan),
            '__call__') as call:
        call.return_value = restore_plan.RestorePlan()
        client.get_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_restore_plan_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetRestorePlanRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore_plan),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(restore_plan.RestorePlan())
        await client.get_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_restore_plan_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = restore_plan.RestorePlan()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_restore_plan(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_restore_plan_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_restore_plan(
            gkebackup.GetRestorePlanRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_restore_plan_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = restore_plan.RestorePlan()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(restore_plan.RestorePlan())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_restore_plan(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_restore_plan_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_restore_plan(
            gkebackup.GetRestorePlanRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.UpdateRestorePlanRequest,
  dict,
])
def test_update_restore_plan(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateRestorePlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_restore_plan_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore_plan),
            '__call__') as call:
        client.update_restore_plan()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateRestorePlanRequest()

@pytest.mark.asyncio
async def test_update_restore_plan_async(transport: str = 'grpc_asyncio', request_type=gkebackup.UpdateRestorePlanRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateRestorePlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_restore_plan_async_from_dict():
    await test_update_restore_plan_async(request_type=dict)


def test_update_restore_plan_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.UpdateRestorePlanRequest()

    request.restore_plan.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore_plan),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'restore_plan.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_restore_plan_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.UpdateRestorePlanRequest()

    request.restore_plan.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore_plan),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'restore_plan.name=name_value',
    ) in kw['metadata']


def test_update_restore_plan_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_restore_plan(
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].restore_plan
        mock_val = gcg_restore_plan.RestorePlan(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_restore_plan_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_restore_plan(
            gkebackup.UpdateRestorePlanRequest(),
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_restore_plan_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_restore_plan(
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].restore_plan
        mock_val = gcg_restore_plan.RestorePlan(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_restore_plan_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_restore_plan(
            gkebackup.UpdateRestorePlanRequest(),
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.DeleteRestorePlanRequest,
  dict,
])
def test_delete_restore_plan(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteRestorePlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_restore_plan_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore_plan),
            '__call__') as call:
        client.delete_restore_plan()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteRestorePlanRequest()

@pytest.mark.asyncio
async def test_delete_restore_plan_async(transport: str = 'grpc_asyncio', request_type=gkebackup.DeleteRestorePlanRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteRestorePlanRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_restore_plan_async_from_dict():
    await test_delete_restore_plan_async(request_type=dict)


def test_delete_restore_plan_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.DeleteRestorePlanRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore_plan),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_restore_plan_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.DeleteRestorePlanRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore_plan),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_restore_plan(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_restore_plan_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_restore_plan(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_restore_plan_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_restore_plan(
            gkebackup.DeleteRestorePlanRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_restore_plan_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore_plan),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_restore_plan(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_restore_plan_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_restore_plan(
            gkebackup.DeleteRestorePlanRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.CreateRestoreRequest,
  dict,
])
def test_create_restore(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.create_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateRestoreRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_create_restore_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore),
            '__call__') as call:
        client.create_restore()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateRestoreRequest()

@pytest.mark.asyncio
async def test_create_restore_async(transport: str = 'grpc_asyncio', request_type=gkebackup.CreateRestoreRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.create_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.CreateRestoreRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_create_restore_async_from_dict():
    await test_create_restore_async(request_type=dict)


def test_create_restore_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.CreateRestoreRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.create_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_create_restore_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.CreateRestoreRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.create_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_create_restore_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.create_restore(
            parent='parent_value',
            restore=gcg_restore.Restore(name='name_value'),
            restore_id='restore_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].restore
        mock_val = gcg_restore.Restore(name='name_value')
        assert arg == mock_val
        arg = args[0].restore_id
        mock_val = 'restore_id_value'
        assert arg == mock_val


def test_create_restore_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_restore(
            gkebackup.CreateRestoreRequest(),
            parent='parent_value',
            restore=gcg_restore.Restore(name='name_value'),
            restore_id='restore_id_value',
        )

@pytest.mark.asyncio
async def test_create_restore_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.create_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.create_restore(
            parent='parent_value',
            restore=gcg_restore.Restore(name='name_value'),
            restore_id='restore_id_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val
        arg = args[0].restore
        mock_val = gcg_restore.Restore(name='name_value')
        assert arg == mock_val
        arg = args[0].restore_id
        mock_val = 'restore_id_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_create_restore_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.create_restore(
            gkebackup.CreateRestoreRequest(),
            parent='parent_value',
            restore=gcg_restore.Restore(name='name_value'),
            restore_id='restore_id_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.ListRestoresRequest,
  dict,
])
def test_list_restores(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListRestoresResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        )
        response = client.list_restores(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListRestoresRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRestoresPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_restores_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__') as call:
        client.list_restores()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListRestoresRequest()

@pytest.mark.asyncio
async def test_list_restores_async(transport: str = 'grpc_asyncio', request_type=gkebackup.ListRestoresRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListRestoresResponse(
            next_page_token='next_page_token_value',
            unreachable=['unreachable_value'],
        ))
        response = await client.list_restores(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListRestoresRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRestoresAsyncPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


@pytest.mark.asyncio
async def test_list_restores_async_from_dict():
    await test_list_restores_async(request_type=dict)


def test_list_restores_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListRestoresRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__') as call:
        call.return_value = gkebackup.ListRestoresResponse()
        client.list_restores(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_restores_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListRestoresRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListRestoresResponse())
        await client.list_restores(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_restores_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListRestoresResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_restores(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_restores_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_restores(
            gkebackup.ListRestoresRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_restores_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListRestoresResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListRestoresResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_restores(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_restores_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_restores(
            gkebackup.ListRestoresRequest(),
            parent='parent_value',
        )


def test_list_restores_pager(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                    restore.Restore(),
                    restore.Restore(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListRestoresResponse(
                restores=[],
                next_page_token='def',
            ),
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                    restore.Restore(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_restores(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, restore.Restore)
                   for i in results)
def test_list_restores_pages(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                    restore.Restore(),
                    restore.Restore(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListRestoresResponse(
                restores=[],
                next_page_token='def',
            ),
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                    restore.Restore(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_restores(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_restores_async_pager():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                    restore.Restore(),
                    restore.Restore(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListRestoresResponse(
                restores=[],
                next_page_token='def',
            ),
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                    restore.Restore(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_restores(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, restore.Restore)
                for i in responses)


@pytest.mark.asyncio
async def test_list_restores_async_pages():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_restores),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                    restore.Restore(),
                    restore.Restore(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListRestoresResponse(
                restores=[],
                next_page_token='def',
            ),
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                    restore.Restore(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_restores(request={})).pages: # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  gkebackup.GetRestoreRequest,
  dict,
])
def test_get_restore(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = restore.Restore(
            name='name_value',
            uid='uid_value',
            description='description_value',
            backup='backup_value',
            cluster='cluster_value',
            state=restore.Restore.State.CREATING,
            state_reason='state_reason_value',
            resources_restored_count=2602,
            resources_excluded_count=2576,
            resources_failed_count=2343,
            volumes_restored_count=2394,
            etag='etag_value',
        )
        response = client.get_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetRestoreRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, restore.Restore)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.description == 'description_value'
    assert response.backup == 'backup_value'
    assert response.cluster == 'cluster_value'
    assert response.state == restore.Restore.State.CREATING
    assert response.state_reason == 'state_reason_value'
    assert response.resources_restored_count == 2602
    assert response.resources_excluded_count == 2576
    assert response.resources_failed_count == 2343
    assert response.volumes_restored_count == 2394
    assert response.etag == 'etag_value'


def test_get_restore_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore),
            '__call__') as call:
        client.get_restore()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetRestoreRequest()

@pytest.mark.asyncio
async def test_get_restore_async(transport: str = 'grpc_asyncio', request_type=gkebackup.GetRestoreRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(restore.Restore(
            name='name_value',
            uid='uid_value',
            description='description_value',
            backup='backup_value',
            cluster='cluster_value',
            state=restore.Restore.State.CREATING,
            state_reason='state_reason_value',
            resources_restored_count=2602,
            resources_excluded_count=2576,
            resources_failed_count=2343,
            volumes_restored_count=2394,
            etag='etag_value',
        ))
        response = await client.get_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetRestoreRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, restore.Restore)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.description == 'description_value'
    assert response.backup == 'backup_value'
    assert response.cluster == 'cluster_value'
    assert response.state == restore.Restore.State.CREATING
    assert response.state_reason == 'state_reason_value'
    assert response.resources_restored_count == 2602
    assert response.resources_excluded_count == 2576
    assert response.resources_failed_count == 2343
    assert response.volumes_restored_count == 2394
    assert response.etag == 'etag_value'


@pytest.mark.asyncio
async def test_get_restore_async_from_dict():
    await test_get_restore_async(request_type=dict)


def test_get_restore_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetRestoreRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore),
            '__call__') as call:
        call.return_value = restore.Restore()
        client.get_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_restore_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetRestoreRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(restore.Restore())
        await client.get_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_restore_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = restore.Restore()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_restore(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_restore_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_restore(
            gkebackup.GetRestoreRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_restore_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = restore.Restore()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(restore.Restore())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_restore(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_restore_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_restore(
            gkebackup.GetRestoreRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.UpdateRestoreRequest,
  dict,
])
def test_update_restore(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.update_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateRestoreRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_update_restore_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore),
            '__call__') as call:
        client.update_restore()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateRestoreRequest()

@pytest.mark.asyncio
async def test_update_restore_async(transport: str = 'grpc_asyncio', request_type=gkebackup.UpdateRestoreRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.update_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.UpdateRestoreRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_update_restore_async_from_dict():
    await test_update_restore_async(request_type=dict)


def test_update_restore_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.UpdateRestoreRequest()

    request.restore.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.update_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'restore.name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_update_restore_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.UpdateRestoreRequest()

    request.restore.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.update_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'restore.name=name_value',
    ) in kw['metadata']


def test_update_restore_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.update_restore(
            restore=gcg_restore.Restore(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].restore
        mock_val = gcg_restore.Restore(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val


def test_update_restore_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_restore(
            gkebackup.UpdateRestoreRequest(),
            restore=gcg_restore.Restore(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

@pytest.mark.asyncio
async def test_update_restore_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.update_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.update_restore(
            restore=gcg_restore.Restore(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].restore
        mock_val = gcg_restore.Restore(name='name_value')
        assert arg == mock_val
        arg = args[0].update_mask
        mock_val = field_mask_pb2.FieldMask(paths=['paths_value'])
        assert arg == mock_val

@pytest.mark.asyncio
async def test_update_restore_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.update_restore(
            gkebackup.UpdateRestoreRequest(),
            restore=gcg_restore.Restore(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.DeleteRestoreRequest,
  dict,
])
def test_delete_restore(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/spam')
        response = client.delete_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteRestoreRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


def test_delete_restore_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore),
            '__call__') as call:
        client.delete_restore()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteRestoreRequest()

@pytest.mark.asyncio
async def test_delete_restore_async(transport: str = 'grpc_asyncio', request_type=gkebackup.DeleteRestoreRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        response = await client.delete_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.DeleteRestoreRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, future.Future)


@pytest.mark.asyncio
async def test_delete_restore_async_from_dict():
    await test_delete_restore_async(request_type=dict)


def test_delete_restore_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.DeleteRestoreRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore),
            '__call__') as call:
        call.return_value = operations_pb2.Operation(name='operations/op')
        client.delete_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_delete_restore_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.DeleteRestoreRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(operations_pb2.Operation(name='operations/op'))
        await client.delete_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_delete_restore_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.delete_restore(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_delete_restore_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_restore(
            gkebackup.DeleteRestoreRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_delete_restore_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.delete_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = operations_pb2.Operation(name='operations/op')

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(
            operations_pb2.Operation(name='operations/spam')
        )
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.delete_restore(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_delete_restore_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.delete_restore(
            gkebackup.DeleteRestoreRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
  gkebackup.ListVolumeRestoresRequest,
  dict,
])
def test_list_volume_restores(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListVolumeRestoresResponse(
            next_page_token='next_page_token_value',
        )
        response = client.list_volume_restores(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListVolumeRestoresRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVolumeRestoresPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_volume_restores_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__') as call:
        client.list_volume_restores()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListVolumeRestoresRequest()

@pytest.mark.asyncio
async def test_list_volume_restores_async(transport: str = 'grpc_asyncio', request_type=gkebackup.ListVolumeRestoresRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListVolumeRestoresResponse(
            next_page_token='next_page_token_value',
        ))
        response = await client.list_volume_restores(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.ListVolumeRestoresRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVolumeRestoresAsyncPager)
    assert response.next_page_token == 'next_page_token_value'


@pytest.mark.asyncio
async def test_list_volume_restores_async_from_dict():
    await test_list_volume_restores_async(request_type=dict)


def test_list_volume_restores_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListVolumeRestoresRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__') as call:
        call.return_value = gkebackup.ListVolumeRestoresResponse()
        client.list_volume_restores(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_list_volume_restores_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.ListVolumeRestoresRequest()

    request.parent = 'parent_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListVolumeRestoresResponse())
        await client.list_volume_restores(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'parent=parent_value',
    ) in kw['metadata']


def test_list_volume_restores_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListVolumeRestoresResponse()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.list_volume_restores(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val


def test_list_volume_restores_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_volume_restores(
            gkebackup.ListVolumeRestoresRequest(),
            parent='parent_value',
        )

@pytest.mark.asyncio
async def test_list_volume_restores_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = gkebackup.ListVolumeRestoresResponse()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(gkebackup.ListVolumeRestoresResponse())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.list_volume_restores(
            parent='parent_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].parent
        mock_val = 'parent_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_list_volume_restores_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.list_volume_restores(
            gkebackup.ListVolumeRestoresRequest(),
            parent='parent_value',
        )


def test_list_volume_restores_pager(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[],
                next_page_token='def',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                ],
            ),
            RuntimeError,
        )

        metadata = ()
        metadata = tuple(metadata) + (
            gapic_v1.routing_header.to_grpc_metadata((
                ('parent', ''),
            )),
        )
        pager = client.list_volume_restores(request={})

        assert pager._metadata == metadata

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, volume.VolumeRestore)
                   for i in results)
def test_list_volume_restores_pages(transport_name: str = "grpc"):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials,
        transport=transport_name,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__') as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[],
                next_page_token='def',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                ],
            ),
            RuntimeError,
        )
        pages = list(client.list_volume_restores(request={}).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.asyncio
async def test_list_volume_restores_async_pager():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[],
                next_page_token='def',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                ],
            ),
            RuntimeError,
        )
        async_pager = await client.list_volume_restores(request={},)
        assert async_pager.next_page_token == 'abc'
        responses = []
        async for response in async_pager: # pragma: no branch
            responses.append(response)

        assert len(responses) == 6
        assert all(isinstance(i, volume.VolumeRestore)
                for i in responses)


@pytest.mark.asyncio
async def test_list_volume_restores_async_pages():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials,
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.list_volume_restores),
            '__call__', new_callable=mock.AsyncMock) as call:
        # Set the response to a series of pages.
        call.side_effect = (
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[],
                next_page_token='def',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                ],
            ),
            RuntimeError,
        )
        pages = []
        async for page_ in (await client.list_volume_restores(request={})).pages: # pragma: no branch
            pages.append(page_)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token

@pytest.mark.parametrize("request_type", [
  gkebackup.GetVolumeRestoreRequest,
  dict,
])
def test_get_volume_restore(request_type, transport: str = 'grpc'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.VolumeRestore(
            name='name_value',
            uid='uid_value',
            volume_backup='volume_backup_value',
            volume_handle='volume_handle_value',
            volume_type=volume.VolumeRestore.VolumeType.GCE_PERSISTENT_DISK,
            state=volume.VolumeRestore.State.CREATING,
            state_message='state_message_value',
            etag='etag_value',
        )
        response = client.get_volume_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetVolumeRestoreRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, volume.VolumeRestore)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.volume_backup == 'volume_backup_value'
    assert response.volume_handle == 'volume_handle_value'
    assert response.volume_type == volume.VolumeRestore.VolumeType.GCE_PERSISTENT_DISK
    assert response.state == volume.VolumeRestore.State.CREATING
    assert response.state_message == 'state_message_value'
    assert response.etag == 'etag_value'


def test_get_volume_restore_empty_call():
    # This test is a coverage failsafe to make sure that totally empty calls,
    # i.e. request == None and no flattened fields passed, work.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_restore),
            '__call__') as call:
        client.get_volume_restore()
        call.assert_called()
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetVolumeRestoreRequest()

@pytest.mark.asyncio
async def test_get_volume_restore_async(transport: str = 'grpc_asyncio', request_type=gkebackup.GetVolumeRestoreRequest):
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Everything is optional in proto3 as far as the runtime is concerned,
    # and we are mocking out the actual API, so just send an empty request.
    request = request_type()

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value =grpc_helpers_async.FakeUnaryUnaryCall(volume.VolumeRestore(
            name='name_value',
            uid='uid_value',
            volume_backup='volume_backup_value',
            volume_handle='volume_handle_value',
            volume_type=volume.VolumeRestore.VolumeType.GCE_PERSISTENT_DISK,
            state=volume.VolumeRestore.State.CREATING,
            state_message='state_message_value',
            etag='etag_value',
        ))
        response = await client.get_volume_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == gkebackup.GetVolumeRestoreRequest()

    # Establish that the response is the type that we expect.
    assert isinstance(response, volume.VolumeRestore)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.volume_backup == 'volume_backup_value'
    assert response.volume_handle == 'volume_handle_value'
    assert response.volume_type == volume.VolumeRestore.VolumeType.GCE_PERSISTENT_DISK
    assert response.state == volume.VolumeRestore.State.CREATING
    assert response.state_message == 'state_message_value'
    assert response.etag == 'etag_value'


@pytest.mark.asyncio
async def test_get_volume_restore_async_from_dict():
    await test_get_volume_restore_async(request_type=dict)


def test_get_volume_restore_field_headers():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetVolumeRestoreRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_restore),
            '__call__') as call:
        call.return_value = volume.VolumeRestore()
        client.get_volume_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


@pytest.mark.asyncio
async def test_get_volume_restore_field_headers_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Any value that is part of the HTTP/1.1 URI should be sent as
    # a field header. Set these to a non-empty value.
    request = gkebackup.GetVolumeRestoreRequest()

    request.name = 'name_value'

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_restore),
            '__call__') as call:
        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(volume.VolumeRestore())
        await client.get_volume_restore(request)

        # Establish that the underlying gRPC stub method was called.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        assert args[0] == request

    # Establish that the field header was sent.
    _, _, kw = call.mock_calls[0]
    assert (
        'x-goog-request-params',
        'name=name_value',
    ) in kw['metadata']


def test_get_volume_restore_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.VolumeRestore()
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        client.get_volume_restore(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls) == 1
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val


def test_get_volume_restore_flattened_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_volume_restore(
            gkebackup.GetVolumeRestoreRequest(),
            name='name_value',
        )

@pytest.mark.asyncio
async def test_get_volume_restore_flattened_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Mock the actual call within the gRPC stub, and fake the request.
    with mock.patch.object(
            type(client.transport.get_volume_restore),
            '__call__') as call:
        # Designate an appropriate return value for the call.
        call.return_value = volume.VolumeRestore()

        call.return_value = grpc_helpers_async.FakeUnaryUnaryCall(volume.VolumeRestore())
        # Call the method with a truthy value for each flattened field,
        # using the keyword arguments to the method.
        response = await client.get_volume_restore(
            name='name_value',
        )

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(call.mock_calls)
        _, args, _ = call.mock_calls[0]
        arg = args[0].name
        mock_val = 'name_value'
        assert arg == mock_val

@pytest.mark.asyncio
async def test_get_volume_restore_flattened_error_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        await client.get_volume_restore(
            gkebackup.GetVolumeRestoreRequest(),
            name='name_value',
        )


@pytest.mark.parametrize("request_type", [
    gkebackup.CreateBackupPlanRequest,
    dict,
])
def test_create_backup_plan_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["backup_plan"] = {'name': 'name_value', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'cluster': 'cluster_value', 'retention_policy': {'backup_delete_lock_days': 2400, 'backup_retain_days': 1896, 'locked': True}, 'labels': {}, 'backup_schedule': {'cron_schedule': 'cron_schedule_value', 'paused': True}, 'etag': 'etag_value', 'deactivated': True, 'backup_config': {'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'include_volume_data': True, 'include_secrets': True, 'encryption_key': {'gcp_kms_encryption_key': 'gcp_kms_encryption_key_value'}}, 'protected_pod_count': 2036}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_backup_plan(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_backup_plan_rest_required_fields(request_type=gkebackup.CreateBackupPlanRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["backup_plan_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "backupPlanId" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_backup_plan._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "backupPlanId" in jsonified_request
    assert jsonified_request["backupPlanId"] == request_init["backup_plan_id"]

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["backupPlanId"] = 'backup_plan_id_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_backup_plan._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("backup_plan_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "backupPlanId" in jsonified_request
    assert jsonified_request["backupPlanId"] == 'backup_plan_id_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_backup_plan(request)

            expected_params = [
                (
                    "backupPlanId",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_backup_plan_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_backup_plan._get_unset_required_fields({})
    assert set(unset_fields) == (set(("backupPlanId", )) & set(("parent", "backupPlan", "backupPlanId", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_backup_plan_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_create_backup_plan") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_create_backup_plan") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.CreateBackupPlanRequest.pb(gkebackup.CreateBackupPlanRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.CreateBackupPlanRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_backup_plan(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_backup_plan_rest_bad_request(transport: str = 'rest', request_type=gkebackup.CreateBackupPlanRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["backup_plan"] = {'name': 'name_value', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'cluster': 'cluster_value', 'retention_policy': {'backup_delete_lock_days': 2400, 'backup_retain_days': 1896, 'locked': True}, 'labels': {}, 'backup_schedule': {'cron_schedule': 'cron_schedule_value', 'paused': True}, 'etag': 'etag_value', 'deactivated': True, 'backup_config': {'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'include_volume_data': True, 'include_secrets': True, 'encryption_key': {'gcp_kms_encryption_key': 'gcp_kms_encryption_key_value'}}, 'protected_pod_count': 2036}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_backup_plan(request)


def test_create_backup_plan_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            backup_plan_id='backup_plan_id_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_backup_plan(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/backupPlans" % client.transport._host, args[1])


def test_create_backup_plan_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_backup_plan(
            gkebackup.CreateBackupPlanRequest(),
            parent='parent_value',
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            backup_plan_id='backup_plan_id_value',
        )


def test_create_backup_plan_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.ListBackupPlansRequest,
    dict,
])
def test_list_backup_plans_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListBackupPlansResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListBackupPlansResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_backup_plans(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupPlansPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_backup_plans_rest_required_fields(request_type=gkebackup.ListBackupPlansRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_backup_plans._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_backup_plans._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gkebackup.ListBackupPlansResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gkebackup.ListBackupPlansResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_backup_plans(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_backup_plans_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_backup_plans._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_backup_plans_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_list_backup_plans") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_list_backup_plans") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.ListBackupPlansRequest.pb(gkebackup.ListBackupPlansRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gkebackup.ListBackupPlansResponse.to_json(gkebackup.ListBackupPlansResponse())

        request = gkebackup.ListBackupPlansRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gkebackup.ListBackupPlansResponse()

        client.list_backup_plans(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_backup_plans_rest_bad_request(transport: str = 'rest', request_type=gkebackup.ListBackupPlansRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_backup_plans(request)


def test_list_backup_plans_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListBackupPlansResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListBackupPlansResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_backup_plans(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/backupPlans" % client.transport._host, args[1])


def test_list_backup_plans_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_backup_plans(
            gkebackup.ListBackupPlansRequest(),
            parent='parent_value',
        )


def test_list_backup_plans_rest_pager(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[],
                next_page_token='def',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListBackupPlansResponse(
                backup_plans=[
                    backup_plan.BackupPlan(),
                    backup_plan.BackupPlan(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(gkebackup.ListBackupPlansResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        pager = client.list_backup_plans(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, backup_plan.BackupPlan)
                for i in results)

        pages = list(client.list_backup_plans(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    gkebackup.GetBackupPlanRequest,
    dict,
])
def test_get_backup_plan_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = backup_plan.BackupPlan(
              name='name_value',
              uid='uid_value',
              description='description_value',
              cluster='cluster_value',
              etag='etag_value',
              deactivated=True,
              protected_pod_count=2036,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = backup_plan.BackupPlan.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_backup_plan(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, backup_plan.BackupPlan)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.description == 'description_value'
    assert response.cluster == 'cluster_value'
    assert response.etag == 'etag_value'
    assert response.deactivated is True
    assert response.protected_pod_count == 2036


def test_get_backup_plan_rest_required_fields(request_type=gkebackup.GetBackupPlanRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_backup_plan._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_backup_plan._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = backup_plan.BackupPlan()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = backup_plan.BackupPlan.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_backup_plan(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_backup_plan_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_backup_plan._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_backup_plan_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_get_backup_plan") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_get_backup_plan") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.GetBackupPlanRequest.pb(gkebackup.GetBackupPlanRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = backup_plan.BackupPlan.to_json(backup_plan.BackupPlan())

        request = gkebackup.GetBackupPlanRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = backup_plan.BackupPlan()

        client.get_backup_plan(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_backup_plan_rest_bad_request(transport: str = 'rest', request_type=gkebackup.GetBackupPlanRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_backup_plan(request)


def test_get_backup_plan_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = backup_plan.BackupPlan()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = backup_plan.BackupPlan.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_backup_plan(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/backupPlans/*}" % client.transport._host, args[1])


def test_get_backup_plan_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_backup_plan(
            gkebackup.GetBackupPlanRequest(),
            name='name_value',
        )


def test_get_backup_plan_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.UpdateBackupPlanRequest,
    dict,
])
def test_update_backup_plan_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'backup_plan': {'name': 'projects/sample1/locations/sample2/backupPlans/sample3'}}
    request_init["backup_plan"] = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'cluster': 'cluster_value', 'retention_policy': {'backup_delete_lock_days': 2400, 'backup_retain_days': 1896, 'locked': True}, 'labels': {}, 'backup_schedule': {'cron_schedule': 'cron_schedule_value', 'paused': True}, 'etag': 'etag_value', 'deactivated': True, 'backup_config': {'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'include_volume_data': True, 'include_secrets': True, 'encryption_key': {'gcp_kms_encryption_key': 'gcp_kms_encryption_key_value'}}, 'protected_pod_count': 2036}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_backup_plan(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_backup_plan_rest_required_fields(request_type=gkebackup.UpdateBackupPlanRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_backup_plan._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_backup_plan._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_backup_plan(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_backup_plan_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_backup_plan._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask", )) & set(("backupPlan", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_backup_plan_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_update_backup_plan") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_update_backup_plan") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.UpdateBackupPlanRequest.pb(gkebackup.UpdateBackupPlanRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.UpdateBackupPlanRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_backup_plan(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_backup_plan_rest_bad_request(transport: str = 'rest', request_type=gkebackup.UpdateBackupPlanRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'backup_plan': {'name': 'projects/sample1/locations/sample2/backupPlans/sample3'}}
    request_init["backup_plan"] = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'cluster': 'cluster_value', 'retention_policy': {'backup_delete_lock_days': 2400, 'backup_retain_days': 1896, 'locked': True}, 'labels': {}, 'backup_schedule': {'cron_schedule': 'cron_schedule_value', 'paused': True}, 'etag': 'etag_value', 'deactivated': True, 'backup_config': {'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'include_volume_data': True, 'include_secrets': True, 'encryption_key': {'gcp_kms_encryption_key': 'gcp_kms_encryption_key_value'}}, 'protected_pod_count': 2036}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_backup_plan(request)


def test_update_backup_plan_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'backup_plan': {'name': 'projects/sample1/locations/sample2/backupPlans/sample3'}}

        # get truthy value for each flattened field
        mock_args = dict(
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_backup_plan(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{backup_plan.name=projects/*/locations/*/backupPlans/*}" % client.transport._host, args[1])


def test_update_backup_plan_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_backup_plan(
            gkebackup.UpdateBackupPlanRequest(),
            backup_plan=gcg_backup_plan.BackupPlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_backup_plan_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.DeleteBackupPlanRequest,
    dict,
])
def test_delete_backup_plan_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_backup_plan(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_backup_plan_rest_required_fields(request_type=gkebackup.DeleteBackupPlanRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_backup_plan._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_backup_plan._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("etag", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_backup_plan(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_backup_plan_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_backup_plan._get_unset_required_fields({})
    assert set(unset_fields) == (set(("etag", )) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_backup_plan_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_delete_backup_plan") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_delete_backup_plan") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.DeleteBackupPlanRequest.pb(gkebackup.DeleteBackupPlanRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.DeleteBackupPlanRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_backup_plan(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_backup_plan_rest_bad_request(transport: str = 'rest', request_type=gkebackup.DeleteBackupPlanRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_backup_plan(request)


def test_delete_backup_plan_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_backup_plan(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/backupPlans/*}" % client.transport._host, args[1])


def test_delete_backup_plan_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_backup_plan(
            gkebackup.DeleteBackupPlanRequest(),
            name='name_value',
        )


def test_delete_backup_plan_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.CreateBackupRequest,
    dict,
])
def test_create_backup_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3'}
    request_init["backup"] = {'name': 'name_value', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'manual': True, 'labels': {}, 'delete_lock_days': 1675, 'delete_lock_expire_time': {}, 'retain_days': 1171, 'retain_expire_time': {}, 'encryption_key': {'gcp_kms_encryption_key': 'gcp_kms_encryption_key_value'}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'contains_volume_data': True, 'contains_secrets': True, 'cluster_metadata': {'cluster': 'cluster_value', 'k8s_version': 'k8s_version_value', 'backup_crd_versions': {}, 'gke_version': 'gke_version_value', 'anthos_version': 'anthos_version_value'}, 'state': 1, 'state_reason': 'state_reason_value', 'complete_time': {}, 'resource_count': 1520, 'volume_count': 1312, 'size_bytes': 1089, 'etag': 'etag_value', 'description': 'description_value', 'pod_count': 971, 'config_backup_size_bytes': 2539}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_backup(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_backup_rest_required_fields(request_type=gkebackup.CreateBackupRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_backup._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("backup_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_backup(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_backup_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_backup._get_unset_required_fields({})
    assert set(unset_fields) == (set(("backupId", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_backup_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_create_backup") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_create_backup") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.CreateBackupRequest.pb(gkebackup.CreateBackupRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.CreateBackupRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_backup(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_backup_rest_bad_request(transport: str = 'rest', request_type=gkebackup.CreateBackupRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3'}
    request_init["backup"] = {'name': 'name_value', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'manual': True, 'labels': {}, 'delete_lock_days': 1675, 'delete_lock_expire_time': {}, 'retain_days': 1171, 'retain_expire_time': {}, 'encryption_key': {'gcp_kms_encryption_key': 'gcp_kms_encryption_key_value'}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'contains_volume_data': True, 'contains_secrets': True, 'cluster_metadata': {'cluster': 'cluster_value', 'k8s_version': 'k8s_version_value', 'backup_crd_versions': {}, 'gke_version': 'gke_version_value', 'anthos_version': 'anthos_version_value'}, 'state': 1, 'state_reason': 'state_reason_value', 'complete_time': {}, 'resource_count': 1520, 'volume_count': 1312, 'size_bytes': 1089, 'etag': 'etag_value', 'description': 'description_value', 'pod_count': 971, 'config_backup_size_bytes': 2539}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_backup(request)


def test_create_backup_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            backup=gcg_backup.Backup(name='name_value'),
            backup_id='backup_id_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_backup(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*/backupPlans/*}/backups" % client.transport._host, args[1])


def test_create_backup_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_backup(
            gkebackup.CreateBackupRequest(),
            parent='parent_value',
            backup=gcg_backup.Backup(name='name_value'),
            backup_id='backup_id_value',
        )


def test_create_backup_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.ListBackupsRequest,
    dict,
])
def test_list_backups_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListBackupsResponse(
              next_page_token='next_page_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListBackupsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_backups(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListBackupsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_backups_rest_required_fields(request_type=gkebackup.ListBackupsRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_backups._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_backups._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gkebackup.ListBackupsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gkebackup.ListBackupsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_backups(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_backups_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_backups._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_backups_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_list_backups") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_list_backups") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.ListBackupsRequest.pb(gkebackup.ListBackupsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gkebackup.ListBackupsResponse.to_json(gkebackup.ListBackupsResponse())

        request = gkebackup.ListBackupsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gkebackup.ListBackupsResponse()

        client.list_backups(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_backups_rest_bad_request(transport: str = 'rest', request_type=gkebackup.ListBackupsRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_backups(request)


def test_list_backups_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListBackupsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListBackupsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_backups(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*/backupPlans/*}/backups" % client.transport._host, args[1])


def test_list_backups_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_backups(
            gkebackup.ListBackupsRequest(),
            parent='parent_value',
        )


def test_list_backups_rest_pager(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                    backup.Backup(),
                    backup.Backup(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListBackupsResponse(
                backups=[],
                next_page_token='def',
            ),
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListBackupsResponse(
                backups=[
                    backup.Backup(),
                    backup.Backup(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(gkebackup.ListBackupsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3'}

        pager = client.list_backups(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, backup.Backup)
                for i in results)

        pages = list(client.list_backups(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    gkebackup.GetBackupRequest,
    dict,
])
def test_get_backup_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = backup.Backup(
              name='name_value',
              uid='uid_value',
              manual=True,
              delete_lock_days=1675,
              retain_days=1171,
              contains_volume_data=True,
              contains_secrets=True,
              state=backup.Backup.State.CREATING,
              state_reason='state_reason_value',
              resource_count=1520,
              volume_count=1312,
              size_bytes=1089,
              etag='etag_value',
              description='description_value',
              pod_count=971,
              config_backup_size_bytes=2539,
              all_namespaces=True,
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = backup.Backup.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_backup(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, backup.Backup)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.manual is True
    assert response.delete_lock_days == 1675
    assert response.retain_days == 1171
    assert response.contains_volume_data is True
    assert response.contains_secrets is True
    assert response.state == backup.Backup.State.CREATING
    assert response.state_reason == 'state_reason_value'
    assert response.resource_count == 1520
    assert response.volume_count == 1312
    assert response.size_bytes == 1089
    assert response.etag == 'etag_value'
    assert response.description == 'description_value'
    assert response.pod_count == 971
    assert response.config_backup_size_bytes == 2539


def test_get_backup_rest_required_fields(request_type=gkebackup.GetBackupRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = backup.Backup()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = backup.Backup.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_backup(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_backup_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_backup._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_backup_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_get_backup") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_get_backup") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.GetBackupRequest.pb(gkebackup.GetBackupRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = backup.Backup.to_json(backup.Backup())

        request = gkebackup.GetBackupRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = backup.Backup()

        client.get_backup(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_backup_rest_bad_request(transport: str = 'rest', request_type=gkebackup.GetBackupRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_backup(request)


def test_get_backup_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = backup.Backup()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = backup.Backup.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_backup(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/backupPlans/*/backups/*}" % client.transport._host, args[1])


def test_get_backup_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_backup(
            gkebackup.GetBackupRequest(),
            name='name_value',
        )


def test_get_backup_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.UpdateBackupRequest,
    dict,
])
def test_update_backup_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'backup': {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}}
    request_init["backup"] = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'manual': True, 'labels': {}, 'delete_lock_days': 1675, 'delete_lock_expire_time': {}, 'retain_days': 1171, 'retain_expire_time': {}, 'encryption_key': {'gcp_kms_encryption_key': 'gcp_kms_encryption_key_value'}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'contains_volume_data': True, 'contains_secrets': True, 'cluster_metadata': {'cluster': 'cluster_value', 'k8s_version': 'k8s_version_value', 'backup_crd_versions': {}, 'gke_version': 'gke_version_value', 'anthos_version': 'anthos_version_value'}, 'state': 1, 'state_reason': 'state_reason_value', 'complete_time': {}, 'resource_count': 1520, 'volume_count': 1312, 'size_bytes': 1089, 'etag': 'etag_value', 'description': 'description_value', 'pod_count': 971, 'config_backup_size_bytes': 2539}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_backup(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_backup_rest_required_fields(request_type=gkebackup.UpdateBackupRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_backup._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_backup(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_backup_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_backup._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask", )) & set(("backup", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_backup_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_update_backup") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_update_backup") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.UpdateBackupRequest.pb(gkebackup.UpdateBackupRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.UpdateBackupRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_backup(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_backup_rest_bad_request(transport: str = 'rest', request_type=gkebackup.UpdateBackupRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'backup': {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}}
    request_init["backup"] = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'manual': True, 'labels': {}, 'delete_lock_days': 1675, 'delete_lock_expire_time': {}, 'retain_days': 1171, 'retain_expire_time': {}, 'encryption_key': {'gcp_kms_encryption_key': 'gcp_kms_encryption_key_value'}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'contains_volume_data': True, 'contains_secrets': True, 'cluster_metadata': {'cluster': 'cluster_value', 'k8s_version': 'k8s_version_value', 'backup_crd_versions': {}, 'gke_version': 'gke_version_value', 'anthos_version': 'anthos_version_value'}, 'state': 1, 'state_reason': 'state_reason_value', 'complete_time': {}, 'resource_count': 1520, 'volume_count': 1312, 'size_bytes': 1089, 'etag': 'etag_value', 'description': 'description_value', 'pod_count': 971, 'config_backup_size_bytes': 2539}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_backup(request)


def test_update_backup_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'backup': {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}}

        # get truthy value for each flattened field
        mock_args = dict(
            backup=gcg_backup.Backup(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_backup(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{backup.name=projects/*/locations/*/backupPlans/*/backups/*}" % client.transport._host, args[1])


def test_update_backup_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_backup(
            gkebackup.UpdateBackupRequest(),
            backup=gcg_backup.Backup(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_backup_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.DeleteBackupRequest,
    dict,
])
def test_delete_backup_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_backup(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_backup_rest_required_fields(request_type=gkebackup.DeleteBackupRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_backup._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("etag", "force", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_backup(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_backup_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_backup._get_unset_required_fields({})
    assert set(unset_fields) == (set(("etag", "force", )) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_backup_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_delete_backup") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_delete_backup") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.DeleteBackupRequest.pb(gkebackup.DeleteBackupRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.DeleteBackupRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_backup(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_backup_rest_bad_request(transport: str = 'rest', request_type=gkebackup.DeleteBackupRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_backup(request)


def test_delete_backup_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_backup(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/backupPlans/*/backups/*}" % client.transport._host, args[1])


def test_delete_backup_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_backup(
            gkebackup.DeleteBackupRequest(),
            name='name_value',
        )


def test_delete_backup_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.ListVolumeBackupsRequest,
    dict,
])
def test_list_volume_backups_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListVolumeBackupsResponse(
              next_page_token='next_page_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListVolumeBackupsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_volume_backups(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVolumeBackupsPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_volume_backups_rest_required_fields(request_type=gkebackup.ListVolumeBackupsRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_volume_backups._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_volume_backups._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gkebackup.ListVolumeBackupsResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gkebackup.ListVolumeBackupsResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_volume_backups(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_volume_backups_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_volume_backups._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_volume_backups_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_list_volume_backups") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_list_volume_backups") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.ListVolumeBackupsRequest.pb(gkebackup.ListVolumeBackupsRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gkebackup.ListVolumeBackupsResponse.to_json(gkebackup.ListVolumeBackupsResponse())

        request = gkebackup.ListVolumeBackupsRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gkebackup.ListVolumeBackupsResponse()

        client.list_volume_backups(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_volume_backups_rest_bad_request(transport: str = 'rest', request_type=gkebackup.ListVolumeBackupsRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_volume_backups(request)


def test_list_volume_backups_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListVolumeBackupsResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListVolumeBackupsResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_volume_backups(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*/backupPlans/*/backups/*}/volumeBackups" % client.transport._host, args[1])


def test_list_volume_backups_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_volume_backups(
            gkebackup.ListVolumeBackupsRequest(),
            parent='parent_value',
        )


def test_list_volume_backups_rest_pager(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[],
                next_page_token='def',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListVolumeBackupsResponse(
                volume_backups=[
                    volume.VolumeBackup(),
                    volume.VolumeBackup(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(gkebackup.ListVolumeBackupsResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4'}

        pager = client.list_volume_backups(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, volume.VolumeBackup)
                for i in results)

        pages = list(client.list_volume_backups(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    gkebackup.GetVolumeBackupRequest,
    dict,
])
def test_get_volume_backup_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4/volumeBackups/sample5'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = volume.VolumeBackup(
              name='name_value',
              uid='uid_value',
              volume_backup_handle='volume_backup_handle_value',
              format_=volume.VolumeBackup.VolumeBackupFormat.GCE_PERSISTENT_DISK,
              storage_bytes=1403,
              disk_size_bytes=1611,
              state=volume.VolumeBackup.State.CREATING,
              state_message='state_message_value',
              etag='etag_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = volume.VolumeBackup.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_volume_backup(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, volume.VolumeBackup)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.volume_backup_handle == 'volume_backup_handle_value'
    assert response.format_ == volume.VolumeBackup.VolumeBackupFormat.GCE_PERSISTENT_DISK
    assert response.storage_bytes == 1403
    assert response.disk_size_bytes == 1611
    assert response.state == volume.VolumeBackup.State.CREATING
    assert response.state_message == 'state_message_value'
    assert response.etag == 'etag_value'


def test_get_volume_backup_rest_required_fields(request_type=gkebackup.GetVolumeBackupRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_volume_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_volume_backup._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = volume.VolumeBackup()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = volume.VolumeBackup.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_volume_backup(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_volume_backup_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_volume_backup._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_volume_backup_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_get_volume_backup") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_get_volume_backup") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.GetVolumeBackupRequest.pb(gkebackup.GetVolumeBackupRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = volume.VolumeBackup.to_json(volume.VolumeBackup())

        request = gkebackup.GetVolumeBackupRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = volume.VolumeBackup()

        client.get_volume_backup(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_volume_backup_rest_bad_request(transport: str = 'rest', request_type=gkebackup.GetVolumeBackupRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4/volumeBackups/sample5'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_volume_backup(request)


def test_get_volume_backup_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = volume.VolumeBackup()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/backupPlans/sample3/backups/sample4/volumeBackups/sample5'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = volume.VolumeBackup.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_volume_backup(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/backupPlans/*/backups/*/volumeBackups/*}" % client.transport._host, args[1])


def test_get_volume_backup_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_volume_backup(
            gkebackup.GetVolumeBackupRequest(),
            name='name_value',
        )


def test_get_volume_backup_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.CreateRestorePlanRequest,
    dict,
])
def test_create_restore_plan_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["restore_plan"] = {'name': 'name_value', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'backup_plan': 'backup_plan_value', 'cluster': 'cluster_value', 'restore_config': {'volume_data_restore_policy': 1, 'cluster_resource_conflict_policy': 1, 'namespaced_resource_restore_mode': 1, 'cluster_resource_restore_scope': {'selected_group_kinds': [{'resource_group': 'resource_group_value', 'resource_kind': 'resource_kind_value'}]}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'substitution_rules': [{'target_namespaces': ['target_namespaces_value1', 'target_namespaces_value2'], 'target_group_kinds': {}, 'target_json_path': 'target_json_path_value', 'original_value_pattern': 'original_value_pattern_value', 'new_value': 'new_value_value'}]}, 'labels': {}, 'etag': 'etag_value'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_restore_plan(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_restore_plan_rest_required_fields(request_type=gkebackup.CreateRestorePlanRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["restore_plan_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "restorePlanId" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_restore_plan._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "restorePlanId" in jsonified_request
    assert jsonified_request["restorePlanId"] == request_init["restore_plan_id"]

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["restorePlanId"] = 'restore_plan_id_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_restore_plan._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("restore_plan_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "restorePlanId" in jsonified_request
    assert jsonified_request["restorePlanId"] == 'restore_plan_id_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_restore_plan(request)

            expected_params = [
                (
                    "restorePlanId",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_restore_plan_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_restore_plan._get_unset_required_fields({})
    assert set(unset_fields) == (set(("restorePlanId", )) & set(("parent", "restorePlan", "restorePlanId", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_restore_plan_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_create_restore_plan") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_create_restore_plan") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.CreateRestorePlanRequest.pb(gkebackup.CreateRestorePlanRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.CreateRestorePlanRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_restore_plan(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_restore_plan_rest_bad_request(transport: str = 'rest', request_type=gkebackup.CreateRestorePlanRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request_init["restore_plan"] = {'name': 'name_value', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'backup_plan': 'backup_plan_value', 'cluster': 'cluster_value', 'restore_config': {'volume_data_restore_policy': 1, 'cluster_resource_conflict_policy': 1, 'namespaced_resource_restore_mode': 1, 'cluster_resource_restore_scope': {'selected_group_kinds': [{'resource_group': 'resource_group_value', 'resource_kind': 'resource_kind_value'}]}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'substitution_rules': [{'target_namespaces': ['target_namespaces_value1', 'target_namespaces_value2'], 'target_group_kinds': {}, 'target_json_path': 'target_json_path_value', 'original_value_pattern': 'original_value_pattern_value', 'new_value': 'new_value_value'}]}, 'labels': {}, 'etag': 'etag_value'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_restore_plan(request)


def test_create_restore_plan_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            restore_plan_id='restore_plan_id_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_restore_plan(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/restorePlans" % client.transport._host, args[1])


def test_create_restore_plan_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_restore_plan(
            gkebackup.CreateRestorePlanRequest(),
            parent='parent_value',
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            restore_plan_id='restore_plan_id_value',
        )


def test_create_restore_plan_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.ListRestorePlansRequest,
    dict,
])
def test_list_restore_plans_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListRestorePlansResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListRestorePlansResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_restore_plans(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRestorePlansPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_restore_plans_rest_required_fields(request_type=gkebackup.ListRestorePlansRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_restore_plans._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_restore_plans._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gkebackup.ListRestorePlansResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gkebackup.ListRestorePlansResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_restore_plans(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_restore_plans_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_restore_plans._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_restore_plans_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_list_restore_plans") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_list_restore_plans") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.ListRestorePlansRequest.pb(gkebackup.ListRestorePlansRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gkebackup.ListRestorePlansResponse.to_json(gkebackup.ListRestorePlansResponse())

        request = gkebackup.ListRestorePlansRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gkebackup.ListRestorePlansResponse()

        client.list_restore_plans(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_restore_plans_rest_bad_request(transport: str = 'rest', request_type=gkebackup.ListRestorePlansRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_restore_plans(request)


def test_list_restore_plans_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListRestorePlansResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListRestorePlansResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_restore_plans(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*}/restorePlans" % client.transport._host, args[1])


def test_list_restore_plans_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_restore_plans(
            gkebackup.ListRestorePlansRequest(),
            parent='parent_value',
        )


def test_list_restore_plans_rest_pager(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[],
                next_page_token='def',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListRestorePlansResponse(
                restore_plans=[
                    restore_plan.RestorePlan(),
                    restore_plan.RestorePlan(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(gkebackup.ListRestorePlansResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2'}

        pager = client.list_restore_plans(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, restore_plan.RestorePlan)
                for i in results)

        pages = list(client.list_restore_plans(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    gkebackup.GetRestorePlanRequest,
    dict,
])
def test_get_restore_plan_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = restore_plan.RestorePlan(
              name='name_value',
              uid='uid_value',
              description='description_value',
              backup_plan='backup_plan_value',
              cluster='cluster_value',
              etag='etag_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = restore_plan.RestorePlan.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_restore_plan(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, restore_plan.RestorePlan)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.description == 'description_value'
    assert response.backup_plan == 'backup_plan_value'
    assert response.cluster == 'cluster_value'
    assert response.etag == 'etag_value'


def test_get_restore_plan_rest_required_fields(request_type=gkebackup.GetRestorePlanRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_restore_plan._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_restore_plan._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = restore_plan.RestorePlan()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = restore_plan.RestorePlan.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_restore_plan(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_restore_plan_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_restore_plan._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_restore_plan_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_get_restore_plan") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_get_restore_plan") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.GetRestorePlanRequest.pb(gkebackup.GetRestorePlanRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = restore_plan.RestorePlan.to_json(restore_plan.RestorePlan())

        request = gkebackup.GetRestorePlanRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = restore_plan.RestorePlan()

        client.get_restore_plan(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_restore_plan_rest_bad_request(transport: str = 'rest', request_type=gkebackup.GetRestorePlanRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_restore_plan(request)


def test_get_restore_plan_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = restore_plan.RestorePlan()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = restore_plan.RestorePlan.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_restore_plan(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/restorePlans/*}" % client.transport._host, args[1])


def test_get_restore_plan_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_restore_plan(
            gkebackup.GetRestorePlanRequest(),
            name='name_value',
        )


def test_get_restore_plan_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.UpdateRestorePlanRequest,
    dict,
])
def test_update_restore_plan_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'restore_plan': {'name': 'projects/sample1/locations/sample2/restorePlans/sample3'}}
    request_init["restore_plan"] = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'backup_plan': 'backup_plan_value', 'cluster': 'cluster_value', 'restore_config': {'volume_data_restore_policy': 1, 'cluster_resource_conflict_policy': 1, 'namespaced_resource_restore_mode': 1, 'cluster_resource_restore_scope': {'selected_group_kinds': [{'resource_group': 'resource_group_value', 'resource_kind': 'resource_kind_value'}]}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'substitution_rules': [{'target_namespaces': ['target_namespaces_value1', 'target_namespaces_value2'], 'target_group_kinds': {}, 'target_json_path': 'target_json_path_value', 'original_value_pattern': 'original_value_pattern_value', 'new_value': 'new_value_value'}]}, 'labels': {}, 'etag': 'etag_value'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_restore_plan(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_restore_plan_rest_required_fields(request_type=gkebackup.UpdateRestorePlanRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_restore_plan._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_restore_plan._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_restore_plan(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_restore_plan_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_restore_plan._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask", )) & set(("restorePlan", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_restore_plan_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_update_restore_plan") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_update_restore_plan") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.UpdateRestorePlanRequest.pb(gkebackup.UpdateRestorePlanRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.UpdateRestorePlanRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_restore_plan(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_restore_plan_rest_bad_request(transport: str = 'rest', request_type=gkebackup.UpdateRestorePlanRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'restore_plan': {'name': 'projects/sample1/locations/sample2/restorePlans/sample3'}}
    request_init["restore_plan"] = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'backup_plan': 'backup_plan_value', 'cluster': 'cluster_value', 'restore_config': {'volume_data_restore_policy': 1, 'cluster_resource_conflict_policy': 1, 'namespaced_resource_restore_mode': 1, 'cluster_resource_restore_scope': {'selected_group_kinds': [{'resource_group': 'resource_group_value', 'resource_kind': 'resource_kind_value'}]}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'substitution_rules': [{'target_namespaces': ['target_namespaces_value1', 'target_namespaces_value2'], 'target_group_kinds': {}, 'target_json_path': 'target_json_path_value', 'original_value_pattern': 'original_value_pattern_value', 'new_value': 'new_value_value'}]}, 'labels': {}, 'etag': 'etag_value'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_restore_plan(request)


def test_update_restore_plan_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'restore_plan': {'name': 'projects/sample1/locations/sample2/restorePlans/sample3'}}

        # get truthy value for each flattened field
        mock_args = dict(
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_restore_plan(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{restore_plan.name=projects/*/locations/*/restorePlans/*}" % client.transport._host, args[1])


def test_update_restore_plan_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_restore_plan(
            gkebackup.UpdateRestorePlanRequest(),
            restore_plan=gcg_restore_plan.RestorePlan(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_restore_plan_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.DeleteRestorePlanRequest,
    dict,
])
def test_delete_restore_plan_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_restore_plan(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_restore_plan_rest_required_fields(request_type=gkebackup.DeleteRestorePlanRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_restore_plan._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_restore_plan._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("etag", "force", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_restore_plan(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_restore_plan_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_restore_plan._get_unset_required_fields({})
    assert set(unset_fields) == (set(("etag", "force", )) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_restore_plan_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_delete_restore_plan") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_delete_restore_plan") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.DeleteRestorePlanRequest.pb(gkebackup.DeleteRestorePlanRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.DeleteRestorePlanRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_restore_plan(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_restore_plan_rest_bad_request(transport: str = 'rest', request_type=gkebackup.DeleteRestorePlanRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_restore_plan(request)


def test_delete_restore_plan_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_restore_plan(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/restorePlans/*}" % client.transport._host, args[1])


def test_delete_restore_plan_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_restore_plan(
            gkebackup.DeleteRestorePlanRequest(),
            name='name_value',
        )


def test_delete_restore_plan_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.CreateRestoreRequest,
    dict,
])
def test_create_restore_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3'}
    request_init["restore"] = {'name': 'name_value', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'backup': 'backup_value', 'cluster': 'cluster_value', 'restore_config': {'volume_data_restore_policy': 1, 'cluster_resource_conflict_policy': 1, 'namespaced_resource_restore_mode': 1, 'cluster_resource_restore_scope': {'selected_group_kinds': [{'resource_group': 'resource_group_value', 'resource_kind': 'resource_kind_value'}]}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'substitution_rules': [{'target_namespaces': ['target_namespaces_value1', 'target_namespaces_value2'], 'target_group_kinds': {}, 'target_json_path': 'target_json_path_value', 'original_value_pattern': 'original_value_pattern_value', 'new_value': 'new_value_value'}]}, 'labels': {}, 'state': 1, 'state_reason': 'state_reason_value', 'complete_time': {}, 'resources_restored_count': 2602, 'resources_excluded_count': 2576, 'resources_failed_count': 2343, 'volumes_restored_count': 2394, 'etag': 'etag_value'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.create_restore(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_create_restore_rest_required_fields(request_type=gkebackup.CreateRestoreRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["parent"] = ""
    request_init["restore_id"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped
    assert "restoreId" not in jsonified_request

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_restore._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present
    assert "restoreId" in jsonified_request
    assert jsonified_request["restoreId"] == request_init["restore_id"]

    jsonified_request["parent"] = 'parent_value'
    jsonified_request["restoreId"] = 'restore_id_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).create_restore._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("restore_id", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'
    assert "restoreId" in jsonified_request
    assert jsonified_request["restoreId"] == 'restore_id_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "post",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.create_restore(request)

            expected_params = [
                (
                    "restoreId",
                    "",
                ),
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_create_restore_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.create_restore._get_unset_required_fields({})
    assert set(unset_fields) == (set(("restoreId", )) & set(("parent", "restore", "restoreId", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_create_restore_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_create_restore") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_create_restore") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.CreateRestoreRequest.pb(gkebackup.CreateRestoreRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.CreateRestoreRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.create_restore(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_create_restore_rest_bad_request(transport: str = 'rest', request_type=gkebackup.CreateRestoreRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3'}
    request_init["restore"] = {'name': 'name_value', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'backup': 'backup_value', 'cluster': 'cluster_value', 'restore_config': {'volume_data_restore_policy': 1, 'cluster_resource_conflict_policy': 1, 'namespaced_resource_restore_mode': 1, 'cluster_resource_restore_scope': {'selected_group_kinds': [{'resource_group': 'resource_group_value', 'resource_kind': 'resource_kind_value'}]}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'substitution_rules': [{'target_namespaces': ['target_namespaces_value1', 'target_namespaces_value2'], 'target_group_kinds': {}, 'target_json_path': 'target_json_path_value', 'original_value_pattern': 'original_value_pattern_value', 'new_value': 'new_value_value'}]}, 'labels': {}, 'state': 1, 'state_reason': 'state_reason_value', 'complete_time': {}, 'resources_restored_count': 2602, 'resources_excluded_count': 2576, 'resources_failed_count': 2343, 'volumes_restored_count': 2394, 'etag': 'etag_value'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.create_restore(request)


def test_create_restore_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
            restore=gcg_restore.Restore(name='name_value'),
            restore_id='restore_id_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.create_restore(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*/restorePlans/*}/restores" % client.transport._host, args[1])


def test_create_restore_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.create_restore(
            gkebackup.CreateRestoreRequest(),
            parent='parent_value',
            restore=gcg_restore.Restore(name='name_value'),
            restore_id='restore_id_value',
        )


def test_create_restore_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.ListRestoresRequest,
    dict,
])
def test_list_restores_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListRestoresResponse(
              next_page_token='next_page_token_value',
              unreachable=['unreachable_value'],
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListRestoresResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_restores(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListRestoresPager)
    assert response.next_page_token == 'next_page_token_value'
    assert response.unreachable == ['unreachable_value']


def test_list_restores_rest_required_fields(request_type=gkebackup.ListRestoresRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_restores._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_restores._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gkebackup.ListRestoresResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gkebackup.ListRestoresResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_restores(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_restores_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_restores._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_restores_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_list_restores") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_list_restores") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.ListRestoresRequest.pb(gkebackup.ListRestoresRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gkebackup.ListRestoresResponse.to_json(gkebackup.ListRestoresResponse())

        request = gkebackup.ListRestoresRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gkebackup.ListRestoresResponse()

        client.list_restores(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_restores_rest_bad_request(transport: str = 'rest', request_type=gkebackup.ListRestoresRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_restores(request)


def test_list_restores_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListRestoresResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListRestoresResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_restores(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*/restorePlans/*}/restores" % client.transport._host, args[1])


def test_list_restores_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_restores(
            gkebackup.ListRestoresRequest(),
            parent='parent_value',
        )


def test_list_restores_rest_pager(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                    restore.Restore(),
                    restore.Restore(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListRestoresResponse(
                restores=[],
                next_page_token='def',
            ),
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListRestoresResponse(
                restores=[
                    restore.Restore(),
                    restore.Restore(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(gkebackup.ListRestoresResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3'}

        pager = client.list_restores(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, restore.Restore)
                for i in results)

        pages = list(client.list_restores(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    gkebackup.GetRestoreRequest,
    dict,
])
def test_get_restore_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = restore.Restore(
              name='name_value',
              uid='uid_value',
              description='description_value',
              backup='backup_value',
              cluster='cluster_value',
              state=restore.Restore.State.CREATING,
              state_reason='state_reason_value',
              resources_restored_count=2602,
              resources_excluded_count=2576,
              resources_failed_count=2343,
              volumes_restored_count=2394,
              etag='etag_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = restore.Restore.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_restore(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, restore.Restore)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.description == 'description_value'
    assert response.backup == 'backup_value'
    assert response.cluster == 'cluster_value'
    assert response.state == restore.Restore.State.CREATING
    assert response.state_reason == 'state_reason_value'
    assert response.resources_restored_count == 2602
    assert response.resources_excluded_count == 2576
    assert response.resources_failed_count == 2343
    assert response.volumes_restored_count == 2394
    assert response.etag == 'etag_value'


def test_get_restore_rest_required_fields(request_type=gkebackup.GetRestoreRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_restore._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_restore._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = restore.Restore()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = restore.Restore.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_restore(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_restore_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_restore._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_restore_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_get_restore") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_get_restore") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.GetRestoreRequest.pb(gkebackup.GetRestoreRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = restore.Restore.to_json(restore.Restore())

        request = gkebackup.GetRestoreRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = restore.Restore()

        client.get_restore(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_restore_rest_bad_request(transport: str = 'rest', request_type=gkebackup.GetRestoreRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_restore(request)


def test_get_restore_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = restore.Restore()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = restore.Restore.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_restore(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/restorePlans/*/restores/*}" % client.transport._host, args[1])


def test_get_restore_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_restore(
            gkebackup.GetRestoreRequest(),
            name='name_value',
        )


def test_get_restore_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.UpdateRestoreRequest,
    dict,
])
def test_update_restore_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'restore': {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}}
    request_init["restore"] = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'backup': 'backup_value', 'cluster': 'cluster_value', 'restore_config': {'volume_data_restore_policy': 1, 'cluster_resource_conflict_policy': 1, 'namespaced_resource_restore_mode': 1, 'cluster_resource_restore_scope': {'selected_group_kinds': [{'resource_group': 'resource_group_value', 'resource_kind': 'resource_kind_value'}]}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'substitution_rules': [{'target_namespaces': ['target_namespaces_value1', 'target_namespaces_value2'], 'target_group_kinds': {}, 'target_json_path': 'target_json_path_value', 'original_value_pattern': 'original_value_pattern_value', 'new_value': 'new_value_value'}]}, 'labels': {}, 'state': 1, 'state_reason': 'state_reason_value', 'complete_time': {}, 'resources_restored_count': 2602, 'resources_excluded_count': 2576, 'resources_failed_count': 2343, 'volumes_restored_count': 2394, 'etag': 'etag_value'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.update_restore(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_update_restore_rest_required_fields(request_type=gkebackup.UpdateRestoreRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_restore._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).update_restore._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("update_mask", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "patch",
                'query_params': pb_request,
            }
            transcode_result['body'] = pb_request
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.update_restore(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_update_restore_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.update_restore._get_unset_required_fields({})
    assert set(unset_fields) == (set(("updateMask", )) & set(("restore", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_update_restore_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_update_restore") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_update_restore") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.UpdateRestoreRequest.pb(gkebackup.UpdateRestoreRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.UpdateRestoreRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.update_restore(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_update_restore_rest_bad_request(transport: str = 'rest', request_type=gkebackup.UpdateRestoreRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'restore': {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}}
    request_init["restore"] = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4', 'uid': 'uid_value', 'create_time': {'seconds': 751, 'nanos': 543}, 'update_time': {}, 'description': 'description_value', 'backup': 'backup_value', 'cluster': 'cluster_value', 'restore_config': {'volume_data_restore_policy': 1, 'cluster_resource_conflict_policy': 1, 'namespaced_resource_restore_mode': 1, 'cluster_resource_restore_scope': {'selected_group_kinds': [{'resource_group': 'resource_group_value', 'resource_kind': 'resource_kind_value'}]}, 'all_namespaces': True, 'selected_namespaces': {'namespaces': ['namespaces_value1', 'namespaces_value2']}, 'selected_applications': {'namespaced_names': [{'namespace': 'namespace_value', 'name': 'name_value'}]}, 'substitution_rules': [{'target_namespaces': ['target_namespaces_value1', 'target_namespaces_value2'], 'target_group_kinds': {}, 'target_json_path': 'target_json_path_value', 'original_value_pattern': 'original_value_pattern_value', 'new_value': 'new_value_value'}]}, 'labels': {}, 'state': 1, 'state_reason': 'state_reason_value', 'complete_time': {}, 'resources_restored_count': 2602, 'resources_excluded_count': 2576, 'resources_failed_count': 2343, 'volumes_restored_count': 2394, 'etag': 'etag_value'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.update_restore(request)


def test_update_restore_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'restore': {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}}

        # get truthy value for each flattened field
        mock_args = dict(
            restore=gcg_restore.Restore(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.update_restore(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{restore.name=projects/*/locations/*/restorePlans/*/restores/*}" % client.transport._host, args[1])


def test_update_restore_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.update_restore(
            gkebackup.UpdateRestoreRequest(),
            restore=gcg_restore.Restore(name='name_value'),
            update_mask=field_mask_pb2.FieldMask(paths=['paths_value']),
        )


def test_update_restore_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.DeleteRestoreRequest,
    dict,
])
def test_delete_restore_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.delete_restore(request)

    # Establish that the response is the type that we expect.
    assert response.operation.name == "operations/spam"


def test_delete_restore_rest_required_fields(request_type=gkebackup.DeleteRestoreRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_restore._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).delete_restore._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("etag", "force", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = operations_pb2.Operation(name='operations/spam')
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "delete",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200
            json_return_value = json_format.MessageToJson(return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.delete_restore(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_delete_restore_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.delete_restore._get_unset_required_fields({})
    assert set(unset_fields) == (set(("etag", "force", )) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_delete_restore_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(operation.Operation, "_set_result_from_operation"), \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_delete_restore") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_delete_restore") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.DeleteRestoreRequest.pb(gkebackup.DeleteRestoreRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = json_format.MessageToJson(operations_pb2.Operation())

        request = gkebackup.DeleteRestoreRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = operations_pb2.Operation()

        client.delete_restore(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_delete_restore_rest_bad_request(transport: str = 'rest', request_type=gkebackup.DeleteRestoreRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.delete_restore(request)


def test_delete_restore_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = operations_pb2.Operation(name='operations/spam')

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        json_return_value = json_format.MessageToJson(return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.delete_restore(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/restorePlans/*/restores/*}" % client.transport._host, args[1])


def test_delete_restore_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.delete_restore(
            gkebackup.DeleteRestoreRequest(),
            name='name_value',
        )


def test_delete_restore_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


@pytest.mark.parametrize("request_type", [
    gkebackup.ListVolumeRestoresRequest,
    dict,
])
def test_list_volume_restores_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListVolumeRestoresResponse(
              next_page_token='next_page_token_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListVolumeRestoresResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.list_volume_restores(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, pagers.ListVolumeRestoresPager)
    assert response.next_page_token == 'next_page_token_value'


def test_list_volume_restores_rest_required_fields(request_type=gkebackup.ListVolumeRestoresRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["parent"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_volume_restores._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["parent"] = 'parent_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).list_volume_restores._get_unset_required_fields(jsonified_request)
    # Check that path parameters and body parameters are not mixing in.
    assert not set(unset_fields) - set(("filter", "order_by", "page_size", "page_token", ))
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "parent" in jsonified_request
    assert jsonified_request["parent"] == 'parent_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = gkebackup.ListVolumeRestoresResponse()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = gkebackup.ListVolumeRestoresResponse.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.list_volume_restores(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_list_volume_restores_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.list_volume_restores._get_unset_required_fields({})
    assert set(unset_fields) == (set(("filter", "orderBy", "pageSize", "pageToken", )) & set(("parent", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_list_volume_restores_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_list_volume_restores") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_list_volume_restores") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.ListVolumeRestoresRequest.pb(gkebackup.ListVolumeRestoresRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = gkebackup.ListVolumeRestoresResponse.to_json(gkebackup.ListVolumeRestoresResponse())

        request = gkebackup.ListVolumeRestoresRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = gkebackup.ListVolumeRestoresResponse()

        client.list_volume_restores(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_list_volume_restores_rest_bad_request(transport: str = 'rest', request_type=gkebackup.ListVolumeRestoresRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.list_volume_restores(request)


def test_list_volume_restores_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = gkebackup.ListVolumeRestoresResponse()

        # get arguments that satisfy an http rule for this method
        sample_request = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}

        # get truthy value for each flattened field
        mock_args = dict(
            parent='parent_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = gkebackup.ListVolumeRestoresResponse.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.list_volume_restores(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{parent=projects/*/locations/*/restorePlans/*/restores/*}/volumeRestores" % client.transport._host, args[1])


def test_list_volume_restores_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.list_volume_restores(
            gkebackup.ListVolumeRestoresRequest(),
            parent='parent_value',
        )


def test_list_volume_restores_rest_pager(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # TODO(kbandes): remove this mock unless there's a good reason for it.
        #with mock.patch.object(path_template, 'transcode') as transcode:
        # Set the response as a series of pages
        response = (
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                ],
                next_page_token='abc',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[],
                next_page_token='def',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                ],
                next_page_token='ghi',
            ),
            gkebackup.ListVolumeRestoresResponse(
                volume_restores=[
                    volume.VolumeRestore(),
                    volume.VolumeRestore(),
                ],
            ),
        )
        # Two responses for two calls
        response = response + response

        # Wrap the values into proper Response objs
        response = tuple(gkebackup.ListVolumeRestoresResponse.to_json(x) for x in response)
        return_values = tuple(Response() for i in response)
        for return_val, response_val in zip(return_values, response):
            return_val._content = response_val.encode('UTF-8')
            return_val.status_code = 200
        req.side_effect = return_values

        sample_request = {'parent': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4'}

        pager = client.list_volume_restores(request=sample_request)

        results = list(pager)
        assert len(results) == 6
        assert all(isinstance(i, volume.VolumeRestore)
                for i in results)

        pages = list(client.list_volume_restores(request=sample_request).pages)
        for page_, token in zip(pages, ['abc','def','ghi', '']):
            assert page_.raw_page.next_page_token == token


@pytest.mark.parametrize("request_type", [
    gkebackup.GetVolumeRestoreRequest,
    dict,
])
def test_get_volume_restore_rest(request_type):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4/volumeRestores/sample5'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = volume.VolumeRestore(
              name='name_value',
              uid='uid_value',
              volume_backup='volume_backup_value',
              volume_handle='volume_handle_value',
              volume_type=volume.VolumeRestore.VolumeType.GCE_PERSISTENT_DISK,
              state=volume.VolumeRestore.State.CREATING,
              state_message='state_message_value',
              etag='etag_value',
        )

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = volume.VolumeRestore.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)

        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value
        response = client.get_volume_restore(request)

    # Establish that the response is the type that we expect.
    assert isinstance(response, volume.VolumeRestore)
    assert response.name == 'name_value'
    assert response.uid == 'uid_value'
    assert response.volume_backup == 'volume_backup_value'
    assert response.volume_handle == 'volume_handle_value'
    assert response.volume_type == volume.VolumeRestore.VolumeType.GCE_PERSISTENT_DISK
    assert response.state == volume.VolumeRestore.State.CREATING
    assert response.state_message == 'state_message_value'
    assert response.etag == 'etag_value'


def test_get_volume_restore_rest_required_fields(request_type=gkebackup.GetVolumeRestoreRequest):
    transport_class = transports.BackupForGKERestTransport

    request_init = {}
    request_init["name"] = ""
    request = request_type(**request_init)
    pb_request = request_type.pb(request)
    jsonified_request = json.loads(json_format.MessageToJson(
        pb_request,
        including_default_value_fields=False,
        use_integers_for_enums=False
    ))

    # verify fields with default values are dropped

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_volume_restore._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with default values are now present

    jsonified_request["name"] = 'name_value'

    unset_fields = transport_class(credentials=ga_credentials.AnonymousCredentials()).get_volume_restore._get_unset_required_fields(jsonified_request)
    jsonified_request.update(unset_fields)

    # verify required fields with non-default values are left alone
    assert "name" in jsonified_request
    assert jsonified_request["name"] == 'name_value'

    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    request = request_type(**request_init)

    # Designate an appropriate value for the returned response.
    return_value = volume.VolumeRestore()
    # Mock the http request call within the method and fake a response.
    with mock.patch.object(Session, 'request') as req:
        # We need to mock transcode() because providing default values
        # for required fields will fail the real version if the http_options
        # expect actual values for those fields.
        with mock.patch.object(path_template, 'transcode') as transcode:
            # A uri without fields and an empty body will force all the
            # request fields to show up in the query_params.
            pb_request = request_type.pb(request)
            transcode_result = {
                'uri': 'v1/sample_method',
                'method': "get",
                'query_params': pb_request,
            }
            transcode.return_value = transcode_result

            response_value = Response()
            response_value.status_code = 200

            pb_return_value = volume.VolumeRestore.pb(return_value)
            json_return_value = json_format.MessageToJson(pb_return_value)

            response_value._content = json_return_value.encode('UTF-8')
            req.return_value = response_value

            response = client.get_volume_restore(request)

            expected_params = [
            ]
            actual_params = req.call_args.kwargs['params']
            assert expected_params == actual_params


def test_get_volume_restore_rest_unset_required_fields():
    transport = transports.BackupForGKERestTransport(credentials=ga_credentials.AnonymousCredentials)

    unset_fields = transport.get_volume_restore._get_unset_required_fields({})
    assert set(unset_fields) == (set(()) & set(("name", )))


@pytest.mark.parametrize("null_interceptor", [True, False])
def test_get_volume_restore_rest_interceptors(null_interceptor):
    transport = transports.BackupForGKERestTransport(
        credentials=ga_credentials.AnonymousCredentials(),
        interceptor=None if null_interceptor else transports.BackupForGKERestInterceptor(),
        )
    client = BackupForGKEClient(transport=transport)
    with mock.patch.object(type(client.transport._session), "request") as req, \
         mock.patch.object(path_template, "transcode")  as transcode, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "post_get_volume_restore") as post, \
         mock.patch.object(transports.BackupForGKERestInterceptor, "pre_get_volume_restore") as pre:
        pre.assert_not_called()
        post.assert_not_called()
        pb_message = gkebackup.GetVolumeRestoreRequest.pb(gkebackup.GetVolumeRestoreRequest())
        transcode.return_value = {
            "method": "post",
            "uri": "my_uri",
            "body": pb_message,
            "query_params": pb_message,
        }

        req.return_value = Response()
        req.return_value.status_code = 200
        req.return_value.request = PreparedRequest()
        req.return_value._content = volume.VolumeRestore.to_json(volume.VolumeRestore())

        request = gkebackup.GetVolumeRestoreRequest()
        metadata =[
            ("key", "val"),
            ("cephalopod", "squid"),
        ]
        pre.return_value = request, metadata
        post.return_value = volume.VolumeRestore()

        client.get_volume_restore(request, metadata=[("key", "val"), ("cephalopod", "squid"),])

        pre.assert_called_once()
        post.assert_called_once()


def test_get_volume_restore_rest_bad_request(transport: str = 'rest', request_type=gkebackup.GetVolumeRestoreRequest):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # send a request that will satisfy transcoding
    request_init = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4/volumeRestores/sample5'}
    request = request_type(**request_init)

    # Mock the http request call within the method and fake a BadRequest error.
    with mock.patch.object(Session, 'request') as req, pytest.raises(core_exceptions.BadRequest):
        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 400
        response_value.request = Request()
        req.return_value = response_value
        client.get_volume_restore(request)


def test_get_volume_restore_rest_flattened():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="rest",
    )

    # Mock the http request call within the method and fake a response.
    with mock.patch.object(type(client.transport._session), 'request') as req:
        # Designate an appropriate value for the returned response.
        return_value = volume.VolumeRestore()

        # get arguments that satisfy an http rule for this method
        sample_request = {'name': 'projects/sample1/locations/sample2/restorePlans/sample3/restores/sample4/volumeRestores/sample5'}

        # get truthy value for each flattened field
        mock_args = dict(
            name='name_value',
        )
        mock_args.update(sample_request)

        # Wrap the value into a proper Response obj
        response_value = Response()
        response_value.status_code = 200
        pb_return_value = volume.VolumeRestore.pb(return_value)
        json_return_value = json_format.MessageToJson(pb_return_value)
        response_value._content = json_return_value.encode('UTF-8')
        req.return_value = response_value

        client.get_volume_restore(**mock_args)

        # Establish that the underlying call was made with the expected
        # request object values.
        assert len(req.mock_calls) == 1
        _, args, _ = req.mock_calls[0]
        assert path_template.validate("%s/v1/{name=projects/*/locations/*/restorePlans/*/restores/*/volumeRestores/*}" % client.transport._host, args[1])


def test_get_volume_restore_rest_flattened_error(transport: str = 'rest'):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport=transport,
    )

    # Attempting to call a method with both a request object and flattened
    # fields is an error.
    with pytest.raises(ValueError):
        client.get_volume_restore(
            gkebackup.GetVolumeRestoreRequest(),
            name='name_value',
        )


def test_get_volume_restore_rest_error():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest'
    )


def test_credentials_transport_error():
    # It is an error to provide credentials and a transport instance.
    transport = transports.BackupForGKEGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BackupForGKEClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport,
        )

    # It is an error to provide a credentials file and a transport instance.
    transport = transports.BackupForGKEGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BackupForGKEClient(
            client_options={"credentials_file": "credentials.json"},
            transport=transport,
        )

    # It is an error to provide an api_key and a transport instance.
    transport = transports.BackupForGKEGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    options = client_options.ClientOptions()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BackupForGKEClient(
            client_options=options,
            transport=transport,
        )

    # It is an error to provide an api_key and a credential.
    options = mock.Mock()
    options.api_key = "api_key"
    with pytest.raises(ValueError):
        client = BackupForGKEClient(
            client_options=options,
            credentials=ga_credentials.AnonymousCredentials()
        )

    # It is an error to provide scopes and a transport instance.
    transport = transports.BackupForGKEGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    with pytest.raises(ValueError):
        client = BackupForGKEClient(
            client_options={"scopes": ["1", "2"]},
            transport=transport,
        )


def test_transport_instance():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BackupForGKEGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    client = BackupForGKEClient(transport=transport)
    assert client.transport is transport

def test_transport_get_channel():
    # A client may be instantiated with a custom transport instance.
    transport = transports.BackupForGKEGrpcTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

    transport = transports.BackupForGKEGrpcAsyncIOTransport(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    channel = transport.grpc_channel
    assert channel

@pytest.mark.parametrize("transport_class", [
    transports.BackupForGKEGrpcTransport,
    transports.BackupForGKEGrpcAsyncIOTransport,
    transports.BackupForGKERestTransport,
])
def test_transport_adc(transport_class):
    # Test default credentials are used if not provided.
    with mock.patch.object(google.auth, 'default') as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class()
        adc.assert_called_once()

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "rest",
])
def test_transport_kind(transport_name):
    transport = BackupForGKEClient.get_transport_class(transport_name)(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert transport.kind == transport_name

def test_transport_grpc_default():
    # A client should use the gRPC transport by default.
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
    )
    assert isinstance(
        client.transport,
        transports.BackupForGKEGrpcTransport,
    )

def test_backup_for_gke_base_transport_error():
    # Passing both a credentials object and credentials_file should raise an error
    with pytest.raises(core_exceptions.DuplicateCredentialArgs):
        transport = transports.BackupForGKETransport(
            credentials=ga_credentials.AnonymousCredentials(),
            credentials_file="credentials.json"
        )


def test_backup_for_gke_base_transport():
    # Instantiate the base transport.
    with mock.patch('google.cloud.gke_backup_v1.services.backup_for_gke.transports.BackupForGKETransport.__init__') as Transport:
        Transport.return_value = None
        transport = transports.BackupForGKETransport(
            credentials=ga_credentials.AnonymousCredentials(),
        )

    # Every method on the transport should just blindly
    # raise NotImplementedError.
    methods = (
        'create_backup_plan',
        'list_backup_plans',
        'get_backup_plan',
        'update_backup_plan',
        'delete_backup_plan',
        'create_backup',
        'list_backups',
        'get_backup',
        'update_backup',
        'delete_backup',
        'list_volume_backups',
        'get_volume_backup',
        'create_restore_plan',
        'list_restore_plans',
        'get_restore_plan',
        'update_restore_plan',
        'delete_restore_plan',
        'create_restore',
        'list_restores',
        'get_restore',
        'update_restore',
        'delete_restore',
        'list_volume_restores',
        'get_volume_restore',
    )
    for method in methods:
        with pytest.raises(NotImplementedError):
            getattr(transport, method)(request=object())

    with pytest.raises(NotImplementedError):
        transport.close()

    # Additionally, the LRO client (a property) should
    # also raise NotImplementedError
    with pytest.raises(NotImplementedError):
        transport.operations_client

    # Catch all for all remaining methods and properties
    remainder = [
        'kind',
    ]
    for r in remainder:
        with pytest.raises(NotImplementedError):
            getattr(transport, r)()


def test_backup_for_gke_base_transport_with_credentials_file():
    # Instantiate the base transport with a credentials file
    with mock.patch.object(google.auth, 'load_credentials_from_file', autospec=True) as load_creds, mock.patch('google.cloud.gke_backup_v1.services.backup_for_gke.transports.BackupForGKETransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        load_creds.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BackupForGKETransport(
            credentials_file="credentials.json",
            quota_project_id="octopus",
        )
        load_creds.assert_called_once_with("credentials.json",
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id="octopus",
        )


def test_backup_for_gke_base_transport_with_adc():
    # Test the default credentials are used if credentials and credentials_file are None.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc, mock.patch('google.cloud.gke_backup_v1.services.backup_for_gke.transports.BackupForGKETransport._prep_wrapped_messages') as Transport:
        Transport.return_value = None
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport = transports.BackupForGKETransport()
        adc.assert_called_once()


def test_backup_for_gke_auth_adc():
    # If no credentials are provided, we should use ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        BackupForGKEClient()
        adc.assert_called_once_with(
            scopes=None,
            default_scopes=(
            'https://www.googleapis.com/auth/cloud-platform',
),
            quota_project_id=None,
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BackupForGKEGrpcTransport,
        transports.BackupForGKEGrpcAsyncIOTransport,
    ],
)
def test_backup_for_gke_transport_auth_adc(transport_class):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, 'default', autospec=True) as adc:
        adc.return_value = (ga_credentials.AnonymousCredentials(), None)
        transport_class(quota_project_id="octopus", scopes=["1", "2"])
        adc.assert_called_once_with(
            scopes=["1", "2"],
            default_scopes=(                'https://www.googleapis.com/auth/cloud-platform',),
            quota_project_id="octopus",
        )


@pytest.mark.parametrize(
    "transport_class",
    [
        transports.BackupForGKEGrpcTransport,
        transports.BackupForGKEGrpcAsyncIOTransport,
        transports.BackupForGKERestTransport,
    ],
)
def test_backup_for_gke_transport_auth_gdch_credentials(transport_class):
    host = 'https://language.com'
    api_audience_tests = [None, 'https://language2.com']
    api_audience_expect = [host, 'https://language2.com']
    for t, e in zip(api_audience_tests, api_audience_expect):
        with mock.patch.object(google.auth, 'default', autospec=True) as adc:
            gdch_mock = mock.MagicMock()
            type(gdch_mock).with_gdch_audience = mock.PropertyMock(return_value=gdch_mock)
            adc.return_value = (gdch_mock, None)
            transport_class(host=host, api_audience=t)
            gdch_mock.with_gdch_audience.assert_called_once_with(
                e
            )


@pytest.mark.parametrize(
    "transport_class,grpc_helpers",
    [
        (transports.BackupForGKEGrpcTransport, grpc_helpers),
        (transports.BackupForGKEGrpcAsyncIOTransport, grpc_helpers_async)
    ],
)
def test_backup_for_gke_transport_create_channel(transport_class, grpc_helpers):
    # If credentials and host are not provided, the transport class should use
    # ADC credentials.
    with mock.patch.object(google.auth, "default", autospec=True) as adc, mock.patch.object(
        grpc_helpers, "create_channel", autospec=True
    ) as create_channel:
        creds = ga_credentials.AnonymousCredentials()
        adc.return_value = (creds, None)
        transport_class(
            quota_project_id="octopus",
            scopes=["1", "2"]
        )

        create_channel.assert_called_with(
            "gkebackup.googleapis.com:443",
            credentials=creds,
            credentials_file=None,
            quota_project_id="octopus",
            default_scopes=(
                'https://www.googleapis.com/auth/cloud-platform',
),
            scopes=["1", "2"],
            default_host="gkebackup.googleapis.com",
            ssl_credentials=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )


@pytest.mark.parametrize("transport_class", [transports.BackupForGKEGrpcTransport, transports.BackupForGKEGrpcAsyncIOTransport])
def test_backup_for_gke_grpc_transport_client_cert_source_for_mtls(
    transport_class
):
    cred = ga_credentials.AnonymousCredentials()

    # Check ssl_channel_credentials is used if provided.
    with mock.patch.object(transport_class, "create_channel") as mock_create_channel:
        mock_ssl_channel_creds = mock.Mock()
        transport_class(
            host="squid.clam.whelk",
            credentials=cred,
            ssl_channel_credentials=mock_ssl_channel_creds
        )
        mock_create_channel.assert_called_once_with(
            "squid.clam.whelk:443",
            credentials=cred,
            credentials_file=None,
            scopes=None,
            ssl_credentials=mock_ssl_channel_creds,
            quota_project_id=None,
            options=[
                ("grpc.max_send_message_length", -1),
                ("grpc.max_receive_message_length", -1),
            ],
        )

    # Check if ssl_channel_credentials is not provided, then client_cert_source_for_mtls
    # is used.
    with mock.patch.object(transport_class, "create_channel", return_value=mock.Mock()):
        with mock.patch("grpc.ssl_channel_credentials") as mock_ssl_cred:
            transport_class(
                credentials=cred,
                client_cert_source_for_mtls=client_cert_source_callback
            )
            expected_cert, expected_key = client_cert_source_callback()
            mock_ssl_cred.assert_called_once_with(
                certificate_chain=expected_cert,
                private_key=expected_key
            )

def test_backup_for_gke_http_transport_client_cert_source_for_mtls():
    cred = ga_credentials.AnonymousCredentials()
    with mock.patch("google.auth.transport.requests.AuthorizedSession.configure_mtls_channel") as mock_configure_mtls_channel:
        transports.BackupForGKERestTransport (
            credentials=cred,
            client_cert_source_for_mtls=client_cert_source_callback
        )
        mock_configure_mtls_channel.assert_called_once_with(client_cert_source_callback)


def test_backup_for_gke_rest_lro_client():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='rest',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.AbstractOperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_backup_for_gke_host_no_port(transport_name):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='gkebackup.googleapis.com'),
         transport=transport_name,
    )
    assert client.transport._host == (
        'gkebackup.googleapis.com:443'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://gkebackup.googleapis.com'
    )

@pytest.mark.parametrize("transport_name", [
    "grpc",
    "grpc_asyncio",
    "rest",
])
def test_backup_for_gke_host_with_port(transport_name):
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        client_options=client_options.ClientOptions(api_endpoint='gkebackup.googleapis.com:8000'),
        transport=transport_name,
    )
    assert client.transport._host == (
        'gkebackup.googleapis.com:8000'
        if transport_name in ['grpc', 'grpc_asyncio']
        else 'https://gkebackup.googleapis.com:8000'
    )

@pytest.mark.parametrize("transport_name", [
    "rest",
])
def test_backup_for_gke_client_transport_session_collision(transport_name):
    creds1 = ga_credentials.AnonymousCredentials()
    creds2 = ga_credentials.AnonymousCredentials()
    client1 = BackupForGKEClient(
        credentials=creds1,
        transport=transport_name,
    )
    client2 = BackupForGKEClient(
        credentials=creds2,
        transport=transport_name,
    )
    session1 = client1.transport.create_backup_plan._session
    session2 = client2.transport.create_backup_plan._session
    assert session1 != session2
    session1 = client1.transport.list_backup_plans._session
    session2 = client2.transport.list_backup_plans._session
    assert session1 != session2
    session1 = client1.transport.get_backup_plan._session
    session2 = client2.transport.get_backup_plan._session
    assert session1 != session2
    session1 = client1.transport.update_backup_plan._session
    session2 = client2.transport.update_backup_plan._session
    assert session1 != session2
    session1 = client1.transport.delete_backup_plan._session
    session2 = client2.transport.delete_backup_plan._session
    assert session1 != session2
    session1 = client1.transport.create_backup._session
    session2 = client2.transport.create_backup._session
    assert session1 != session2
    session1 = client1.transport.list_backups._session
    session2 = client2.transport.list_backups._session
    assert session1 != session2
    session1 = client1.transport.get_backup._session
    session2 = client2.transport.get_backup._session
    assert session1 != session2
    session1 = client1.transport.update_backup._session
    session2 = client2.transport.update_backup._session
    assert session1 != session2
    session1 = client1.transport.delete_backup._session
    session2 = client2.transport.delete_backup._session
    assert session1 != session2
    session1 = client1.transport.list_volume_backups._session
    session2 = client2.transport.list_volume_backups._session
    assert session1 != session2
    session1 = client1.transport.get_volume_backup._session
    session2 = client2.transport.get_volume_backup._session
    assert session1 != session2
    session1 = client1.transport.create_restore_plan._session
    session2 = client2.transport.create_restore_plan._session
    assert session1 != session2
    session1 = client1.transport.list_restore_plans._session
    session2 = client2.transport.list_restore_plans._session
    assert session1 != session2
    session1 = client1.transport.get_restore_plan._session
    session2 = client2.transport.get_restore_plan._session
    assert session1 != session2
    session1 = client1.transport.update_restore_plan._session
    session2 = client2.transport.update_restore_plan._session
    assert session1 != session2
    session1 = client1.transport.delete_restore_plan._session
    session2 = client2.transport.delete_restore_plan._session
    assert session1 != session2
    session1 = client1.transport.create_restore._session
    session2 = client2.transport.create_restore._session
    assert session1 != session2
    session1 = client1.transport.list_restores._session
    session2 = client2.transport.list_restores._session
    assert session1 != session2
    session1 = client1.transport.get_restore._session
    session2 = client2.transport.get_restore._session
    assert session1 != session2
    session1 = client1.transport.update_restore._session
    session2 = client2.transport.update_restore._session
    assert session1 != session2
    session1 = client1.transport.delete_restore._session
    session2 = client2.transport.delete_restore._session
    assert session1 != session2
    session1 = client1.transport.list_volume_restores._session
    session2 = client2.transport.list_volume_restores._session
    assert session1 != session2
    session1 = client1.transport.get_volume_restore._session
    session2 = client2.transport.get_volume_restore._session
    assert session1 != session2
def test_backup_for_gke_grpc_transport_channel():
    channel = grpc.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BackupForGKEGrpcTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


def test_backup_for_gke_grpc_asyncio_transport_channel():
    channel = aio.secure_channel('http://localhost/', grpc.local_channel_credentials())

    # Check that channel is used if provided.
    transport = transports.BackupForGKEGrpcAsyncIOTransport(
        host="squid.clam.whelk",
        channel=channel,
    )
    assert transport.grpc_channel == channel
    assert transport._host == "squid.clam.whelk:443"
    assert transport._ssl_channel_credentials == None


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.BackupForGKEGrpcTransport, transports.BackupForGKEGrpcAsyncIOTransport])
def test_backup_for_gke_transport_channel_mtls_with_client_cert_source(
    transport_class
):
    with mock.patch("grpc.ssl_channel_credentials", autospec=True) as grpc_ssl_channel_cred:
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_ssl_cred = mock.Mock()
            grpc_ssl_channel_cred.return_value = mock_ssl_cred

            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel

            cred = ga_credentials.AnonymousCredentials()
            with pytest.warns(DeprecationWarning):
                with mock.patch.object(google.auth, 'default') as adc:
                    adc.return_value = (cred, None)
                    transport = transport_class(
                        host="squid.clam.whelk",
                        api_mtls_endpoint="mtls.squid.clam.whelk",
                        client_cert_source=client_cert_source_callback,
                    )
                    adc.assert_called_once()

            grpc_ssl_channel_cred.assert_called_once_with(
                certificate_chain=b"cert bytes", private_key=b"key bytes"
            )
            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel
            assert transport._ssl_channel_credentials == mock_ssl_cred


# Remove this test when deprecated arguments (api_mtls_endpoint, client_cert_source) are
# removed from grpc/grpc_asyncio transport constructor.
@pytest.mark.parametrize("transport_class", [transports.BackupForGKEGrpcTransport, transports.BackupForGKEGrpcAsyncIOTransport])
def test_backup_for_gke_transport_channel_mtls_with_adc(
    transport_class
):
    mock_ssl_cred = mock.Mock()
    with mock.patch.multiple(
        "google.auth.transport.grpc.SslCredentials",
        __init__=mock.Mock(return_value=None),
        ssl_credentials=mock.PropertyMock(return_value=mock_ssl_cred),
    ):
        with mock.patch.object(transport_class, "create_channel") as grpc_create_channel:
            mock_grpc_channel = mock.Mock()
            grpc_create_channel.return_value = mock_grpc_channel
            mock_cred = mock.Mock()

            with pytest.warns(DeprecationWarning):
                transport = transport_class(
                    host="squid.clam.whelk",
                    credentials=mock_cred,
                    api_mtls_endpoint="mtls.squid.clam.whelk",
                    client_cert_source=None,
                )

            grpc_create_channel.assert_called_once_with(
                "mtls.squid.clam.whelk:443",
                credentials=mock_cred,
                credentials_file=None,
                scopes=None,
                ssl_credentials=mock_ssl_cred,
                quota_project_id=None,
                options=[
                    ("grpc.max_send_message_length", -1),
                    ("grpc.max_receive_message_length", -1),
                ],
            )
            assert transport.grpc_channel == mock_grpc_channel


def test_backup_for_gke_grpc_lro_client():
    client = BackupForGKEClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_backup_for_gke_grpc_lro_async_client():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport='grpc_asyncio',
    )
    transport = client.transport

    # Ensure that we have a api-core operations client.
    assert isinstance(
        transport.operations_client,
        operations_v1.OperationsAsyncClient,
    )

    # Ensure that subsequent calls to the property send the exact same object.
    assert transport.operations_client is transport.operations_client


def test_backup_path():
    project = "squid"
    location = "clam"
    backup_plan = "whelk"
    backup = "octopus"
    expected = "projects/{project}/locations/{location}/backupPlans/{backup_plan}/backups/{backup}".format(project=project, location=location, backup_plan=backup_plan, backup=backup, )
    actual = BackupForGKEClient.backup_path(project, location, backup_plan, backup)
    assert expected == actual


def test_parse_backup_path():
    expected = {
        "project": "oyster",
        "location": "nudibranch",
        "backup_plan": "cuttlefish",
        "backup": "mussel",
    }
    path = BackupForGKEClient.backup_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_backup_path(path)
    assert expected == actual

def test_backup_plan_path():
    project = "winkle"
    location = "nautilus"
    backup_plan = "scallop"
    expected = "projects/{project}/locations/{location}/backupPlans/{backup_plan}".format(project=project, location=location, backup_plan=backup_plan, )
    actual = BackupForGKEClient.backup_plan_path(project, location, backup_plan)
    assert expected == actual


def test_parse_backup_plan_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "backup_plan": "clam",
    }
    path = BackupForGKEClient.backup_plan_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_backup_plan_path(path)
    assert expected == actual

def test_cluster_path():
    project = "whelk"
    location = "octopus"
    cluster = "oyster"
    expected = "projects/{project}/locations/{location}/clusters/{cluster}".format(project=project, location=location, cluster=cluster, )
    actual = BackupForGKEClient.cluster_path(project, location, cluster)
    assert expected == actual


def test_parse_cluster_path():
    expected = {
        "project": "nudibranch",
        "location": "cuttlefish",
        "cluster": "mussel",
    }
    path = BackupForGKEClient.cluster_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_cluster_path(path)
    assert expected == actual

def test_crypto_key_path():
    project = "winkle"
    location = "nautilus"
    key_ring = "scallop"
    crypto_key = "abalone"
    expected = "projects/{project}/locations/{location}/keyRings/{key_ring}/cryptoKeys/{crypto_key}".format(project=project, location=location, key_ring=key_ring, crypto_key=crypto_key, )
    actual = BackupForGKEClient.crypto_key_path(project, location, key_ring, crypto_key)
    assert expected == actual


def test_parse_crypto_key_path():
    expected = {
        "project": "squid",
        "location": "clam",
        "key_ring": "whelk",
        "crypto_key": "octopus",
    }
    path = BackupForGKEClient.crypto_key_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_crypto_key_path(path)
    assert expected == actual

def test_restore_path():
    project = "oyster"
    location = "nudibranch"
    restore_plan = "cuttlefish"
    restore = "mussel"
    expected = "projects/{project}/locations/{location}/restorePlans/{restore_plan}/restores/{restore}".format(project=project, location=location, restore_plan=restore_plan, restore=restore, )
    actual = BackupForGKEClient.restore_path(project, location, restore_plan, restore)
    assert expected == actual


def test_parse_restore_path():
    expected = {
        "project": "winkle",
        "location": "nautilus",
        "restore_plan": "scallop",
        "restore": "abalone",
    }
    path = BackupForGKEClient.restore_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_restore_path(path)
    assert expected == actual

def test_restore_plan_path():
    project = "squid"
    location = "clam"
    restore_plan = "whelk"
    expected = "projects/{project}/locations/{location}/restorePlans/{restore_plan}".format(project=project, location=location, restore_plan=restore_plan, )
    actual = BackupForGKEClient.restore_plan_path(project, location, restore_plan)
    assert expected == actual


def test_parse_restore_plan_path():
    expected = {
        "project": "octopus",
        "location": "oyster",
        "restore_plan": "nudibranch",
    }
    path = BackupForGKEClient.restore_plan_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_restore_plan_path(path)
    assert expected == actual

def test_volume_backup_path():
    project = "cuttlefish"
    location = "mussel"
    backup_plan = "winkle"
    backup = "nautilus"
    volume_backup = "scallop"
    expected = "projects/{project}/locations/{location}/backupPlans/{backup_plan}/backups/{backup}/volumeBackups/{volume_backup}".format(project=project, location=location, backup_plan=backup_plan, backup=backup, volume_backup=volume_backup, )
    actual = BackupForGKEClient.volume_backup_path(project, location, backup_plan, backup, volume_backup)
    assert expected == actual


def test_parse_volume_backup_path():
    expected = {
        "project": "abalone",
        "location": "squid",
        "backup_plan": "clam",
        "backup": "whelk",
        "volume_backup": "octopus",
    }
    path = BackupForGKEClient.volume_backup_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_volume_backup_path(path)
    assert expected == actual

def test_volume_restore_path():
    project = "oyster"
    location = "nudibranch"
    restore_plan = "cuttlefish"
    restore = "mussel"
    volume_restore = "winkle"
    expected = "projects/{project}/locations/{location}/restorePlans/{restore_plan}/restores/{restore}/volumeRestores/{volume_restore}".format(project=project, location=location, restore_plan=restore_plan, restore=restore, volume_restore=volume_restore, )
    actual = BackupForGKEClient.volume_restore_path(project, location, restore_plan, restore, volume_restore)
    assert expected == actual


def test_parse_volume_restore_path():
    expected = {
        "project": "nautilus",
        "location": "scallop",
        "restore_plan": "abalone",
        "restore": "squid",
        "volume_restore": "clam",
    }
    path = BackupForGKEClient.volume_restore_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_volume_restore_path(path)
    assert expected == actual

def test_common_billing_account_path():
    billing_account = "whelk"
    expected = "billingAccounts/{billing_account}".format(billing_account=billing_account, )
    actual = BackupForGKEClient.common_billing_account_path(billing_account)
    assert expected == actual


def test_parse_common_billing_account_path():
    expected = {
        "billing_account": "octopus",
    }
    path = BackupForGKEClient.common_billing_account_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_common_billing_account_path(path)
    assert expected == actual

def test_common_folder_path():
    folder = "oyster"
    expected = "folders/{folder}".format(folder=folder, )
    actual = BackupForGKEClient.common_folder_path(folder)
    assert expected == actual


def test_parse_common_folder_path():
    expected = {
        "folder": "nudibranch",
    }
    path = BackupForGKEClient.common_folder_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_common_folder_path(path)
    assert expected == actual

def test_common_organization_path():
    organization = "cuttlefish"
    expected = "organizations/{organization}".format(organization=organization, )
    actual = BackupForGKEClient.common_organization_path(organization)
    assert expected == actual


def test_parse_common_organization_path():
    expected = {
        "organization": "mussel",
    }
    path = BackupForGKEClient.common_organization_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_common_organization_path(path)
    assert expected == actual

def test_common_project_path():
    project = "winkle"
    expected = "projects/{project}".format(project=project, )
    actual = BackupForGKEClient.common_project_path(project)
    assert expected == actual


def test_parse_common_project_path():
    expected = {
        "project": "nautilus",
    }
    path = BackupForGKEClient.common_project_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_common_project_path(path)
    assert expected == actual

def test_common_location_path():
    project = "scallop"
    location = "abalone"
    expected = "projects/{project}/locations/{location}".format(project=project, location=location, )
    actual = BackupForGKEClient.common_location_path(project, location)
    assert expected == actual


def test_parse_common_location_path():
    expected = {
        "project": "squid",
        "location": "clam",
    }
    path = BackupForGKEClient.common_location_path(**expected)

    # Check that the path construction is reversible.
    actual = BackupForGKEClient.parse_common_location_path(path)
    assert expected == actual


def test_client_with_default_client_info():
    client_info = gapic_v1.client_info.ClientInfo()

    with mock.patch.object(transports.BackupForGKETransport, '_prep_wrapped_messages') as prep:
        client = BackupForGKEClient(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

    with mock.patch.object(transports.BackupForGKETransport, '_prep_wrapped_messages') as prep:
        transport_class = BackupForGKEClient.get_transport_class()
        transport = transport_class(
            credentials=ga_credentials.AnonymousCredentials(),
            client_info=client_info,
        )
        prep.assert_called_once_with(client_info)

@pytest.mark.asyncio
async def test_transport_close_async():
    client = BackupForGKEAsyncClient(
        credentials=ga_credentials.AnonymousCredentials(),
        transport="grpc_asyncio",
    )
    with mock.patch.object(type(getattr(client.transport, "grpc_channel")), "close") as close:
        async with client:
            close.assert_not_called()
        close.assert_called_once()


def test_transport_close():
    transports = {
        "rest": "_session",
        "grpc": "_grpc_channel",
    }

    for transport, close_name in transports.items():
        client = BackupForGKEClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        with mock.patch.object(type(getattr(client.transport, close_name)), "close") as close:
            with client:
                close.assert_not_called()
            close.assert_called_once()

def test_client_ctx():
    transports = [
        'rest',
        'grpc',
    ]
    for transport in transports:
        client = BackupForGKEClient(
            credentials=ga_credentials.AnonymousCredentials(),
            transport=transport
        )
        # Test client calls underlying transport.
        with mock.patch.object(type(client.transport), "close") as close:
            close.assert_not_called()
            with client:
                pass
            close.assert_called()

@pytest.mark.parametrize("client_class,transport_class", [
    (BackupForGKEClient, transports.BackupForGKEGrpcTransport),
    (BackupForGKEAsyncClient, transports.BackupForGKEGrpcAsyncIOTransport),
])
def test_api_key_credentials(client_class, transport_class):
    with mock.patch.object(
        google.auth._default, "get_api_key_credentials", create=True
    ) as get_api_key_credentials:
        mock_cred = mock.Mock()
        get_api_key_credentials.return_value = mock_cred
        options = client_options.ClientOptions()
        options.api_key = "api_key"
        with mock.patch.object(transport_class, "__init__") as patched:
            patched.return_value = None
            client = client_class(client_options=options)
            patched.assert_called_once_with(
                credentials=mock_cred,
                credentials_file=None,
                host=client.DEFAULT_ENDPOINT,
                scopes=None,
                client_cert_source_for_mtls=None,
                quota_project_id=None,
                client_info=transports.base.DEFAULT_CLIENT_INFO,
                always_use_jwt_access=True,
                api_audience=None,
            )
