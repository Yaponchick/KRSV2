from rest_framework.viewsets import GenericViewSet

from computers.models import Computer,VideoCard,Motherboard,Processor,PowerUnit

from rest_framework import mixins

from computers.serializers import ComputerSerializer, VideoCardSerializer, MotherboardSerializer, ProcessorSerializer, PowerUnitSerializer

from rest_framework.decorators import action
from rest_framework.response import Response

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