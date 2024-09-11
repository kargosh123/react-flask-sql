import sqlite3

import click
from flask import Blueprint, current_app, Flask, g, typing as ft, request as req


bp = Blueprint("db", __name__, url_prefix="/db")


def dict_factory(cursor: sqlite3.Cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory

    return g.db


def close_db(e: ft.TeardownCallable | None = None):
    del e

    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@bp.route("/list_items", methods=["GET"])
def list_items():
    db = get_db()
    if not db:
        return {}

    items = db.execute("SELECT * FROM items").fetchall()
    return items


@bp.route("/add_item", methods=["POST"])
def add_item():
    db = get_db()
    if not db:
        return {"success": False}

    db.execute("INSERT INTO items DEFAULT VALUES")
    db.commit()
    return {"success": True}


@bp.route("/list_values", methods=["GET"])
def list_all_values():
    db = get_db()
    if not db:
        return {}

    values: list[dict[str, int]] = db.execute("SELECT * FROM values_store").fetchall()
    value_map = {value["item_id"]: [] for value in values}
    for value in values:
        value_map[value["item_id"]].append(value["value"])
    return value_map


@bp.route("/list_values/<int:item_id>", methods=["GET"])
def list_values(item_id):
    db = get_db()
    if not db:
        return {}

    values = db.execute(
        "SELECT * FROM values_store WHERE item_id = ?", (item_id,)
    ).fetchall()
    return values


@bp.route("/add_value/<int:item_id>/<float:value>", methods=["POST"])
def add_value(item_id, value):
    db = get_db()
    if not db:
        return {"success": False}

    db.execute(
        "INSERT INTO values_store (item_id, value) VALUES (?, ?)", (item_id, value)
    )
    db.commit()
    return {"success": True}


@bp.route("/delete_item/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    db = get_db()
    if not db:
        return {"success": False}

    db.execute("DELETE FROM values_store WHERE item_id = ?", (item_id,))
    db.execute("DELETE FROM items WHERE id = ?", (item_id,))
    db.commit()
    return {"success": True}


@bp.route("/delete_value/<int:value_id>", methods=["DELETE"])
def delete_value(value_id):
    db = get_db()
    if not db:
        return {"success": False}

    db.execute("DELETE FROM values_store WHERE id = ?", (value_id,))
    db.commit()
    return {"success": True}

@bp.route("/bulk_add_items", methods=["POST"])
def bulk_add_items():
    db = get_db()
    if not db:
        return {"success": False}
    for item in req.json:
        add_item()
        get_id_key = db.execute("SELECT MAX(id) as id FROM items").fetchone()['id']
        for value in item:
            add_value(get_id_key, value)
    db.commit()
    return {"success": True}