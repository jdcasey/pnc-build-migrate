import click
import os
from indy_build_promote.config import (load, DEFAULT_CONFIG_FILE)
from indy_build_promote.promote import promote_builds
from indy_build_promote.builds import list_builds

@click.command()
@click.option('-c', '--config', default=DEFAULT_CONFIG_FILE, help='Alternative configuration file', type=click.File('r'))
@click.argument('input_file', required=True, help='File containing the list of hosted repositories whose content you wish to promote')
@click.argument('progress_file', required=True, help='File containing the list of repos successfully promoted')
@click.argument('fail_file', required=True, help='File containing the list of repos we could not promote')
def promote(config, input_file, progress_file, fail_file):
	cfg = load(config_file)
	promote_builds(cfg, input_file, progress_file, fail_file)

@click.command()
@click.option('-c', '--config', default=DEFAULT_CONFIG_FILE, help='Alternative configuration file', type=click.File('r'))
@click.argument('input_file', required=True, help='File containing the list of hosted repositories whose content you wish to list')
@click.argument('progress_file', required=True, help='File containing the list of repos successfully listed')
@click.argument('repo_defs', required=True, help='Directory where repository definition JSON is stored')
@click.argument('build_listing_dir', required=True, help='Directory where listings should be written')
def list_build_files(config, input_file, progress_file, repo_defs, build_listing_dir):
	cfg = load(config)
	list_builds(cfg, input_file, progress_file, repo_defs, build_listing_dir)
