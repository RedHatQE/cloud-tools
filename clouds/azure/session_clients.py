from azure.identity import ClientSecretCredential
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.redhatopenshift import AzureRedHatOpenShiftClient


def get_azure_credentials(tenant_id, client_id, client_secret):
    return ClientSecretCredential(
        tenant_id=tenant_id,
        client_id=client_id,
        client_secret=client_secret,
    )


def get_aro_client(credential, subscription_id):
    return AzureRedHatOpenShiftClient(credential=credential, subscription_id=subscription_id)


def get_network_client(credential, subscription_id):
    return NetworkManagementClient(credential=credential, subscription_id=subscription_id)


def get_resource_client(credential, subscription_id):
    return ResourceManagementClient(credential=credential, subscription_id=subscription_id)


def get_subscription_client(credential):
    return SubscriptionClient(credential=credential)
