from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Resume, Bookmark
from .serializers import (
    UserSerializer,
    ResumeSerializer,
    BookmarkSerializer,
    UserProfileSerializer
)
from .views import extract_pdf_text, extract_skills, load_jobs, combined_match_jobs
import logging

logger = logging.getLogger(__name__)

# Simple root endpoint that doesn't require authentication and ensures CSRF cookie is set
@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def api_root(request):
    """Root endpoint that sets CSRF cookie for the frontend"""
    return Response({
        "message": "API is working", 
        "authenticated": request.user.is_authenticated,
        "endpoints": {
            "login": "/api/users/login/",
            "register": "/api/users/register/",
            "profile": "/api/users/profile/",
            "resumes": "/api/resumes/",
            "bookmarks": "/api/bookmarks/",
        }
    })

class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Use Django's authenticate function
        user = authenticate(username=username, password=password)
        
        if user:
            # Get or create a token
            token, created = Token.objects.get_or_create(user=user)
            
            # Log the user in for session auth too
            login(request, user)
            
            logger.info(f"User {username} logged in successfully, token: {token.key}")
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email
            })
        
        logger.warning(f"Failed login attempt for user {username}")
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=request.data['username'],
                password=request.data['password'],
                email=request.data.get('email', '')
            )
            
            # Create token for the new user
            token, created = Token.objects.get_or_create(user=user)
            
            # Also log the user in for session auth
            login(request, user)
            
            logger.info(f"New user registered: {user.username}, token: {token.key}")
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email
            })
        
        logger.warning(f"Registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        # Delete the token if it exists
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        return Response({"detail": "Not logged in"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    @authentication_classes([TokenAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def profile(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch', 'put'])
    @authentication_classes([TokenAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def profile_update(self, request):
        try:
            user = request.user
            data = request.data
            
            # Update user fields
            if 'first_name' in data:
                user.first_name = data['first_name']
            if 'last_name' in data:
                user.last_name = data['last_name']
            if 'email' in data:
                user.email = data['email']
                
            # Update additional profile info (if you add a Profile model later)
            # This demonstrates extensibility for future features
            
            # Save the changes
            user.save()
            
            logger.info(f"Updated profile for user: {user.username}")
            return Response(UserProfileSerializer(user).data)
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    @authentication_classes([TokenAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def change_password(self, request):
        try:
            user = request.user
            current_password = request.data.get('current_password')
            new_password = request.data.get('new_password')
            
            # Validate inputs
            if not current_password or not new_password:
                return Response(
                    {'error': 'Both current and new password required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify current password
            if not user.check_password(current_password):
                return Response(
                    {'error': 'Current password is incorrect'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(new_password)
            user.save()
            
            # Update token since password changed
            Token.objects.filter(user=user).delete()
            token, _ = Token.objects.get_or_create(user=user)
            
            logger.info(f"Password changed for user: {user.username}")
            return Response({
                'message': 'Password updated successfully',
                'token': token.key
            })
        except Exception as e:
            logger.error(f"Error changing password: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class ResumeViewSet(viewsets.ModelViewSet):
    serializer_class = ResumeSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            logger.warning("Unauthenticated user tried to access resumes")
            return Resume.objects.none()
        return Resume.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        # Debug info
        logger.info(f"User: {request.user}, authenticated: {request.user.is_authenticated}")
        logger.info(f"Auth header: {request.META.get('HTTP_AUTHORIZATION', 'No Auth header')}")
        logger.info(f"Request FILES: {request.FILES}")
        
        # Check authentication explicitly
        if not request.user.is_authenticated:
            logger.warning("Unauthenticated user tried to upload resume")
            return Response(
                {'error': 'Authentication required'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error creating resume: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        logger.info(f"Creating resume for user: {self.request.user}")
        resume = serializer.save(user=self.request.user)
        if resume.file and resume.file.name.lower().endswith('.pdf'):
            try:
                text = extract_pdf_text(resume.file.path)
                resume.parsed_text = text
                skills = extract_skills(text)
                resume.skills = ", ".join(skills)
                resume.save()
                logger.info(f"Resume {resume.id} successfully processed")
            except Exception as e:
                logger.error(f"Error processing resume: {str(e)}")

    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        try:
            resume = self.get_object()
            jobs = load_jobs()
            matches = combined_match_jobs(resume, jobs)
            logger.info(f"Found {len(matches)} job matches for resume {resume.id}")
            return Response(matches)
        except Exception as e:
            logger.error(f"Error getting job matches: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class BookmarkViewSet(viewsets.ModelViewSet):
    serializer_class = BookmarkSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Bookmark.objects.none()
        return Bookmark.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Check if bookmark already exists
        existing = Bookmark.objects.filter(
            user=self.request.user,
            job_id=self.request.data['job_id']
        ).first()
        if not existing:
            serializer.save(user=self.request.user) 

# Add a JobViewSet to handle job-related endpoints
class JobViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]  # Allow anyone to view jobs
    
    def list(self, request):
        try:
            query = request.query_params.get('q', '')
            jobs = load_jobs()
            
            if query:
                # Filter jobs by query
                filtered_jobs = []
                query = query.lower()
                for job in jobs:
                    # Search in title, company, skills, description
                    if (query in job.get('title', '').lower() or
                        query in job.get('company', '').lower() or
                        any(query in skill.lower() for skill in job.get('skills', [])) or
                        query in job.get('description', '').lower()):
                        filtered_jobs.append(job)
                jobs = filtered_jobs
            
            logger.info(f"Returning {len(jobs)} jobs, query: '{query}'")
            return Response(jobs[:50])  # Limit to 50 jobs for performance
        except Exception as e:
            logger.error(f"Error listing jobs: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def matches(self, request):
        try:
            resume_id = request.query_params.get('resume_id')
            if not resume_id:
                return Response(
                    {'error': 'resume_id parameter is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if user has access to this resume
            resume = Resume.objects.get(id=resume_id)
            if request.user.is_authenticated and resume.user == request.user:
                jobs = load_jobs()
                matches = combined_match_jobs(resume, jobs)
                logger.info(f"Found {len(matches)} job matches for resume {resume_id}")
                return Response(matches)
            else:
                return Response(
                    {'error': 'Not authorized to access this resume'},
                    status=status.HTTP_403_FORBIDDEN
                )
        except Resume.DoesNotExist:
            return Response(
                {'error': f'Resume with id {resume_id} not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error matching jobs: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 