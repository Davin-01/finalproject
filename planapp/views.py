from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import StudyPlan, Event
import json


from .Serializers import PlanSerializer
from .auth import CookieAuthentication

# from .serializers import PlanSerializer, UserSerializer

class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        email = request.data.get('email')

        print(username, first_name, last_name, password)
        # Check for missing fields
        if not all([username, first_name, last_name, password, email]):
            return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for existing username or email
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

class SigninView(TokenObtainPairView):
    """
    Handles user login using JWT and stores the access token in an HTTP-only cookie.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Get tokens
        refresh = serializer.validated_data["refresh"]
        access = serializer.validated_data["access"]

        # Prepare response
        response = Response({
            "refresh": refresh,
            "access": access
        }, status=status.HTTP_200_OK)

        # Set cookies
        response.set_cookie(
            key="access_token",
            value=access,
            httponly=False,  # Prevent JavaScript access
            secure=True,    # Use this in production (requires HTTPS)
            samesite="None"  # Helps mitigate CSRF attacks
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=False,
            secure=True,
            samesite="None"
        )
        return response

class PlanView(APIView):
    authentication_classes = [CookieAuthentication]
    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.method = None
        self.body = None

    def get(self, request):
        user = request.user
        plans = StudyPlan.objects.filter(user=user)
        serializer = PlanSerializer(plans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        serializer = PlanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)  # Associate the plan with the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def add_view(request):
    # Handle POST request (for adding new event)
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            time = data.get("time")

            if not title or not time:
                return JsonResponse({"error": "Invalid input, 'title' and 'time' are required"}, status=400)

            # Create the event
            event = Event.objects.create(title=title, time=time)

            # Return created event details
            return JsonResponse({
                "id": event.id,
                "title": event.title,
                "time": event.time
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    # Handle GET request (to retrieve all events)
    elif request.method == "GET":
        try:
            data = json.loads(request.body)
            title = data.get("title")
            events = Event.objects.filter(title=title)  # Retrieve events for the logged-in user
            events_data = [{"id": event.id, "title": event.title, "time": event.time} for event in events]

            return JsonResponse(events_data, safe=False, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid method"}, status=405)
