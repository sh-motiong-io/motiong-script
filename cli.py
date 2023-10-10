import click

from group2 import commands as group2
from hello_world import hello_world
from spiders import commands as spiders


@click.group()
def entry_point():
    pass


entry_point.add_command(spiders.printscreen)
entry_point.add_command(group2.foo)
entry_point.add_command(hello_world)

if __name__ == "__main__":
    entry_point()
