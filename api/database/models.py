from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import JSONB
import enum


class UserType(enum.Enum):
    ORGANIZATION = "ORGANIZATION"
    DEVELOPER = "DEVELOPER"
    ADMIN = "ADMIN"

class RequestStatus(enum.Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    PENDING = "PENDING"

class Funding():
    __tablename__ = 'fundings'

    id = Column(String, primary_key=True)
    amount = Column(Float)
    currency = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    userId = Column(String, ForeignKey('users.id'))

class APIToken():
    __tablename__ = 'api_tokens'

    id = Column(String, primary_key=True)
    tokenGr = Column(String)
    tokenCr = Column(String)
    tokenSm = Column(String)
    name = Column(String, nullable=True)
    verified = Column(Boolean, default=False)
    userId = Column(String, ForeignKey('users.id'))
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Request():
    __tablename__ = 'requests'

    id = Column(String, primary_key=True)
    status = Column(Enum(RequestStatus), default=RequestStatus.PENDING)
    parameters = Column(JSONB)
    request = Column(JSONB)
    response = Column(String)
    endpoint = Column(String)
    userId = Column(String, ForeignKey('users.id'))
    apiTokenId = Column(String, ForeignKey('api_tokens.id'), nullable=True)
    resourceTokenId = Column(String, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Usage():
    __tablename__ = 'usages'

    id = Column(String, primary_key=True, unique=True)
    tokens_used = Column(Integer)
    cost = Column(Float)
    requestId = Column(String, ForeignKey('requests.id'), unique=True, nullable=True)
    userId = Column(String, ForeignKey('users.id'))
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Resource():
    __tablename__ = 'resources'

    id = Column(String, primary_key=True)
    name = Column(String)
    description = Column(String, nullable=True)
    size = Column(Integer)
    handle = Column(String)
    type = Column(String)
    url = Column(String)
    userId = Column(String, ForeignKey('users.id'))
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Account():
    __tablename__ = 'accounts'

    userId = Column(String, ForeignKey('users.id'), primary_key=True)
    type = Column(String, primary_key=True)
    provider = Column(String, primary_key=True)
    providerAccountId = Column(String, primary_key=True)
    refresh_token = Column(String, nullable=True)
    access_token = Column(String, nullable=True)
    expires_at = Column(Integer, nullable=True)
    token_type = Column(String, nullable=True)
    scope = Column(String, nullable=True)
    id_token = Column(String, nullable=True)
    session_state = Column(String, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class Session():
    __tablename__ = 'sessions'

    sessionToken = Column(String, primary_key=True)
    userId = Column(String, ForeignKey('users.id'))
    expires = Column(DateTime)
    updated_at = Column(DateTime)
    created_at = Column(DateTime)

class User():
    __tablename__ = 'users'

    id = Column(String, primary_key=True)
    username = Column(String, nullable=True)
    phone = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True)
    type = Column(Enum(UserType), default=UserType.DEVELOPER)
    image = Column(String, default="https://dev.undrstnd-labs.com/placeholder.svg")
    verified = Column(Boolean, default=False)
    email_verified = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class VerificationToken():
    __tablename__ = 'verification_tokens'

    token = Column(String, primary_key=True)
    identifier = Column(String, primary_key=True)
    expires = Column(DateTime)
    passCode = Column(String, nullable=True)
    verificationUrl = Column(String, nullable=True)