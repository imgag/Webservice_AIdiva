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
aidiva_mailing_queue = Queue("aidiva-mails", connection=conn, default_timeout=3600)


def create_and_queue_jobs(work_dir, mail_address,vcf_file, hpo_file=None, exclusion_file=None, fam_file=None, fam_type="SINGLE"):
	job_execution = aidiva_execution_queue.enqueue(run_aidiva, args=(work_dir +  "/",mail_address,vcf_file,))
	print(job_execution.get_id())
	job_mail = aidiva_mailing_queue.enqueue(send_result_mail, args=(mail_address,work_dir,), depends_on=job_execution.get_id())
	print(job_mail.get_id())


def run_aidiva(work_dir, mail_address, vcf_file, hpo_file=None, fam_file=None, exclusion_file=None, fam_type="SINGLE"):
	try:
		# start AIdiva pipeline to process the uploaded files
		subprocess.run("/usr/bin/python3 /mnt/data/AIdiva/aidiva/run_annotation_and_AIdiva.py --vcf " + work_dir + vcf_file + " --workdir " + work_dir + " --config /mnt/data/AIdiva/data/AIdiva_configuration_with_annotation.yaml", shell=True, check=True)
		print(work_dir)
		send_result_mail(mail_address, work_dir)
	except:
		app.logger.error("Unhandled exception", exc_info=sys.exc_info())
	finally:
		print("Job successfully finished!")


def send_result_mail(mail_address, work_dir):
	try:
		#send mail with link to the workfolder
		email_text = render_template("email/results.txt", result=work_dir)
		email_html = render_template("email/results.html", result=work_dir)
		mail_handler.send_mail("AIdiva-result", "aidiva@localhost.com", [mail_address], email_text, email_html, None)
			
		print(mail_address)
	except:
		app.logger.error("Unhandled exception", exc_info=sys.exc_info())
	finally:
		print("Job successfully finished!")
