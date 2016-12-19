from flask import (Blueprint, Response,
                   request, flash, redirect, url_for, render_template)

from ._utils import call
from .import api_rooms


blueprint = Blueprint('options', __name__, url_prefix="/rooms")


@blueprint.route("/<code>/options")
def index(code):
    name = request.args.get('name', "")

    link = url_for('rooms.detail', code=code, _external=True)
    html = render_template("options.html", link=link, name=name, code=code)

    return Response(html)


@blueprint.route("/<code>/options", methods=['POST'])
def action(code):
    name = request.args.get('name', "")

    if 'rename' in request.form:
        new_name = request.form['name'].strip()

        if new_name:
            flash("Name changed: {}".format(new_name), 'info')
            return redirect(url_for('rooms.detail', code=code, name=new_name))

        else:
            flash("A name is required.", 'danger')
            return redirect(url_for('.index', code=code, name=name))

    elif 'next' in request.form:
        call(api_rooms.next_speaker, code=code, name=name, force=True)

    elif 'clear' in request.form:
        call(api_rooms.clear, code)

    elif 'delete' in request.form:
        call(api_rooms.delete, code)

    return redirect(url_for('rooms.detail', code=code, name=name))
