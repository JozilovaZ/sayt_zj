from celery import shared_task
from django.core.cache import cache
from .models import News


@shared_task
def cache_news_data():
    latest_new=News.published.first()
    if latest_new:
        latest_news = News.published.exclude(id=latest_new.id)[:4]
    else:
        latest_news=News.published.all()

    sport_news=News.published.filter(category__name="Sport")
    teno_news=News.published.filter(category__name="Texnologiya")
    mahaliy_news=News.published.filter(category__name="Mahalliy")
    xorij_news=News.published.filter(category__name="Xorij")

    cache.set('latest_new', latest_new, 60)
    cache.set('latest_news', latest_news, 60)
    cache.set('sport_news', sport_news, 60)
    cache.set('teno_news', teno_news, 60)
    cache.set('mahaliy_news', mahaliy_news, 60)
    cache.set('xorij_news', xorij_news, 60)

