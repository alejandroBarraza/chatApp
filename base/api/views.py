from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]
    if request.method == 'GET':
        return Response(routes)
        
@api_view(['GET'])
def get_rooms(request):
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializers = RoomSerializer(rooms, many = True)
        return Response(serializers.data)

@api_view(['GET'])
def get_room(request,pk):
    if request.method == 'GET':
        room = Room.objects.get(id = pk)
        serializers = RoomSerializer(room, many = False)
        return Response(serializers.data)
    

            
