import logging 
# setup 
logging.basicConfig(
    filename = "employee_app_logs.log",
    level = logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s"
)