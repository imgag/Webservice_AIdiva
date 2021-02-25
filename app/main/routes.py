import os
import uuid
from flask import abort, current_app, render_template, flash, request, redirect, url_for
from app.main import bp
from app.background_jobs import tasks
from werkzeug.utils import secure_filename


@bp.route("/")
@bp.route("/index")
def index():
        return render_template("index.html", title="Webservice")


def validate_file_content():
        return None


@bp.route("/file", methods=["GET", "POST"])
def file_upload():
        if request.method == "POST":
                vcf_file = request.files["vcfFile"]
                hpo_file = request.files["hpoFile"]
                geneExclusion_file = request.files["geneExclusion"]
                family_file = request.files["familyFile"]
                family_type = request.form.get("familyType")
                mail_address = request.form.get("inputEmail")

                vcf_filename = secure_filename(vcf_file.filename)
                hpo_filename = secure_filename(hpo_file.filename)
                geneExclusion_filename = secure_filename(geneExclusion_file.filename)
                family_filename = secure_filename(family_file.filename)
        
                vcf_file_ext = os.path.splitext(vcf_filename)[1]
                hpo_file_ext = os.path.splitext(hpo_filename)[1]
                geneExclusion_file_ext = os.path.splitext(geneExclusion_filename)[1]
                family_file_ext = os.path.splitext(family_filename)[1]

                result_folder = str(uuid.uuid4().hex)
                work_dir = current_app.config["UPLOAD_PATH"] + "/" + result_folder

                os.mkdir(work_dir)
                os.chmod(work_dir, 0o755)

                # only this file is mandatory
                if vcf_file.filename != "":
                        if vcf_file_ext not in current_app.config["VCF_EXTENSIONS"]:
                                abort(400)                      
                        vcf_file.save(work_dir +  "/" + vcf_filename)

                if hpo_file.filename != "":
                        if hpo_file_ext not in current_app.config["TXT_EXTENSIONS"]:
                                abort(400)
                        hpo_file.save(work_dir +  "/" + hpo_filename)

                if geneExclusion_file.filename != "":
                        if geneExclusion_file_ext not in current_app.config["TXT_EXTENSIONS"]:
                                abort(400)
                        geneExclusion_file.save(work_dir +  "/" + geneExclusion_filename)

                if family_file.filename != "":
                        if family_file_ext not in current_app.config["PED_EXTENSIONS"]:
                                abort(400)
                        family_file.save(work_dir +  "/" + family_filename)

                tasks.create_and_queue_jobs(work_dir +  "/", result_folder, mail_address, vcf_filename, hpo_file=hpo_filename, exclusion_file=geneExclusion_filename, fam_file=family_filename, fam_type=family_type)

        return render_template("file_handling/file_upload.html", title="File Upload")

