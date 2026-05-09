"""
Authentication Service for Nova Nexus
Handles user login, validation, and session management
"""
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class User:
    """User data model"""
    def __init__(self, username: str, email: str, password: str, role: str = "Operator"):
        self.username = username
        self.email = email
        self.password_hash = self._hash_password(password)
        self.role = role
        self.created_at = datetime.now()
        self.is_authenticated = False

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        """Verify password against hash"""
        return self.password_hash == self._hash_password(password)


class AuthService:
    """Authentication service for managing users and sessions"""
    
    # Default demo users
    DEMO_USERS = {
        "operator@factory.com": User("Operator", "operator@factory.com", "password", "Manufacturing"),
        "manager@factory.com": User("Manager", "manager@factory.com", "manager123", "Supervisor"),
        "supervisor@factory.com": User("Supervisor", "supervisor@factory.com", "supervisor123", "Quality Control"),
    }

    def __init__(self):
        """Initialize auth service with demo users"""
        self.users: Dict[str, User] = self.DEMO_USERS.copy()
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.login_attempts: Dict[str, int] = {}
        self.max_attempts = 5
        self.lockout_duration = 300  # 5 minutes

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dict with status, message, and session token if successful
        """
        # Check if account is locked
        if email in self.login_attempts and self.login_attempts[email] >= self.max_attempts:
            return {
                "success": False,
                "error": "ACCOUNT_LOCKED",
                "message": "Too many failed login attempts. Please try again in 5 minutes."
            }

        # Validate inputs
        if not email or not password:
            return {
                "success": False,
                "error": "INVALID_INPUT",
                "message": "Email and password are required"
            }

        # Check if user exists
        if email not in self.users:
            # Track failed attempt
            self.login_attempts[email] = self.login_attempts.get(email, 0) + 1
            return {
                "success": False,
                "error": "INVALID_CREDENTIALS",
                "message": "Invalid email or password"
            }

        user = self.users[email]

        # Verify password
        if not user.verify_password(password):
            # Track failed attempt
            self.login_attempts[email] = self.login_attempts.get(email, 0) + 1
            attempts_left = self.max_attempts - self.login_attempts[email]
            
            return {
                "success": False,
                "error": "INVALID_CREDENTIALS",
                "message": f"Invalid email or password ({attempts_left} attempts remaining)",
                "attempts_left": attempts_left
            }

        # Reset login attempts on successful login
        self.login_attempts[email] = 0

        # Create session
        session_token = self._generate_token(email)
        self.sessions[session_token] = {
            "email": email,
            "username": user.username,
            "role": user.role,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=24)
        }

        return {
            "success": True,
            "message": "Login successful",
            "token": session_token,
            "user": {
                "username": user.username,
                "email": email,
                "role": user.role,
                "avatar": user.username[0].upper()
            }
        }

    def logout(self, token: str) -> Dict[str, Any]:
        """
        Logout user by invalidating session
        
        Args:
            token: Session token
            
        Returns:
            Success/failure status
        """
        if token in self.sessions:
            del self.sessions[token]
            return {"success": True, "message": "Logged out successfully"}
        
        return {"success": False, "message": "Invalid session"}

    def verify_session(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify if session is valid
        
        Args:
            token: Session token
            
        Returns:
            Session data if valid, None otherwise
        """
        if token not in self.sessions:
            return None

        session = self.sessions[token]
        
        # Check if session expired
        if datetime.now() > session["expires_at"]:
            del self.sessions[token]
            return None

        return session

    def register_user(self, username: str, email: str, password: str, role: str = "Operator") -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            username: Username
            email: User email
            password: User password
            role: User role
            
        Returns:
            Success/failure status
        """
        # Validate inputs
        if not all([username, email, password]):
            return {
                "success": False,
                "error": "INVALID_INPUT",
                "message": "All fields are required"
            }

        # Check if email already exists
        if email in self.users:
            return {
                "success": False,
                "error": "USER_EXISTS",
                "message": "Email already registered"
            }

        # Create new user
        self.users[email] = User(username, email, password, role)
        
        return {
            "success": True,
            "message": "User registered successfully"
        }

    def _generate_token(self, email: str) -> str:
        """Generate unique session token"""
        import uuid
        return f"{email}:{uuid.uuid4().hex}"


# Global auth service instance
auth_service = AuthService()
