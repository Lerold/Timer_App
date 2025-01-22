#!/usr/bin/env python
import click

# Import your app/db/User from the main Flask file
from app import db, User

@click.group()
def cli():
    """A command-line interface for managing users."""
    pass

@cli.command("create-user")
@click.option("--username", prompt=True, help="Username for the new user")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True, help="Password for the new user")
def create_user(username, password):
    """Create a new user."""
    existing = User.query.filter_by(username=username).first()
    if existing:
        click.echo(f"User '{username}' already exists!")
        return

    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    click.echo(f"User '{username}' created successfully.")

@cli.command("list-users")
def list_users():
    """List all users."""
    users = User.query.all()
    if not users:
        click.echo("No users found.")
        return

    click.echo("Existing users:")
    for user in users:
        click.echo(f" - {user.username} (id: {user.id})")

@cli.command("edit-user")
@click.option("--old-username", prompt=True, help="Current username")
@click.option("--new-username", default=None, help="New username (optional)")
@click.option("--new-password", default=None, hide_input=True, confirmation_prompt=True, help="New password (optional)")
def edit_user(old_username, new_username, new_password):
    """Rename or reset password for a user."""
    user = User.query.filter_by(username=old_username).first()
    if not user:
        click.echo(f"User '{old_username}' not found.")
        return

    # Update the username if given
    if new_username:
        # Check if the new name is taken
        if User.query.filter_by(username=new_username).first():
            click.echo(f"Cannot rename to '{new_username}' — already taken.")
            return
        user.username = new_username
        click.echo(f"Username changed from '{old_username}' to '{new_username}'")

    # Update the password if given
    if new_password:
        user.set_password(new_password)
        click.echo(f"Password updated for user '{user.username}'")

    db.session.commit()
    click.echo("Update complete.")

@cli.command("remove-user")
@click.option("--username", prompt=True, help="Username to delete")
def remove_user(username):
    """Remove a user entirely."""
    user = User.query.filter_by(username=username).first()
    if not user:
        click.echo(f"User '{username}' not found.")
        return

    # Proceed with deletion
    db.session.delete(user)
    db.session.commit()
    click.echo(f"User '{username}' has been removed.")

if __name__ == "__main__":
    cli()