import logging
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.utils.password import hash_password
from app.models.users import User
from typing import List, Optional
from app.schemas.users import CreateUserInput, UpdateUserInput

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Create a New User
def create_user(user: CreateUserInput, db: Session):
    logger.info(f"Attempting to create new user with username: {user.username}")
    
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        logger.warning(f"Registration failed - Email already exists: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        logger.warning(f"Registration failed - Username already exists: {user.username}")
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = User(
        name=user.name,
        username=user.username,
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    logger.info(f"Successfully created user: {user.username}")
    return db_user

# Read All Users (Paginated)
def read_users(skip: int, limit: int, db: Session) -> List[User]:
    logger.info(f"Fetching users list - skip: {skip}, limit: {limit}")
    users = db.query(User).offset(skip).limit(limit).all()
    logger.info(f"Retrieved {len(users)} users")
    return users

# Read User by ID
def read_user(user_id: int, db: Session) -> Optional[User]:
    logger.info(f"Attempting to fetch user with ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.warning(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    logger.info(f"Successfully retrieved user: {user.username}")
    return user

# Update User
def update_user(user_id: int, user: UpdateUserInput, current_user: User, db: Session) -> User:
    logger.info(f"Attempting to update user with ID: {user_id}")
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        logger.warning(f"Update failed - User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.username != db_user.username:
        logger.warning(f"Update failed - Unauthorized access attempt by user: {current_user.username}")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")

    # Log which fields are being updated
    update_fields = []
    
    # Only update if the field is not None and not an empty string
    if user.name is not None and user.name.strip() != "":
        update_fields.append("name")
        db_user.name = user.name
    if user.username is not None and user.username.strip() != "":
        update_fields.append("username")
        db_user.username = user.username
    if user.email is not None and user.email.strip() != "":
        update_fields.append("email")
        db_user.email = user.email
    if user.phone is not None and user.phone.strip() != "":
        update_fields.append("phone")
        db_user.phone = user.phone
    if user.password and user.password.strip() != "":
        update_fields.append("password")
        db_user.password = hash_password(user.password)
    
    if not update_fields:
        logger.info(f"No fields to update for user: {db_user.username}")
        return db_user
        
    logger.info(f"Updating fields for user {db_user.username}: {', '.join(update_fields)}")

    db.commit()
    db.refresh(db_user)
    
    logger.info(f"Successfully updated user: {db_user.username}")
    return db_user

# Delete User
def delete_user(user_id: int, db: Session) -> User:
    logger.info(f"Attempting to delete user with ID: {user_id}")
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        logger.warning(f"Delete failed - User not found with ID: {user_id}")
        raise HTTPException(status_code=404, detail="User not found")

    username = db_user.username
    db.delete(db_user)
    db.commit()
    
    logger.info(f"Successfully deleted user: {username}")
    return db_user