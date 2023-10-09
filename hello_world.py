import click


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', default='Your name',
              help='The person to greet.')
def hello_world(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")
    click.echo("Hello world!")


if __name__ == "__main__":
    hello_world()
