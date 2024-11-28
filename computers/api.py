from rest_framework.viewsets import GenericViewSet

from computers.models import Computer,VideoCard,Motherboard,Processor,PowerUnit

from rest_framework import mixins, serializers

from computers.serializers import ComputerSerializer, VideoCardSerializer, MotherboardSerializer, ProcessorSerializer, PowerUnitSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Count, Avg, Max, Min, Sum
from django.db.models.functions import Cast
from django.db.models import FloatField

class VideoCardViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = VideoCard.objects.all()
    serializer_class = VideoCardSerializer
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return VideoCard.objects.none()
        qs = super().get_queryset()
        
        if self.request.user.username != 'admin':
            qs = qs.filter(user=self.request.user)
            
        return qs
    
    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
        totalPrice = serializers.FloatField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, *args, **kwargs):
        stats = VideoCard.objects.aggregate(
            count=Count("*"),
            avg=Avg("price"),
            max=Max(Cast('price', FloatField())),
            min=Min(Cast('price', FloatField())),
            totalPrice=Sum("price")
        )
        
        print(f"Лог: {stats}")
        
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)


class MotherboardViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Motherboard.objects.all()
    serializer_class = MotherboardSerializer
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Motherboard.objects.none()
        qs = super().get_queryset()
        
        if self.request.user.username != 'admin':
            qs = qs.filter(user=self.request.user)
            
        return qs

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
        totalPrice = serializers.FloatField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, *args, **kwargs):
        stats = Motherboard.objects.aggregate(
            count=Count("*"),
            avg=Avg("price"),
            max=Max(Cast('price', FloatField())),
            min=Min(Cast('price', FloatField())),
            totalPrice=Sum("price")
        )
        
        print(f"Лог: {stats}")
        
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class ProcessorViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Processor.objects.all()
    serializer_class = ProcessorSerializer
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Processor.objects.none()
        qs = super().get_queryset()
        
        if self.request.user.username != 'admin':
            qs = qs.filter(user=self.request.user)
            
        return qs

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
        totalPrice = serializers.FloatField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, *args, **kwargs):
        stats = Processor.objects.aggregate(
            count=Count("*"),
            avg=Avg("price"),
            max=Max(Cast('price', FloatField())),
            min=Min(Cast('price', FloatField())),
            totalPrice=Sum("price")
        )
        
        print(f"Лог: {stats}")
        
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)

class PowerUnitViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = PowerUnit.objects.all()
    serializer_class = PowerUnitSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return PowerUnit.objects.none()
        qs = super().get_queryset()
        
        if self.request.user.username != 'admin':
            qs = qs.filter(user=self.request.user)
            
        return qs

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
        totalPrice = serializers.FloatField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, *args, **kwargs):
        stats = PowerUnit.objects.aggregate(
            count=Count("*"),
            avg=Avg("price"),
            max=Max(Cast('price', FloatField())),
            min=Min(Cast('price', FloatField())),
            totalPrice=Sum("price")
        )
        
        print(f"Лог: {stats}")
        
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)
    
class ComputersViewset(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Computer.objects.none()
        qs = super().get_queryset()
        
        if self.request.user.username != 'admin':
            qs = qs.filter(user=self.request.user)
            
        return qs

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
        totalPrice = serializers.FloatField()

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, *args, **kwargs):
        stats = Computer.objects.aggregate(
            count=Count("*"),
            avg=Avg("price"),
            max=Max(Cast('price', FloatField())),
            min=Min(Cast('price', FloatField())),
            totalPrice=Sum("price")
        )
        
        print(f"Лог: {stats}")
        
        serializer = self.StatsSerializer(instance=stats)
        return Response(serializer.data)
    
class UserViewSet(GenericViewSet): 
    @action(url_path="info", methods=["GET"], detail=False) 
    def get_info(self, request, *args, **kwargs): 
        data = { 
            "is_authenticated": request.user.is_authenticated 
        } 
        if request.user.is_authenticated: 
            data.update({ 
                "username": request.user.username, 
                "user_id": request.user.id 
            }) 
        return Response(data)