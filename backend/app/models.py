from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    BUSINESS_OWNER = "business_owner"
    ADMIN = "admin"


class SubscriptionPlan(str, Enum):
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"


class BusinessCategory(str, Enum):
    YOGA = "yoga"
    PILATES = "pilates"
    CYCLING = "cycling"
    STRENGTH = "strength"
    DANCE = "dance"
    BOXING = "boxing"
    RUNNING = "running"
    MARTIAL_ARTS = "martial_arts"
    BARBERSHOP = "barbershop"
    SPA = "spa"
    PARTY = "party"


class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: str
    role: UserRole
    credits: int
    subscription_plan: Optional[SubscriptionPlan] = None
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


# Business schemas
class BusinessBase(BaseModel):
    name: str
    description: str
    category: BusinessCategory
    address: str
    city: str
    country: str
    phone: str
    email: EmailStr
    image_url: Optional[str] = None
    rating: float = Field(default=0.0, ge=0, le=5)


class BusinessCreate(BusinessBase):
    owner_id: Optional[str] = None


class BusinessResponse(BusinessBase):
    id: str
    owner_id: str
    is_active: bool
    created_at: datetime


class BusinessUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    image_url: Optional[str] = None


# Service schemas
class ServiceBase(BaseModel):
    name: str
    description: str
    duration_minutes: int = Field(ge=15, le=480)
    credits_cost: int = Field(ge=1, le=100)
    price_cop: int = Field(default=0, ge=0)
    max_capacity: int = Field(default=1, ge=1)


class ServiceCreate(ServiceBase):
    business_id: str


class ServiceResponse(ServiceBase):
    id: str
    business_id: str
    is_active: bool
    created_at: datetime
    price_cop: int = 0


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_minutes: Optional[int] = None
    credits_cost: Optional[int] = None
    max_capacity: Optional[int] = None
    is_active: Optional[bool] = None


# Schedule schemas
class ScheduleSlot(BaseModel):
    id: str
    service_id: str
    date: str
    start_time: str
    end_time: str
    available_spots: int
    total_spots: int


class ScheduleCreate(BaseModel):
    service_id: str
    date: str
    start_time: str
    end_time: str


# Booking schemas
class BookingBase(BaseModel):
    service_id: str
    schedule_slot_id: str


class BookingCreate(BookingBase):
    pass


class BookingResponse(BaseModel):
    id: str
    user_id: str
    service_id: str
    schedule_slot_id: str
    status: BookingStatus
    credits_used: int
    created_at: datetime
    service_name: Optional[str] = None
    business_name: Optional[str] = None
    date: Optional[str] = None
    start_time: Optional[str] = None


# Subscription schemas
class SubscriptionInfo(BaseModel):
    plan: SubscriptionPlan
    credits_per_month: int
    price_usd: float
    features: List[str]


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[str] = None
