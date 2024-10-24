from rest_framework import serializers

from computers import models
from computers.models import Computer,VideoCard,Motherboard,Processor,PowerUnit

class VideoCardSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)
    class Meta:
        model = VideoCard
        fields = ['id','model','price','numberFans','turboFrequency','memory_size','picture','user']

class MotherboardSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)
    class Meta:
        model = Motherboard
        fields = ['id','model','price','compatibleKernels','processorPowerConnector','supportedMemory','picture','user']

class ProcessorSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)
    class Meta:
        model = Processor
        fields = ['id','model','price','socket','chipset','frequency','user']

class PowerUnitSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)
    class Meta:
        model = PowerUnit
        fields = ['id','model','price','networkVoltage','coolingSystem','power','user']

class ComputerSerializer(serializers.ModelSerializer):
    def create(self, validated_data): 
        if 'request' in self.context:
            validated_data['user'] = self.context['request'].user
            
        return super().create(validated_data)
    
    computerV_FK = VideoCardSerializer(read_only=True)
    computerV_FK_1 = serializers.PrimaryKeyRelatedField(queryset=VideoCard.objects.all(), write_only=True, source='computerV_FK')

    computerM_FK = MotherboardSerializer(read_only=True)
    computerM_FK_1 = serializers.PrimaryKeyRelatedField(queryset=Motherboard.objects.all(), write_only=True, source='computerM_FK')
    
    computerP_FK = ProcessorSerializer(read_only=True)
    computerP_FK_1 = serializers.PrimaryKeyRelatedField(queryset=Processor.objects.all(), write_only=True, source='computerP_FK')

    computerPU_FK = PowerUnitSerializer(read_only=True)
    computerPU_FK_1 = serializers.PrimaryKeyRelatedField(queryset=PowerUnit.objects.all(), write_only=True, source='computerPU_FK')

    class Meta:
        model = Computer
        fields = ['id', 'model', 'price', 'computerV_FK', 'computerV_FK_1',
                  'computerM_FK', 'computerM_FK_1', 'computerP_FK', 
                  'computerP_FK_1', 'computerPU_FK', 'computerPU_FK_1','user']
