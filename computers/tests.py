from django.test import TestCase
from model_bakery import baker
from computers.models import Computer, VideoCard, Motherboard, Processor, PowerUnit
from rest_framework.test import APIClient
from rest_framework import serializers, viewsets
from rest_framework.test import APITestCase

    # ----- Computer CRUD -----
class ComputerCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_computer(self):
        video_card = baker.make("VideoCard")
        motherboard = baker.make("Motherboard")
        processor = baker.make("Processor")
        power_unit = baker.make("PowerUnit")

        r = self.client.post("/api/computers/", {
            "model": "СуперПК2000", 
            "price": "2000000", 
            "computerV_FK_1": video_card.id,
            "computerM_FK_1": motherboard.id,
            "computerP_FK_1": processor.id,
            "computerPU_FK_1": power_unit.id
        })
        assert r.status_code == 201

    def test_get_computer(self):
        computer = baker.make("Computer")
        r = self.client.get('/api/computers/')
        data = r.json()

        assert computer.model == data[0]['model']
        assert computer.id == data[0]['id']
        assert computer.price == data[0]['price']
        assert len(data) == 1

    def test_delete_computer(self):
        computers = baker.make("Computer", 10)
        r = self.client.get('/api/computers/')
        data = r.json()
        assert len(data) == 10

        computer_id_to_delete = computers[3].id
        self.client.delete(f'/api/computers/{computer_id_to_delete}/')

        r = self.client.get('/api/computers/')
        data = r.json()
        assert len(data) == 9
        assert computer_id_to_delete not in [i['id'] for i in data]

    def test_update_Computer(self):
        video_card = baker.make("VideoCard", model="GTX 3080", price="120000", numberFans="3", turboFrequency="1.8 GHz", memory_size="10 GB")
        motherboard = baker.make("Motherboard", model="ASUS ROG", price="30000")
        processor = baker.make("Processor", model="Intel i9", price="50000")
        power_unit = baker.make("PowerUnit", model="Corsair 750W", price="15000")

        computer = baker.make("Computer", model="Gaming PC", price="200000",
                            computerV_FK=video_card,
                            computerM_FK=motherboard,
                            computerP_FK=processor,
                            computerPU_FK=power_unit)

        r = self.client.get(f"/api/computers/{computer.id}/")
        data = r.json()
        assert data['model'] == computer.model
        assert data['price'] == computer.price

        update_data = {
            "model": "High-End Gaming PC",
            "price": computer.price,
            "computerV_FK": video_card.id,
            "computerM_FK": motherboard.id,
            "computerP_FK": processor.id,
            "computerPU_FK": power_unit.id,
        }

        r = self.client.patch(f"/api/computers/{computer.id}/", update_data)
        updated_data = r.json()

        assert updated_data['model'] == "High-End Gaming PC"
        assert updated_data['price'] == computer.price

        computer.refresh_from_db()
        assert computer.model == "High-End Gaming PC"
        assert computer.price == updated_data['price']


    # ----- VideoCard CRUD -----
class VideoCardCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_VideoCard(self):
        r = self.client.post("/api/VideoCard/", {
            "model": "GTX 3080",
            "price": "120000",
            "numberFans": "3",
            "turboFrequency": "1.8 GHz",
            "memory_size": "10 GB"
        })
        assert r.status_code == 201
        data = r.json()
        assert data['model'] == "GTX 3080"
        assert data['price'] == "120000"
        assert data['numberFans'] == "3"
        assert data['turboFrequency'] == "1.8 GHz"
        assert data['memory_size'] == "10 GB"

    def test_get_VideoCard(self):
        video_card = baker.make("VideoCard")
        r = self.client.get('/api/VideoCard/')
        data = r.json()

        assert video_card.model == data[0]['model']
        assert video_card.id == data[0]['id']
        assert video_card.price == data[0]['price']
        assert video_card.numberFans == data[0]['numberFans']
        assert video_card.turboFrequency == data[0]['turboFrequency']
        assert video_card.memory_size == data[0]['memory_size']
        assert len(data) == 1

    def test_update_VideoCard(self):
        video_card = baker.make("VideoCard", model="GTX 3080", price="120000", numberFans="3", turboFrequency="1.8 GHz", memory_size="10 GB")

        r = self.client.get(f"/api/VideoCard/{video_card.id}/")
        data = r.json()
        assert data['model'] == video_card.model
        assert data['price'] == video_card.price
        assert data['numberFans'] == video_card.numberFans
        assert data['turboFrequency'] == video_card.turboFrequency
        assert data['memory_size'] == video_card.memory_size

        update_data = {
            "model": "GTX 3090",
            "price": video_card.price,
            "numberFans": video_card.numberFans,
            "turboFrequency": video_card.turboFrequency,
            "memory_size": video_card.memory_size
        }

        r = self.client.patch(f"/api/VideoCard/{video_card.id}/", update_data)
        updated_data = r.json()

        assert updated_data['model'] == "GTX 3090"
        assert updated_data['price'] == video_card.price
        assert updated_data['numberFans'] == video_card.numberFans
        assert updated_data['turboFrequency'] == video_card.turboFrequency
        assert updated_data['memory_size'] == video_card.memory_size

        video_card.refresh_from_db()
        assert video_card.model == "GTX 3090"
        assert video_card.price == updated_data['price']
        assert video_card.numberFans == updated_data['numberFans']
        assert video_card.turboFrequency == updated_data['turboFrequency']
        assert video_card.memory_size == updated_data['memory_size']


    # ----- Motherboard CRUD -----
class MotherboardCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_Motherboard(self):
        r = self.client.post("/api/Motherboard/", {
            "model": "ASUS ROG STRIX",
            "price": "20000",
            "compatibleKernels": "Intel, AMD",
            "processorPowerConnector": "8-pin",
            "supportedMemory": "DDR4"
        })
        assert r.status_code == 201
        data = r.json()
        assert data['model'] == "ASUS ROG STRIX"
        assert data['price'] == "20000"
        assert data['compatibleKernels'] == "Intel, AMD"
        assert data['processorPowerConnector'] == "8-pin"
        assert data['supportedMemory'] == "DDR4"

    def test_get_Motherboard(self):
        motherboard = baker.make("Motherboard")
        r = self.client.get('/api/Motherboard/')
        data = r.json()

        assert motherboard.model == data[0]['model']
        assert motherboard.id == data[0]['id']
        assert motherboard.price == data[0]['price']
        assert motherboard.compatibleKernels == data[0]['compatibleKernels']
        assert motherboard.processorPowerConnector == data[0]['processorPowerConnector']
        assert motherboard.supportedMemory == data[0]['supportedMemory']
        assert len(data) == 1

    def test_update_Motherboard(self):
        motherboard = baker.make("Motherboard", model="ASUS ROG STRIX", price="20000", compatibleKernels="Intel, AMD", processorPowerConnector="8-pin", supportedMemory="DDR4")

        r = self.client.get(f"/api/Motherboard/{motherboard.id}/")
        data = r.json()
        assert data['model'] == motherboard.model
        assert data['price'] == motherboard.price
        assert data['compatibleKernels'] == motherboard.compatibleKernels
        assert data['processorPowerConnector'] == motherboard.processorPowerConnector
        assert data['supportedMemory'] == motherboard.supportedMemory

        update_data = {
            "model": "MSI B450 TOMAHAWK",
            "price": motherboard.price,
            "compatibleKernels": motherboard.compatibleKernels,
            "processorPowerConnector": motherboard.processorPowerConnector,
            "supportedMemory": motherboard.supportedMemory
        }

        r = self.client.patch(f"/api/Motherboard/{motherboard.id}/", update_data)
        updated_data = r.json()

        assert updated_data['model'] == "MSI B450 TOMAHAWK"
        assert updated_data['price'] == motherboard.price
        assert updated_data['compatibleKernels'] == motherboard.compatibleKernels
        assert updated_data['processorPowerConnector'] == motherboard.processorPowerConnector
        assert updated_data['supportedMemory'] == motherboard.supportedMemory

        motherboard.refresh_from_db()
        assert motherboard.model == "MSI B450 TOMAHAWK"
        assert motherboard.price == updated_data['price']
        assert motherboard.compatibleKernels == updated_data['compatibleKernels']
        assert motherboard.processorPowerConnector == updated_data['processorPowerConnector']
        assert motherboard.supportedMemory == updated_data['supportedMemory']

    # ----- Processor CRUD -----
class ProcessorCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_Processor(self):
        r = self.client.post("/api/Processor/", {
            "model": "Intel Core i9",
            "price": "50000",
            "socket": "LGA 1200",
            "chipset": "Z490",
            "frequency": "3.5 GHz"
        })
        assert r.status_code == 201
        data = r.json()
        assert data['model'] == "Intel Core i9"
        assert data['price'] == "50000"
        assert data['socket'] == "LGA 1200"
        assert data['chipset'] == "Z490"
        assert data['frequency'] == "3.5 GHz"

    def test_get_Processor(self):
        processor = baker.make("Processor")
        r = self.client.get('/api/Processor/')
        data = r.json()

        assert processor.model == data[0]['model']
        assert processor.id == data[0]['id']
        assert processor.price == data[0]['price']
        assert processor.socket == data[0]['socket']
        assert processor.chipset == data[0]['chipset']
        assert processor.frequency == data[0]['frequency']
        assert len(data) == 1

    def test_update_Processor(self):
        processor = baker.make("Processor", model="Intel Core i9", price="50000", socket="LGA 1200", chipset="Z490", frequency="3.5 GHz")

        r = self.client.get(f"/api/Processor/{processor.id}/")
        data = r.json()
        assert data['model'] == processor.model
        assert data['price'] == processor.price
        assert data['socket'] == processor.socket
        assert data['chipset'] == processor.chipset
        assert data['frequency'] == processor.frequency

        update_data = {
            "model": "AMD Ryzen 9",
            "price": processor.price,
            "socket": processor.socket,
            "chipset": processor.chipset,
            "frequency": processor.frequency
        }

        r = self.client.patch(f"/api/Processor/{processor.id}/", update_data)
        updated_data = r.json()

        assert updated_data['model'] == "AMD Ryzen 9"
        assert updated_data['price'] == processor.price
        assert updated_data['socket'] == processor.socket
        assert updated_data['chipset'] == processor.chipset
        assert updated_data['frequency'] == processor.frequency

        processor.refresh_from_db()
        assert processor.model == "AMD Ryzen 9"
        assert processor.price == updated_data['price']
        assert processor.socket == updated_data['socket']
        assert processor.chipset == updated_data['chipset']
        assert processor.frequency == updated_data['frequency']


    # ----- PowerUnitr CRUD -----
class PowerUnitCRUDTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_PowerUnit(self):
        r = self.client.post("/api/PowerUnit/", {
            "model": "Corsair RM750",
            "price": "12000",
            "networkVoltage": "220V",
            "coolingSystem": "Active",
            "power": "750W"
        })
        assert r.status_code == 201
        data = r.json()
        assert data['model'] == "Corsair RM750"
        assert data['price'] == "12000"
        assert data['networkVoltage'] == "220V"
        assert data['coolingSystem'] == "Active"
        assert data['power'] == "750W"

    def test_get_PowerUnit(self):
        power_unit = baker.make("PowerUnit")
        r = self.client.get('/api/PowerUnit/')
        data = r.json()

        assert power_unit.model == data[0]['model']
        assert power_unit.id == data[0]['id']
        assert power_unit.price == data[0]['price']
        assert power_unit.networkVoltage == data[0]['networkVoltage']
        assert power_unit.coolingSystem == data[0]['coolingSystem']
        assert power_unit.power == data[0]['power']
        assert len(data) == 1

    def test_update_PowerUnit(self):
        power_unit = baker.make("PowerUnit", model="Corsair RM750", price="12000", networkVoltage="220V", coolingSystem="Active", power="750W")

        r = self.client.get(f"/api/PowerUnit/{power_unit.id}/")
        data = r.json()
        assert data['model'] == power_unit.model
        assert data['price'] == power_unit.price
        assert data['networkVoltage'] == power_unit.networkVoltage
        assert data['coolingSystem'] == power_unit.coolingSystem
        assert data['power'] == power_unit.power

        update_data = {
            "model": "Seasonic Focus Gold 750",
            "price": power_unit.price,
            "networkVoltage": power_unit.networkVoltage,
            "coolingSystem": power_unit.coolingSystem,
            "power": power_unit.power
        }

        r = self.client.patch(f"/api/PowerUnit/{power_unit.id}/", update_data)
        updated_data = r.json()

        assert updated_data['model'] == "Seasonic Focus Gold 750"
        assert updated_data['price'] == power_unit.price
        assert updated_data['networkVoltage'] == power_unit.networkVoltage
        assert updated_data['coolingSystem'] == power_unit.coolingSystem
        assert updated_data['power'] == power_unit.power

        power_unit.refresh_from_db()
        assert power_unit.model == "Seasonic Focus Gold 750"
        assert power_unit.price == updated_data['price']
        assert power_unit.networkVoltage == updated_data['networkVoltage']
        assert power_unit.coolingSystem == updated_data['coolingSystem']
        assert power_unit.power == updated_data['power']