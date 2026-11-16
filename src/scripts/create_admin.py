import argparse
from getpass import getpass

from sqlalchemy.exc import IntegrityError

from src.app import create_app
from src.app.extensions import db
from src.app.models import User


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an administrator account.")
    parser.add_argument("username")
    args = parser.parse_args()

    password = getpass("Password: ")
    password_confirm = getpass("Confirm password: ")

    if len(password) < 8:
        raise SystemExit("Password must be at least 8 characters long.")
    if password != password_confirm:
        raise SystemExit("Passwords do not match.")

    app = create_app(load_models=False)
    with app.app_context():
        if User.query.filter_by(username=args.username).first():
            raise SystemExit("This username is already taken.")

        admin = User(username=args.username, role="admin")
        admin.set_password(password)
        db.session.add(admin)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise SystemExit("Could not create the administrator account.")

    print(f"Administrator account '{args.username}' created.")


if __name__ == "__main__":
    main()
