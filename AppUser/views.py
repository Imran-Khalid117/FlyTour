from datetime import timedelta
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from AppUser.models import ApplicationUser
from AppUser.serializer import ApplicationUserSerializer
from FlyTour.general_functions import error_message, success_message


# Create your views here.
class PublicUserViewSet(viewsets.ModelViewSet):
    queryset = ApplicationUser.objects.all()
    serializer_class = ApplicationUserSerializer

    @action(detail=False, methods=['post'])
    def signup(self, request: Request, *args, **kwargs) -> Response:
        """
        In this method we are getting the email, username and password from calling function. This is sent in
        request body as a JSON object. Create method extracts the data provided process it and create a new user
        in the application. Where username is mandatory field in the user database.

        STEP 1: In this step we are extracting the user password from request object, hashing the object, and updating
        data object with new hashed password.

        STEP 2: we are creating user and saving it in the database.

        param:
        request: Request (Object) this pertains the request from the POST call from the calling application.
        **args: These are additional parameters
        **kwargs: These are additional - optional keyword parameters

        return:  rest_framework.response object with status of OK of failure to requesting source for this API
        """
        response_status = status.HTTP_400_BAD_REQUEST
        try:
            request_data = request.data
            serializer = self.get_serializer(data=request_data)
            if not serializer.is_valid(raise_exception=True):
                response_dictionary = error_message('An error has occurred with message ')
                return Response(response_dictionary, status=response_status)

            new_user = ApplicationUser.objects.create_user(**request_data)
            serializer = ApplicationUserSerializer(instance=new_user, fields=["id", "username", "email"])

            response_status = status.HTTP_201_CREATED
            response_dictionary = success_message('user created', serializer.data, response_status)
        except Exception as e:
            response_dictionary = error_message('An error has occurred with message ' + str(e))
        return Response(response_dictionary, status=response_status)

    @action(methods=['POST'], detail=False)
    def login(self, request: Request, *args, **kwargs) -> Response:
        """
       This method implements the login functionality for user to login. We are also generating the access token,
       refresh token and calculated access token expiry field data and saving it in database.

       In case if user is just created - this method will generate the new access token,
       refresh token and calculated access token expiry field data and saving it in database.

       In case if user has access token it will check the expiry and in case expiry datatime is expired i.e. after 6hrs
       it will again generate a new access token, refresh token and update the access token expiry field.

       In case if access token is not expired based on the datatime saved it will return the same access token,
       refresh token and will not update the expiry datetime field.

       param:
       request: Request (Object) this pertains the request from the POST call from the calling application.
       **args: These are additional parameters
       **kwargs: These are additional - optional keyword parameters
       return:  rest_framework.response object with status of OK of failure to requesting source for this API.
       """
        # Step 1: we are extracting "username" and "password" from request data
        request_data = request.data
        # Step 2: In this try catch block we are testing following things.
        # 1) We will check if access token is set and if it expired then generate a new token
        # 2) We will check if access token is not expired then return same access token, refresh token and expiry date.
        # 3) We will also verify if user exists in database.

        try:
            # Step 2.3 extracting user details from DB if not then raise exception
            user = ApplicationUser.objects.get(username=request_data.get("username"))
            # Step 2.1 checking if access token of a user is already set
            if user.access_token_expiry:
                time_delta = (user.access_token_expiry - timezone.now()).total_seconds() / 3600
                # if access token is set we authenticate the user.
                if check_password(request_data.get("password"), user.password):
                    # After authentication, we verify that if token is expired - in case it is expired we generate
                    # a new token and save it.
                    if time_delta < 0:
                        # Generate JWT tokens
                        refresh = RefreshToken.for_user(user)
                        access = AccessToken.for_user(user)
                        # Set expiration time for access token (e.g., 1 hour)
                        access_expiry = timezone.now() + timedelta(hours=6)
                        # Update user tokens and access token expiry
                        user.refresh_token = str(refresh)
                        user.access_token = str(access)
                        user.access_token_expiry = access_expiry
                        user.save()
                        response_status = status.HTTP_202_ACCEPTED
                        response_dictionary = success_message("User Authenticated and new Token generated",
                                                              data={'refresh': str(refresh), 'access': str(access),
                                                                    'access_token_expiry': user.access_token_expiry,
                                                                    })
                        return Response(response_dictionary, status=response_status)
                    else:
                        response_status = status.HTTP_202_ACCEPTED
                        response_dictionary = success_message("User Authenticated and new Token generated",
                                                              data={'refresh': str(user.refresh_token),
                                                                    'access': str(user.access_token),
                                                                    'access_token_expiry': user.access_token_expiry,
                                                                    })
                        return Response(response_dictionary, status=response_status)
                else:
                    response_status = status.HTTP_401_UNAUTHORIZED
                    response_dictionary = error_message('User not authenticated')
                    return Response(response_dictionary, status=response_status)
            else:
                # This block will fire if user access token expiry is empty, so we add new tokens and expiry date and
                # time.
                if check_password(request_data.get("password"), user.password):
                    # Generate JWT tokens
                    refresh = RefreshToken.for_user(user)
                    access = AccessToken.for_user(user)

                    # Set expiration time for access token (e.g., 1 hour)
                    access_expiry = timezone.now() + timedelta(hours=6)
                    # Update user tokens and access token expiry
                    user.refresh_token = str(refresh)
                    user.access_token = str(access)
                    user.access_token_expiry = access_expiry
                    user.save()

                    response_status = status.HTTP_202_ACCEPTED
                    response_dictionary = success_message("User Authenticated and new Token generated",
                                                          data={'refresh': str(refresh), 'access': str(access),
                                                                'access_token_expiry': user.access_token_expiry,
                                                                })
                    return Response(response_dictionary, status=response_status)
                else:
                    response_status = status.HTTP_401_UNAUTHORIZED
                    response_dictionary = error_message('User not authenticated')
                    return Response(response_dictionary, status=response_status)
        except ValueError as e:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    @permission_classes([IsAuthenticated])
    def logout(self, request: Request, *args, **kwargs) -> Response:
        """
            In this method we have implemented the logout functionality. This method will only be accessible
            if user is authenticated. This function receives username in request body and access token in request
            header.

            We filter out the user based on the username and extract the access token from the header. Access token
            is passed in header so that to make sure that user is authenticated user.

            Params:
            request: HTTP Request object - you can access all fields from this variable
            **args: These are additional parameters
            **kwargs: These are additional - optional keyword parameters

            return:  rest_framework.response object with status of OK of failure to requesting source for this API
        """
        request_data = request.data
        # extracting the user from database with respect to username provided in request body.
        user = ApplicationUser.objects.get(username=request_data.get("username"))
        jwt_token = None
        # We are checking here if application has provided access token if that is so then request header
        # will have Authorization key in request dictionary
        if 'Authorization' in request_data:
            # Get the JWT token from the request headers
            auth_header = request_data['Authorization']
            # Token should be in the format "Bearer <token>"
            jwt_token = auth_header.split()[1] if auth_header.startswith('Bearer') else None
        try:
            # If we have access token then we set all token and expiry field to none.
            if jwt_token:
                user.refresh_token = None
                user.access_token_expiry = None
                user.access_token = None
                user.save()
                response_status = status.HTTP_200_OK
                response_dictionary = success_message("Logout successful")
                return Response(response_dictionary, status=response_status)
            else:
                response_status = status.HTTP_400_BAD_REQUEST
                response_dictionary = error_message("Refresh token not provided")
                return Response(response_dictionary, status=response_status)
        except ObjectDoesNotExist:
            response_status = status.HTTP_404_NOT_FOUND
            response_dictionary = error_message("User does not exist")
            return Response(response_dictionary, status=response_status)
        except Exception as e:
            response_status = status.HTTP_401_UNAUTHORIZED
            response_dictionary = error_message("Invalid token" + str(e))
            return Response(response_dictionary, status=response_status)
