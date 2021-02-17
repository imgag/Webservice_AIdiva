from app.errors import bp


@bp.app_errorhandler(400)
def invalid_file_upload():
    return render_template("errors/400.html"), 400


@bp.app_errorhandler(404)
def invalid_file_upload():
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(413)
def invalid_file_upload():
    return render_template("errors/413.html"), 413


@bp.app_errorhandler(500)
def invalid_file_upload():
    return render_template("errors/500.html"), 500
