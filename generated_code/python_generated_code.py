from twilio.rest import Client
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
class OTPVerificationView(APIView):
    def post(self, request, format=None):
        try:
            twilio_client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            phone_number = request.data.get('phoneNumber')
            verification_code = request.data.get('verificationCode')
            if verification_code: 
                verification_check = twilio_client.verify \
                    .services(settings.TWILIO_VERIFY_SERVICE_SID) \
                    .verification_checks \
                    .create(to=phone_number, code=verification_code)
                if verification_check.status == 'approved':
                    return Response({'message': 'Verification successful'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Verification failed'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                verification = twilio_client.verify \
                    .services(settings.TWILIO_VERIFY_SERVICE_SID) \
                    .verifications \
                    .create(to=phone_number, channel='sms')
                return Response({'message': 'OTP sent successfully', 'sid': verification.sid}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)