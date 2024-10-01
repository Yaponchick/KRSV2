from django.contrib import admin

from computers.models import Computer
from computers.models import VideoCard
from computers.models import Motherboard
from computers.models import Processor
from computers.models import PowerUnit


@admin.register(Computer)
class СomputerAdmin(admin.ModelAdmin):
    list_display=['id','model','price','computerV_FK','computerM_FK','computerP_FK','computerPU_FK']

@admin.register(VideoCard)
class VideoCardAdmin(admin.ModelAdmin):
    list_display=['id','model','price','numberFans','turboFrequency','memory_size']

@admin.register(Motherboard)
class MotherboardAdmin(admin.ModelAdmin):
    list_display=['id','model','price','compatibleKernels','processorPowerConnector','supportedMemory']
@admin.register(Processor)
class ProcessorAdmin(admin.ModelAdmin):
    list_display=['id','model','price','socket','chipset','frequency']

@admin.register(PowerUnit)
class PowerUnitAdmin(admin.ModelAdmin):
    list_display=['id','model','price','networkVoltage','coolingSystem','power']

