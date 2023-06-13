import datetime

from django.db import models
from django.utils import timezone

class RailVehicle(models.Model):
    reporting_mark = models.CharField(max_length=4)
    id_number = models.PositiveIntegerField()
    aar_type = models.CharField(max_length=2)
    cargo = models.CharField(max_length=12)
    loaded = models.BooleanField()
    location = models.PositiveIntegerField() # eventually a ForeignKey
    last_loaded_unloaded = models.PositiveIntegerField() # eventually a ForeignKey
    ready_for_pickup = models.BooleanField()
    img_url = models.URLField()

    class Meta:
        constraints: [ # type:ignore <- that oughta shut up VSCode
            models.UniqueConstraint(
                fields=['reporting_mark','id_number'], name='unique_reportingmark_idnumber_combination'
            )
        ]
    
    def __str__(self):
        return "%s %s - %s (%s)" % (self.reporting_mark,self.id_number,self.aar_type,self.cargo)

    def move(self,location):
        self.location = location

    def service(self):
        self.last_loaded_unloaded = self.location
        self.loaded = not self.loaded