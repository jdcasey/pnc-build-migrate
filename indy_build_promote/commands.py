import click
import os
from indy_build_promote.config import (load, DEFAULT_CONFIG_FILE)
from indy_build_promote.promote import promote_builds
from indy_build_promote.builds import list_builds

@click.command()
@click.option('-c', '--config', default=DEFAULT_CONFIG_FILE)
@click.argument('input_file')
@click.argument('progress_file')
@click.argument('fail_file')
def promote(config, input_file, progress_file, fail_file):
	cfg = load(config)
	promote_builds(cfg, input_file, progress_file, fail_file)

@click.command()
@click.option('-c', '--config', default=DEFAULT_CONFIG_FILE)
@click.argument('input_file')
@click.argument('progress_file')
@click.argument('repo_defs')
@click.argument('build_listing_dir')
def list_build_files(config, input_file, progress_file, repo_defs, build_listing_dir):
	cfg = load(config)
	list_builds(cfg, input_file, progress_file, repo_defs, build_listing_dir)
