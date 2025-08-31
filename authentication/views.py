# views.py مصحح

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .serializer import ProfileSerializer, ChangePasswordSerializer
from .models import Profile
from utils.cache.cache_utils import safe_cache_get, safe_cache_set, safe_cache_delete

# ------------------------------
# وظيفة مشتركة لحظر Refresh Token
# ------------------------------
def blacklist_refresh_token(token_str):
    try:
        if token_str:
            token = RefreshToken(token_str)
            token.blacklist()
    except TokenError:
        return False
    return True

# ------------------------------
# حظر جميع التوكنات الخاصة بالمستخدم
# ------------------------------
def logout_all_sessions(user):
    try:
        token = RefreshToken.for_user(user)
        token.blacklist()
    except TokenError:
        pass

# ------------------------------
# تسجيل مستخدم جديد
# ------------------------------
class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = ProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        register = serializer.save()
        safe_cache_delete("all_profiles")
        data = ProfileSerializer(register).data
        return Response({
            "message": "Account Created Successfully",
            "account": data
        }, status=status.HTTP_201_CREATED)

# ------------------------------
# عرض بيانات المستخدم الحالي
# ------------------------------
class CurrentUsersView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs):
        cache_key = f"user_{request.user.id}_profile"
        cache_data = safe_cache_get(cache_key)
        if cache_data:
            return Response({"source": "cache", "data": cache_data})

        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        safe_cache_set(cache_key, serializer.data, timeout=300)
        return Response({"profile": serializer.data}, status=status.HTTP_200_OK)

# ------------------------------
# تحديث الملف الشخصي
# ------------------------------
class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def patch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        safe_cache_delete("all_profiles")
        safe_cache_delete(f"user_{request.user.id}_profile")
        return Response({
            "message": "Profile updated successfully",
            "profile": serializer.data
        }, status=status.HTTP_200_OK)

# ------------------------------
# حذف الحساب الشخصي
# ------------------------------
class DeleteProfileView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def delete(self, request, *args, **kwargs):
        logout_all_sessions(request.user)
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            profile.delete()
        request.user.delete()
        safe_cache_delete("all_profiles")
        safe_cache_delete(f"user_{request.user.id}_profile")
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

# ------------------------------
# تغيير كلمة المرور
# ------------------------------
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def patch(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        safe_cache_delete("all_profiles")
        safe_cache_delete(f"user_{request.user.id}_profile")
        logout_all_sessions(user)
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

# ------------------------------
# تسجيل الخروج من جلسة واحدة
# ------------------------------
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not blacklist_refresh_token(refresh_token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
