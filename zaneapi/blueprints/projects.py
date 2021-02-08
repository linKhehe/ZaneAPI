import flask
from flask import current_app, request

from ..project import Project
from ..user import User
from .. import oauth

bp = flask.Blueprint("projects", __name__, url_prefix="/projects")


@bp.route("/")
@oauth.requires_user
def projects(user):
    return flask.render_template("projects.html", user=user, projects=user.get_projects())


@bp.route("/<int:project_id>/")
@oauth.requires_user
def view_project(user, project_id: int):
    project = Project(current_app.redis, project_id)

    if not user.has_project_permissions(project):
        return flask.abort(403)

    return flask.render_template(
        "view_project.html",
        user=user,
        project=project,
        owner=User(flask.current_app.redis, id=project.owner_id)
    )


@bp.route("/<int:project_id>/revoke")
@oauth.requires_user
def revoke_project_token(user, project_id: int):
    project = Project(flask.current_app.redis, project_id)

    if not user.has_project_permissions(project):
        return flask.abort(403)

    project.token.revoke()
    return flask.redirect(f"/projects/{project_id}/")


@bp.route("/<int:project_id>/generate")
@oauth.requires_user
def generate_project_token(user, project_id: int):
    project = Project(flask.current_app.redis, project_id)

    if not user.has_project_permissions(project):
        return flask.abort(403)

    project.token.generate()
    return flask.redirect(f"/projects/{project_id}/")


@bp.route("/<int:project_id>/delete")
@oauth.requires_user
def delete_project(user, project_id: int):
    project = Project(flask.current_app.redis, project_id)

    if not user.has_project_permissions(project):
        return flask.abort(403)

    project.delete()
    return flask.redirect("/projects")


@bp.route("/<int:project_id>/edit", methods=["GET", "POST"])
@oauth.requires_user
def edit_project(user, project_id: int):
    if request.method == "POST":
        project = Project(flask.current_app.redis, project_id)

        if not user.has_project_permissions(project):
            return flask.abort(403)

        project.edit(**request.form)
        return flask.redirect(f"/projects/{project_id}")

    project = Project(flask.current_app.redis, project_id)

    if not user.has_project_permissions(project):
        return flask.abort(403)

    return flask.render_template(
        "edit_project.html",
        user=user,
        project=project
    )


@bp.route("/create", methods=["GET", "POST"])
@oauth.requires_user
def projects_create(user):
    if request.method == "POST":
        project_id = flask.current_app.redis.incr("project_id")
        Project.create(
            flask.current_app.redis,
            project_id,
            name=request.form.get("name"),
            description=request.form.get("description"),
            owner_id=user.id
        )

        return flask.redirect(f"/projects/{project_id}/")

    return flask.render_template("projects_create.html", user=user)
