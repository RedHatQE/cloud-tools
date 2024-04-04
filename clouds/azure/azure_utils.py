from clouds.azure.session_clients import (
    get_aro_client,
    get_subscription_client,
)
from simple_logger.logger import get_logger

LOGGER = get_logger(name=__name__)


def get_aro_supported_versions(credential, subscription_id, region):
    return [
        aro_version.version
        for aro_version in get_aro_client(
            credential=credential, subscription_id=subscription_id
        ).open_shift_versions.list(location=region)
    ]


def get_azure_supported_regions(credential, subscription_id):
    return [
        region.name
        for region in get_subscription_client(credential=credential).subscriptions.list_locations(
            subscription_id=subscription_id
        )
    ]
