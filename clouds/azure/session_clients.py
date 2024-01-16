import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.redhatopenshift import AzureRedHatOpenShiftClient
from vars import azure_client_credentials_env_vars


class MissingAzureCredentials(Exception):
    pass


def assert_azure_credentials():
    azure_required_env_vars = azure_client_credentials_env_vars.values()
    if not all([os.getenv(azure_env_var) for azure_env_var in azure_required_env_vars]):
        raise MissingAzureCredentials(
            f"Some required environment variables for Azure clients auth are missing, "
            f"required keys: {azure_required_env_vars}"
        )


def get_subscription_id():
    subscription_id = os.getenv(key=azure_client_credentials_env_vars["subscription_id"])
    assert subscription_id, "Azure subscription ID must be set as an environment variable."
    return subscription_id


def get_azure_credentials():
    # TODO: check how to get credentials using an identity provider.
    assert_azure_credentials()
    return DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True,
        exclude_developer_cli_credential=True,
        exclude_shared_token_cache_credential=True,
        exclude_powershell_credential=True,
        exclude_cli_credential=False,
        exclude_interactive_browser_credential=True,
        exclude_visual_studio_code_credential=True,
        exclude_workload_identity_credential=True,
    )


def get_aro_client(credential=None):
    return AzureRedHatOpenShiftClient(credential=credential, subscription_id=get_subscription_id())


def get_network_client(credential=None):
    return NetworkManagementClient(credential=credential, subscription_id=get_subscription_id())


def get_resource_client(credential=None):
    return ResourceManagementClient(credential=credential, subscription_id=get_subscription_id())
