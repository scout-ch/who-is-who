wsgi_app = "app.app:create_app()"
timeout = 180

accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s "%(r)s" %(s)s %(b)s %(D)sus'
