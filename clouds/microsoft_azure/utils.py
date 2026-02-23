from azure.mgmt.redhatopenshift import AzureRedHatOpenShiftClient
from azure.mgmt.subscription import SubscriptionClient
from simple_logger.logger import get_logger

LOGGER = get_logger(name="microsoft-azure-utils")


def get_aro_supported_versions(aro_client: AzureRedHatOpenShiftClient, region: str) -> list[str]:
    supported_versions: list[str] = [
        aro_version.version for aro_version in aro_client.open_shift_versions.list(location=region)
    ]
    LOGGER.info(f"ARO supported versions: {supported_versions}")
    return supported_versions


def get_azure_supported_regions(subscription_client: SubscriptionClient, subscription_id: str) -> list[str]:
    supported_regions: list[str] = [
        region.name for region in subscription_client.subscriptions.list_locations(subscription_id=subscription_id)
    ]
    LOGGER.info(f"ARO supported regions: {supported_regions}")
    return supported_regions
