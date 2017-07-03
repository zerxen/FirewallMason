from firewall_rules.models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

class PortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Port
        #fields = ('id', 'version','owner')
        fields = '__all__'

class PortList(APIView):
    """
    List all Port objects
    
    get:
    Return a list of all the existing port.

    post:
    Create a new port instance using <code>application/json</code> data payload with following parameters:<br>
    - **vtip** to make fun<br>
    - **kreten** to target<br>
            
    """
    def get(self, request, format=None):
        promiscuous=self.request.GET.get('promiscuous', False)
        #ports = Port.objects.all()
        #ports = Port.getUseAllowedObjects(request.user)
        ports = Port.getPromiscuousObjects()
        serializer = PortSerializer(ports, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PortSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class PortDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Port.objects.get(pk=pk)
        except Port.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        port = self.get_object(pk)
        serializer = PortSerializer(port, many=False) #Port(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = PortSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
    
    
   