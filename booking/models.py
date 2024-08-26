from django.conf import settings
from django.db import models
from django.utils import timezone


class Store(models.Model):
    """店舗"""
    name = models.CharField('店名', max_length=255)

    def __str__(self):
        return self.name

class BookInfo(models.Model):
    """蔵書データ"""
    name= models.CharField('表示名', max_length=50, default='デフォルト値')
    ISBN = models.CharField('ISBN', max_length=50, default='デフォルト値')
    author = models.CharField('著者', max_length=50, default='デフォルト値')
    publisher = models.CharField('出版社', max_length=50, default='デフォルト値')
    cover = models.ImageField('表紙画像', upload_to='covers/', null=True, blank=True)
    Division = models.CharField('支社', max_length=50, default='デフォルト値')
    shelf = models.CharField('棚', max_length=50, default='デフォルト値')
    section = models.CharField('セクション', max_length=50, default='デフォルト値')
    
    def __str__(self):
        return self.name
    
    def get_cover_url(self):
        if self.cover and hasattr(self.cover, 'url'):
            return self.cover.url
        else:
            return settings.STATIC_URL + 'default_cover.jpg'
        
from django.utils import timezone

class Staff(models.Model):
    """予約情報"""
    staff = models.ForeignKey('self', on_delete=models.CASCADE, related_name='related_staff', null=True)
    start = models.DateTimeField('開始時間', default=timezone.now)
    end = models.DateTimeField('終了時間', default=timezone.now)
    name = models.CharField('予約者名', max_length=255)
    memo = models.TextField('メモ', blank=True, null=True)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.name} {start} ~ {end} {self.staff}'

    def clean(self):
        if self.start >= self.end:
            raise ValidationError('開始時間は終了時間よりも前に設定してください')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['staff', 'start', 'end'], name='unique_schedule'),
        ]

class Schedule(models.Model):
    """予約スケジュール."""
    start = models.DateTimeField('開始時間')
    end = models.DateTimeField('終了時間')
    name = models.CharField('予約者名', max_length=255)
    staff = models.ForeignKey('Staff', verbose_name='占いスタッフ', on_delete=models.CASCADE)

    def __str__(self):
        start = timezone.localtime(self.start).strftime('%Y/%m/%d %H:%M:%S')
        end = timezone.localtime(self.end).strftime('%Y/%m/%d %H:%M:%S')
        return f'{self.name} {start} ~ {end} {self.staff}'
