from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class ShortUrl(models.Model):
    short_url = models.CharField(max_length=20, null=True)
    default_url = models.CharField(max_length=800, null=False)
    mobile_url = models.CharField(max_length=800, null=True)
    tablet_url = models.CharField(max_length=800, null=True)
    created = models.DateTimeField(auto_now_add=True)
    redirect_count = models.IntegerField(default=0)

    def _create_short_url(self):
        num = ShortUrl.objects.all().count() + 1000
        num = num+1
        new_value = hex(num).split('x')[1]
        return new_value

    def __str__(self):
        return 'Short Url:{} Default Url:{}'.format(self.short_url, self.default_url)

    def save(self, *args, **kwargs):
        val = URLValidator()
        if val(self.default_url):
            raise Exception('ValidationError')
        if self.short_url is None:
            self.short_url = self._create_short_url()
        super(ShortUrl, self).save(*args, **kwargs)
