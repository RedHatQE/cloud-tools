from azure.identity import ClientSecretCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.redhatopenshift import AzureRedHatOpenShiftClient


def azure_credentials(tenant_id, client_id, client_secret) -> ClientSecretCredential:
    return ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
    )


def aro_client(credential, subscription_id) -> AzureRedHatOpenShiftClient:
    return AzureRedHatOpenShiftClient(credential=credential, subscription_id=subscription_id)


def network_client(credential, subscription_id) -> NetworkManagementClient:
    return NetworkManagementClient(credential=credential, subscription_id=subscription_id)


def resource_client(credential, subscription_id) -> ResourceManagementClient:
    return ResourceManagementClient(credential=credential, subscription_id=subscription_id)


def subscription_client(credential) -> SubscriptionClient:
    return SubscriptionClient(credential=credential)
