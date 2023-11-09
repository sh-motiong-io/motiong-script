import click

from group2 import commands as group2
from hello_world import hello_world
from spiders import commands as spiders
from jira_migration import commands as jira_migration


@click.group()
def entry_point():
    pass


entry_point.add_command(spiders.save_website_screenshots, 'save-website-screenshots')
entry_point.add_command(group2.foo)
entry_point.add_command(hello_world)
entry_point.add_command(jira_migration.jira_migration)

if __name__ == "__main__":
    entry_point()
