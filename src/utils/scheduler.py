from apscheduler.schedulers.asyncio import AsyncIOScheduler

def schedule_func(func):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=func, trigger="interval", seconds=20)
    scheduler.start()
