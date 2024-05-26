from django.contrib.auth.hashers import check_password
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
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
        data object with new hashed password. Note: When we create the user record using the create command it
        hashes the password automatically.

        STEP 2: we are creating user and saving it in the database.

        param:
        request: Request (Object) this pertains the request from the POST call from the calling application.
        **args: These are additional parameters
        **kwargs: These are additional - optional keyword parameters

        return:  rest_framework.response object with status of OK of failure to requesting source for this API
        """
        # Step 1:
        response_status = status.HTTP_400_BAD_REQUEST
        try:
            request_data = request.data
            serializer = self.get_serializer(data=request_data)
            if not serializer.is_valid(raise_exception=True):
                response_dictionary = error_message('An error has occurred with message ')
                return Response(response_dictionary, status=response_status)

            # Step 2:
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
       refresh token using JWT built in classes `TokenObtainPairView` and `TokenRefreshView`. We are calling
       these views as per our need from this view function.

       In case if user is just created and attempt login - this method will generate the new access token,
       refresh token. We are not saving the access and refresh token as they can be generated when ever
       user login. We have added the `SIMPLE_JWT` dictionary with default settings for access and refresh token,
       that regulates the expiry date and time.

       param:
       request: Request (Object) this pertains the request from the POST call from the calling application.
       **args: These are additional parameters
       **kwargs: These are additional - optional keyword parameters
       return:  rest_framework.response object with status of OK of failure to requesting source for this API.
       """
        # Step 1: we are extracting "username" and "password" from request data
        request_data = request.data
        # Step 2: In this try catch block we are testing following things.
        try:
            # Step 2.1 extracting user details from DB if not then raise exception
            user = ApplicationUser.objects.get(username=request_data.get("username"))

            # Authenticating the user
            if check_password(request_data.get("password"), user.password):
                # After authentication. We are now calling the view to generate the access and refresh token
                url = reverse('token_obtain_pair')
                # Building absolute path to the view as relative path does not work with this function.
                token_pair_url = request.build_absolute_uri(url)
                # Constructing the data input from the token generation view.
                data = {"username": user.username, "password": request_data.get("password")}
                # Sending the post request to the view.
                response = requests.post(token_pair_url, json=data)
                # Raise an exception for HTTP errors
                response.raise_for_status()

                response_status = status.HTTP_202_ACCEPTED
                response_dictionary = success_message("User Authenticated and new Token generated",
                                                      data={'token': response.json()})
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
        request_data = request.headers
        # extracting the user from database with respect to username provided in request header.
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
            # If we have access token then we log out the user.
            if jwt_token:
                response_status = status.HTTP_200_OK
                response_dictionary = success_message("Logout successful", data={user.username})
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
