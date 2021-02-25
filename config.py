import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    #LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "localhost"
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    #MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    #MAIL_USERNAME = os.environ.get("MAIL_USER")
    #MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    REDIS_URL = os.environ.get("REDIS_URL") or "redis://localhost:6379"
    
    # defines the maximum file size (current: 100MB)
    MAX_CONTENT_LENGTH = 100*1024*1024
    VCF_EXTENSIONS = [".VCF", ".vcf", ".vcf.gz"]
    PED_EXTENSIONS = [".ped", ".PED"]
    TXT_EXTENSIONS = [".txt", "TXT"]
    UPLOAD_PATH = "/var/www/html/download/ahboced1/aidiva_workdir/"
