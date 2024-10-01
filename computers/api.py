from rest_framework.viewsets import GenericViewSet

from computers.models import Computer,VideoCard,Motherboard,Processor,PowerUnit

from rest_framework import mixins

from computers.serializers import ComputerSerializer, VideoCardSerializer, MotherboardSerializer, ProcessorSerializer, PowerUnitSerializer

class VideoCardViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = VideoCard.objects.all()
    serializer_class = VideoCardSerializer

class MotherboardViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Motherboard.objects.all()
    serializer_class = MotherboardSerializer

class ProcessorViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer

class PowerUnitViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = PowerUnit.objects.all()
    serializer_class = PowerUnitSerializer

class ComputersViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer