#!/usr/bin/env python
import os
import schedule
import time
import logging


logging.basicConfig(filename='/var/log/confd.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
logger = logging.getLogger('jobs')


def log_job(job_func):
    logger.info("Running {}".format(job_func.__name__))
    job_func()


def trigger_confd():
    os.system('sudo /opt/confd/bin/confd -backend consul -node consul-endpoint-xyz.example.com:443 -scheme https -onetime')
    logger.info("Confd job is started!!")


schedule.every(60).seconds.do(log_job, trigger_confd)


def main():
    logger.info('Starting schedule loop')
    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    main()
