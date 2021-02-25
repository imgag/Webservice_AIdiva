import subprocess
import os
import sys
from app.background_jobs import bp
from app import create_app
from app.email import mail_handler
from flask import render_template
import redis
from rq import Queue


app = create_app()
app.app_context().push()


listen = ["aidiva-tasks"]

redis_url = os.getenv("REDISTOGO_URL", "redis://localhost:6379")

conn = redis.from_url(redis_url)#config["REDIS_URL"])
aidiva_execution_queue = Queue("aidiva-tasks", connection=conn, default_timeout=3600)
#aidiva_mailing_queue = Queue("aidiva-mails", connection=conn, default_timeout=3600)


def create_and_queue_jobs(work_dir, result_folder, mail_address,vcf_file, hpo_file=None, exclusion_file=None, fam_file=None, fam_type="SINGLE"):
        job_execution = aidiva_execution_queue.enqueue(run_aidiva, args=(work_dir +  "/",result_folder,mail_address,vcf_file,hpo_file,fam_file,exclusion_file,fam_type,))
        #job_mail = aidiva_mailing_queue.enqueue(send_result_mail, args=(mail_address,work_dir,), depends_on=job_execution.get_id())
        #print(job_mail.get_id())


def run_aidiva(work_dir, result_folder, mail_address, vcf_file, hpo_file, fam_file, exclusion_file, fam_type):
        try:
                aidiva_command = "/var/www/html/AIdiva/venv/bin/python3 /var/www/html/AIdiva/tools/AIdiva-0.5/aidiva/run_annotation_and_AIdiva.py"
                aidiva_command = aidiva_command + " --config /var/www/html/AIdiva/tools/AIdiva-0.5/data/AIdiva_configuration_with_annotation.yml"
                aidiva_command = aidiva_command + " --vcf " + work_dir + vcf_file
                aidiva_command = aidiva_command + " --workdir " + work_dir

                if hpo_file is not None:
                    aidiva_command = aidiva_command + " --hpo_list " + work_dir + hpo_file
                
                if exclusion_file is not None:
                    aidiva_command = aidiva_command + " --gene_exclusion " + work_dir + exclusion_file
                
                if fam_type != "SINGLE":
                    if fam_file is not None:
                        aidiva_command = aidiva_command + " --family_file " + work_dir + fam_file
                        aidiva_command = aidiva_command + " --family_type " + fam_type
                    else:
                        aidiva_command = aidiva_command + " --family_type SINGLE"
                else:
                    aidiva_command = aidiva_command + " --family_type " + fam_type
                
                # start AIdiva pipeline to process the uploaded files
                subprocess.run(aidiva_command, shell=True, check=True)
                send_result_mail(mail_address, result_folder)
        except:
                app.logger.error("Unhandled exception", exc_info=sys.exc_info())
        finally:
                print("Job successfully finished!")


def send_result_mail(mail_address, work_dir):
        try:
                #send mail with link to the workfolder
                email_text = render_template("email/results.txt", result=str("https://download.imgag.de/ahboced1/aidiva_workdir/" + work_dir))
                email_html = render_template("email/results.html", result=str("https://download.imgag.de/ahboced1/aidiva_workdir/" + work_dir))
                mail_handler.send_mail("AIdiva-result", ("AIdiva Team", "no-reply@imgag.de"), [mail_address], email_text, email_html, None)
        except:
                app.logger.error("Unhandled exception", exc_info=sys.exc_info())
        finally:
                print("Job successfully finished!")

