from django.db import models

class VideoCard(models.Model):
    model = models.TextField("Модель")
    price = models.TextField("Цена")
    numberFans = models.TextField("Количество вентиляторов")
    turboFrequency = models.TextField("Турбочастота")
    memory_size = models.TextField("Размер памяти")

    picture = models.ImageField("Изображение", null=True, upload_to="computers")

    class Meta:
        verbose_name = "Видеокарта"
        verbose_name_plural = "Видеокарты"

    def __str__(self) -> str:
        return self.model

class Motherboard(models.Model):
    model = models.TextField("Модель")
    price = models.TextField("Цена")
    compatibleKernels = models.TextField("Совместимые ядра")
    processorPowerConnector = models.TextField("Разъем питания процессора")
    supportedMemory = models.TextField("Поддерживаемая память")
    processors = models.ManyToManyField("Processor", verbose_name="Поддерживаемые процессоры")

    picture = models.ImageField("Изображение", null=True, upload_to="computers")


    class Meta:
        verbose_name = "Материнская плата"
        verbose_name_plural = "Материнские платы"
    
    def __str__(self) -> str:
        return self.model


class Processor(models.Model):
    model = models.TextField("Модель")
    price = models.TextField("Цена")
    socket = models.TextField("Сокет")
    chipset = models.TextField("Чипсет")
    frequency = models.TextField("Частота")

    class Meta:
        verbose_name = "Процессор"
        verbose_name_plural = "Процессоры"

    def __str__(self) -> str:
        return self.model


class PowerUnit(models.Model):
    model = models.TextField("Модель")
    price = models.TextField("Цена")
    networkVoltage = models.TextField("Сетевое напряжение")
    coolingSystem = models.TextField("Система охлаждения")
    power = models.TextField("Мощность")

    class Meta:
        verbose_name = "Блок питания"
        verbose_name_plural = "Блоки питания"

    def __str__(self) -> str:
        return self.model


class Computer(models.Model):
    model = models.TextField("Имя")
    price = models.TextField("Цена")

    computerV_FK = models.ForeignKey(VideoCard, on_delete=models.CASCADE, null=True, verbose_name="Видеокарта")
    computerM_FK = models.ForeignKey(Motherboard, on_delete=models.CASCADE,null=True, verbose_name="Материнская плата")
    computerP_FK = models.ForeignKey(Processor, on_delete=models.CASCADE,null=True, verbose_name="Процессор")
    computerPU_FK = models.ForeignKey(PowerUnit, on_delete=models.CASCADE,null=True, verbose_name="Блок питания")
    

    class Meta:
        verbose_name = "Компьютер"
        verbose_name_plural = "Компьютеры"
    
    def __str__(self) -> str:
        return self.model
    