from flask import (Blueprint, Response,
                   request, redirect, url_for, flash, render_template)


blueprint = Blueprint('join', __name__, url_prefix="/rooms")


@blueprint.route("/<code>/join", methods=['GET', 'POST'])
def get(code):
    if request.method == 'POST':
        name = request.form['name'].strip()

        if name:
            flash("Welcome, {}!".format(name), 'info')
            return redirect(url_for('rooms.detail', code=code, name=name))

        flash("A name is required.", 'error')

    return Response(render_template("join.html", code=code))
