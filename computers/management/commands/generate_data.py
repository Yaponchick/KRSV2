from django.core.management.base import BaseCommand
from faker import Faker
from random import choice
from computers.models import Computer, VideoCard, Motherboard, Processor, PowerUnit
from random import choice, randint

class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])

        # Генерация блоков питания
        brands_power_units = ["Corsair", "Cooler Master", "Thermaltake", "Seasonic", "Be Quiet", "EVGA"]
        series_power_units = ["Platinum", "Gold", "Bronze", "Silver"]
        model_types_power_units = ["Pro", "X", "G", "M", "Elite"]

        for _ in range(3):
            brand = choice(brands_power_units)
            series_name = choice(series_power_units)
            model_type = choice(model_types_power_units)
            model_name = f"{brand} {series_name} {model_type}-{fake.random_int(min=500, max=1000)}W"

            PowerUnit.objects.create(
                model=model_name,
                price=f"{fake.random_int(min=2000, max=15000)}",
                networkVoltage=f"{fake.random_int(min=100, max=240)} В",
                coolingSystem=fake.random_element(elements=["Активное", "Пассивное", "Водяное"]),
                power=f"{fake.random_int(min=300, max=1000)} Вт",
                user=None
            )

        self.stdout.write(self.style.SUCCESS('Успешно сгенерированы записи для таблицы PowerUnit'))

        # Генерация процессоров
        brands_processors = ["Intel", "AMD"]
        series_processors = {
            "Intel": ["Core i3", "Core i5", "Core i7", "Core i9", "Pentium", "Celeron"],
            "AMD": ["Ryzen 3", "Ryzen 5", "Ryzen 7", "Ryzen 9", "Athlon", "Threadripper"]
        }
        sockets_processors = ["LGA1700", "AM5", "AM4", "LGA1200", "TR4"]
        chipsets_processors = ["Z790", "B760", "X670", "B550", "X570"]

        for _ in range(3):
            brand = choice(brands_processors)
            series_name = choice(series_processors[brand])
            model_name = f"{brand} {series_name} {fake.random_int(min=1000, max=9990)}X"

            Processor.objects.create(
                model=model_name,
                price=f"{fake.random_int(min=5000, max=70000)}",
                socket=choice(sockets_processors),
                chipset=choice(chipsets_processors),
                frequency=f"{fake.random_int(min=2000, max=5000)} МГц",
                user=None
            )

        self.stdout.write(self.style.SUCCESS('Успешно сгенерированы записи для таблицы Processor'))

        # Генерация материнских плат
        brands_motherboards = ["ASUS", "MSI", "Gigabyte", "ASRock", "Biostar"]
        series_motherboards = ["Prime", "TUF", "ROG Strix", "Aorus", "Phantom Gaming"]
        supported_memory_types = ["DDR4", "DDR5"]

        for _ in range(3):
            brand = choice(brands_motherboards)
            series_name = choice(series_motherboards)
            model_name = f"{brand} {series_name} {fake.random_int(min=100, max=999)}"

            Motherboard.objects.create(
                model=model_name,
                price=f"{fake.random_int(min=4000, max=30000)}",
                compatibleKernels=fake.random_element(elements=["x86", "ARM", "x64"]),
                processorPowerConnector=f"{fake.random_int(min=4, max=8)}-pin",
                supportedMemory=choice(supported_memory_types),
                user=None
            )

        self.stdout.write(self.style.SUCCESS('Успешно сгенерированы записи для таблицы Motherboard'))

        # Генерация видеокарт
        brands_video_cards = ["NVIDIA", "AMD", "Intel"]
        series_video_cards = {
            "NVIDIA": ["RTX 3050", "RTX 3060", "RTX 3070", "RTX 3080", "RTX 3090"],
            "AMD": ["RX 6500 XT", "RX 6600 XT", "RX 6700 XT", "RX 6800 XT", "RX 6900 XT"],
            "Intel": ["Arc A380", "Arc A750", "Arc A770"]
        }

        for _ in range(3):
            brand = choice(brands_video_cards)
            model_name = choice(series_video_cards[brand])
            number_fans = fake.random_int(min=1, max=3)
            turbo_frequency = f"{fake.random_int(min=1200, max=2500)} МГц"
            memory_size = f"{fake.random_int(min=4, max=24)} ГБ"

            VideoCard.objects.create(
                model=f"{brand} {model_name}",
                price=f"{fake.random_int(min=10000, max=150000)}",
                numberFans=number_fans,
                turboFrequency=turbo_frequency,
                memory_size=memory_size,
                user=None
            )

        self.stdout.write(self.style.SUCCESS('Успешно сгенерированы записи для таблицы VideoCard'))
        
        # Получение всех записей из связанных таблиц
        video_cards = list(VideoCard.objects.all())
        motherboards = list(Motherboard.objects.all())
        processors = list(Processor.objects.all())
        power_units = list(PowerUnit.objects.all())

        if not video_cards or not motherboards or not processors or not power_units:
            self.stdout.write(self.style.ERROR(
                'Необходимо предварительно сгенерировать данные (VideoCard, Motherboard, Processor, PowerUnit).'
            ))
            return

        # Генерация компьютеров
        for _ in range(3):
            video_card = choice(video_cards)
            motherboard = choice(motherboards)
            processor = choice(processors)
            power_unit = choice(power_units)

            model_name = f"{fake.word().capitalize()}-{randint(1000, 9999)}"
            
            try:
                total_price = (
                    int(video_card.price.split()[0]) +
                    int(motherboard.price.split()[0]) +
                    int(processor.price.split()[0]) +
                    int(power_unit.price.split()[0]) +
                    randint(5000, 20000)  # Дополнительная стоимость сборки
                )
            except (ValueError, IndexError) as e:
                self.stdout.write(self.style.ERROR(f"Ошибка обработки цены: {e}"))
                continue

            # Создаем объект
            Computer.objects.create(
                model=model_name,
                price=f"{total_price}",
                computerV_FK=video_card,
                computerM_FK=motherboard,
                computerP_FK=processor,
                computerPU_FK=power_unit,
                user=None
            )

        self.stdout.write(self.style.SUCCESS('Успешно сгенерированы записи для таблицы Computer'))
        
        
#python manage.py generate_data