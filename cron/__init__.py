from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from urllib.parse import urlparse
import os
from cron.create_video_job import create_video


redis_url  = urlparse(os.getenv('REDIS_URL'))

print(redis_url.password, redis_url.port, redis_url.hostname)

executors = {
    'default' : ThreadPoolExecutor(10)
}

jobstores = {
    'default' : RedisJobStore(
        host=redis_url.hostname,
        port=redis_url.port,
        password=redis_url.password
    )
}

scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors)

scheduler.add_job(create_video, 'interval', minutes=1, id='create_video_job',
                  max_instances=1, replace_existing=True, misfire_grace_time=10)

