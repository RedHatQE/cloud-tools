import os
import click
from clouds.azure.utils import nuke_all_azure_resources
from pyhelper_utils.runners import function_runner_with_pdb


@click.command()
@click.option(
    "--azure-tenant-id",
    help="Azure's managed identity tenant ID, needed for Azure API clients.",
    type=str,
    default=os.environ.get("AZURE_TENANT_ID"),
)
@click.option(
    "--azure-client-id",
    help="Azure's managed identity client ID, needed for Azure API clients.",
    type=str,
    default=os.environ.get("AZURE_CLIENT_ID"),
)
@click.option(
    "--azure-client-secret",
    help="Azure's managed identity client secret, needed for Azure API clients.",
    type=str,
    default=os.environ.get("AZURE_CLIENT_SECRET"),
)
@click.option(
    "--azure-subscription-id",
    help="Azure subscription ID, needed for Azure API clients.",
    type=str,
    default=os.environ.get("AZURE_SUBSCRIPTION_ID"),
)
def main(**kwargs):
    """
    Nuke all Azure cloud resources.
    """
    nuke_all_azure_resources(
        tenant_id=kwargs.get("azure_tenant_id"),
        client_id=kwargs.get("azure_client_id"),
        client_secret=kwargs.get("azure_client_secret"),
        subscription_id=kwargs.get("azure_subscription_id"),
    )


if __name__ == "__main__":
    function_runner_with_pdb(func=main)
