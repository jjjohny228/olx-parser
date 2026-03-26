from apscheduler.schedulers.asyncio import AsyncIOScheduler

def schedule_func(func):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=func, trigger="interval", minutes=1)
    scheduler.start()
