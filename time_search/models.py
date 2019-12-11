from django.db import models

class Guide(models.Model):
    collect_time = models.DateTimeField()
    departure_place = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_place = models.CharField(max_length=100)
    #line_name = models.CharField(max_length=100)
    line_id = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    delay_time = models.IntegerField()

    def __str__(self):
        #return str(self.collect_time)
        return '{0}---{1}'.format(self.collect_time, self.departure_time)
