from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests


CHATBOTS = {
    'statbot': {
        "url": "https://api.leastcube.com/bot748",
        "password": 1234
    },

    'medbot': {
        "url": "",
        "password": "",
    },

}

class APIView(APIView):
    """
    API endpoint for interacting with the chatbots.
    """
    def get(self, request):
        """
        Send a message to the chatbots api and return the response to client.

        Expected Query Parameters:
        - message : string 
        - chatbot : string

        Response Parameters:
        - method : which is GET
        - url : url of api endpoint
        - message: the message to send to the chatbot
        - response : the response of chatbot to the client
        """

        message = request.GET.get('message')
        chatbot = request.GET.get('chatbot')

        if not message:
            return Response({"error": "enter valid message"}, status=status.HTTP_400_BAD_REQUEST)

        if chatbot not in CHATBOTS.keys():
            return Response({"error": "enter valid chatbot name"}, status=status.HTTP_400_BAD_REQUEST)

        CHATBOT_DATA = CHATBOTS[chatbot]

        # should be deleted
        if chatbot == 'medbot' : 
            return Response({
                "method":"GET",
                "url": request.build_absolute_uri(),
                "chatbot": chatbot,
                "message": message,
                "response": message},
                status=status.HTTP_200_OK)
        # till here

        result = requests.get(CHATBOT_DATA["url"], params={'message':message, "password":CHATBOT_DATA["password"]})

        if result.status_code == 200:
            response = result.json()['response']
            return Response({
                "method":"GET",
                "url": request.build_absolute_uri(),
                "chatbot": chatbot,
                "message": message,
                "response": response},
                status=status.HTTP_200_OK)
        return Response({"error":"chatbot api unavailable",}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
