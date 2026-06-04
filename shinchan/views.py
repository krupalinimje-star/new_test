import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# pyrefly: ignore [missing-import]
from rest_framework.response import Response
# pyrefly: ignore [missing-import]
from rest_framework.decorators import api_view
# pyrefly: ignore [missing-import]
from rest_framework_simplejwt.tokens import RefreshToken
from shinchan.models import FarmerProfile


@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            mobile = data.get("mobile_number")
            village = data.get("village_city")

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already taken"}, status=400)

            user = User.objects.create_user(username=username, password=password)
            FarmerProfile.objects.create(
                user=user,
                mobile_number=mobile,
                village_city=village
            )
            return JsonResponse({"message": "User registered successfully!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST allowed"}, status=405)


def home(request):
    # Check Authorization header
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'error': 'Authorization token missing'}, status=401)

    token_str = auth_header.split(' ')[1]

    try:
        # pyrefly: ignore [missing-import]
        from rest_framework_simplejwt.tokens import AccessToken
        token = AccessToken(token_str)
        user_id = token['user_id']
        user = User.objects.get(id=user_id)
    except Exception:
        return JsonResponse({'error': 'Invalid or expired token'}, status=401)

    # Get authenticated user's profile
    try:
        profile = FarmerProfile.objects.get(user=user)
        profile_data = {
            "mobile_number": profile.mobile_number,
            "village_city": profile.village_city
        }
    except FarmerProfile.DoesNotExist:
        profile_data = {}

    return JsonResponse({
        "authenticated_user": {
            "username": user.username,

            "profile": profile_data
        }
    })


@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({          # ✅ JSON response
            'status': 'success',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

    return JsonResponse({              # ✅ JSON response
        'status': 'error',
        'message': 'Invalid credentials'
    }, status=401)

