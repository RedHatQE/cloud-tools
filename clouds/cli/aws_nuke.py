import click
import shutil
from pyhelper_utils.runners import function_runner_with_pdb
from clouds.aws.utilities.delete_aws_resources import clean_aws_resources
from clouds.aws.aws_utils import set_and_verify_aws_credentials, aws_region_names


@click.command()
@click.option(
    "--aws-regions",
    help="""
        \b
        Comma-separated string of AWS regions to delete resources from.
        If not provided will iterate over all regions.
        """,
    required=False,
)
@click.option(
    "--all-aws-regions",
    help="""
        \b
        Run on all AWS regions.
        """,
    is_flag=True,
)
def main(aws_regions: str, all_aws_regions: bool):
    """
    Nuke all AWS cloud resources in given/all regions
    """

    if all_aws_regions:
        _aws_regions = aws_region_names()
    elif aws_regions:
        _aws_regions = aws_regions.split(",")
    else:
        click.echo("Either pass --all-aws-regions or --aws-regions to run cleanup")
        raise click.Abort()

    if not shutil.which("cloud-nuke"):
        click.echo("cloud-nuke is not installed; install from" " https://github.com/gruntwork-io/cloud-nuke")
        raise click.Abort()

    set_and_verify_aws_credentials(region_name=_aws_regions[0])

    clean_aws_resources(aws_regions=_aws_regions)


if __name__ == "__main__":
    function_runner_with_pdb(func=main)
