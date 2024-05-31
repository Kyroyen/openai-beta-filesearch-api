from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import UploadSerializer, ChatQuerySerializer
from .models import UserFiles

class UploadAPIView(APIView):
    serializer_class = UploadSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        user = request.user
        return Response(data = {"username" : user.username})
    
    def post(self, request, *args, **kwargs):
        
        file = request.data["file_uploaded"]
        
        usf = UserFiles(file = file, user = request.user)

        try:
            usf.save()
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        return Response(data = {"file_id":usf.file_name}, status=200)
    

class ChatAPIView(APIView):
    serializer_class = ChatQuerySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, *args, **kwargs):

        serializer = ChatQuerySerializer(data = request.data)
        serializer.get_openai_fileid(request.user)
        data = serializer.make_query()
        return Response(data = data, status = 200)
        

