from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from datetime import timedelta

from app.models import (
    UserCreate, UserLogin, UserResponse, UserUpdate, Token,
    BusinessCreate, BusinessResponse, BusinessUpdate, BusinessCategory,
    ServiceCreate, ServiceResponse, ServiceUpdate,
    ScheduleSlot, BookingCreate, BookingResponse,
    SubscriptionPlan, SubscriptionInfo
)
from app.database import db
from app.auth import (
    get_password_hash, verify_password, create_access_token,
    get_current_user, get_current_user_optional, ACCESS_TOKEN_EXPIRE_MINUTES
)

app = FastAPI(
    title="FastPass Col API",
    description="API para la plataforma de bienestar y fitness tipo ClassPass para Colombia",
    version="1.0.0"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Configuración de planes de suscripción - Solo un plan inicial
SUBSCRIPTION_PLANS = {
    SubscriptionPlan.BASIC: SubscriptionInfo(
        plan=SubscriptionPlan.BASIC,
        credits_per_month=20,
        price_usd=99000,  # $99,000 COP
        features=[
            "20 créditos mensuales",
            "Acceso a gimnasios, spas, yoga y más",
            "Reservas fáciles desde la app",
            "Cancela cuando quieras"
        ]
    )
}


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


# ==================== ENDPOINTS DE AUTENTICACIÓN ====================

@app.post("/api/auth/register", response_model=Token, tags=["Autenticación"])
async def registrar(user_data: UserCreate):
    """Registrar un nuevo usuario"""
    existing_user = db.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.model_dump()
    user_dict["password"] = hashed_password
    
    user = db.create_user(user_dict)
    
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/auth/login", response_model=Token, tags=["Autenticación"])
async def iniciar_sesion(credentials: UserLogin):
    """Iniciar sesión con correo y contraseña"""
    user = db.get_user_by_email(credentials.email)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    
    access_token = create_access_token(
        data={"sub": user["id"], "email": user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/auth/me", response_model=UserResponse, tags=["Autenticación"])
async def obtener_perfil(current_user: dict = Depends(get_current_user)):
    """Obtener perfil del usuario actual"""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        phone=current_user.get("phone"),
        role=current_user["role"],
        credits=current_user["credits"],
        subscription_plan=current_user.get("subscription_plan"),
        created_at=current_user["created_at"]
    )


@app.put("/api/auth/me", response_model=UserResponse, tags=["Autenticación"])
async def actualizar_perfil(update_data: UserUpdate, current_user: dict = Depends(get_current_user)):
    """Actualizar perfil del usuario actual"""
    user_id = current_user["id"]
    if update_data.full_name:
        db.users[user_id]["full_name"] = update_data.full_name
    if update_data.phone:
        db.users[user_id]["phone"] = update_data.phone
    
    updated_user = db.get_user_by_id(user_id)
    return UserResponse(
        id=updated_user["id"],
        email=updated_user["email"],
        full_name=updated_user["full_name"],
        phone=updated_user.get("phone"),
        role=updated_user["role"],
        credits=updated_user["credits"],
        subscription_plan=updated_user.get("subscription_plan"),
        created_at=updated_user["created_at"]
    )


# ==================== ENDPOINTS DE SUSCRIPCIONES ====================

@app.get("/api/subscriptions", response_model=List[SubscriptionInfo], tags=["Suscripciones"])
async def obtener_planes():
    """Obtener todos los planes de suscripción disponibles"""
    return list(SUBSCRIPTION_PLANS.values())


@app.post("/api/subscriptions/{plan}", response_model=UserResponse, tags=["Suscripciones"])
async def suscribirse(plan: SubscriptionPlan, current_user: dict = Depends(get_current_user)):
    """Suscribirse a un plan (pago simulado)"""
    plan_info = SUBSCRIPTION_PLANS.get(plan)
    if not plan_info:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    
    # En producción, esto procesaría el pago via Stripe/PayU
    db.update_user_subscription(current_user["id"], plan, plan_info.credits_per_month)
    
    updated_user = db.get_user_by_id(current_user["id"])
    return UserResponse(
        id=updated_user["id"],
        email=updated_user["email"],
        full_name=updated_user["full_name"],
        phone=updated_user.get("phone"),
        role=updated_user["role"],
        credits=updated_user["credits"],
        subscription_plan=updated_user.get("subscription_plan"),
        created_at=updated_user["created_at"]
    )


# ==================== ENDPOINTS DE NEGOCIOS ====================

@app.get("/api/businesses", response_model=List[BusinessResponse], tags=["Negocios"])
async def obtener_negocios(
    category: Optional[BusinessCategory] = Query(None, description="Filtrar por categoría"),
    city: Optional[str] = Query(None, description="Filtrar por ciudad")
):
    """Obtener todos los negocios con filtros opcionales"""
    businesses = db.get_all_businesses(category=category, city=city)
    return [BusinessResponse(
        id=b["id"],
        name=b["name"],
        description=b["description"],
        category=b["category"],
        address=b["address"],
        city=b["city"],
        country=b["country"],
        phone=b["phone"],
        email=b["email"],
        image_url=b.get("image_url"),
        rating=b["rating"],
        owner_id=b["owner_id"],
        is_active=b["is_active"],
        created_at=b["created_at"]
    ) for b in businesses]


@app.get("/api/businesses/{business_id}", response_model=BusinessResponse, tags=["Negocios"])
async def obtener_negocio(business_id: str):
    """Obtener un negocio específico por ID"""
    business = db.get_business_by_id(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    return BusinessResponse(
        id=business["id"],
        name=business["name"],
        description=business["description"],
        category=business["category"],
        address=business["address"],
        city=business["city"],
        country=business["country"],
        phone=business["phone"],
        email=business["email"],
        image_url=business.get("image_url"),
        rating=business["rating"],
        owner_id=business["owner_id"],
        is_active=business["is_active"],
        created_at=business["created_at"]
    )


@app.get("/api/categories", tags=["Negocios"])
async def obtener_categorias():
    """Obtener todas las categorías de negocios con nombres en español e imágenes"""
    category_data = {
        BusinessCategory.YOGA: {
            "label": "Yoga",
            "image": "https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=400"
        },
        BusinessCategory.PILATES: {
            "label": "Pilates",
            "image": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400"
        },
        BusinessCategory.CYCLING: {
            "label": "Ciclismo",
            "image": "https://images.unsplash.com/photo-1534787238916-9ba6764efd4f?w=400"
        },
        BusinessCategory.STRENGTH: {
            "label": "Entrenamiento de fuerza",
            "image": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400"
        },
        BusinessCategory.DANCE: {
            "label": "Danza",
            "image": "https://images.unsplash.com/photo-1508700929628-666bc8bd84ea?w=400"
        },
        BusinessCategory.BOXING: {
            "label": "Boxeo",
            "image": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=400"
        },
        BusinessCategory.RUNNING: {
            "label": "Carrera",
            "image": "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400"
        },
        BusinessCategory.MARTIAL_ARTS: {
            "label": "Artes marciales",
            "image": "https://images.unsplash.com/photo-1555597673-b21d5c935865?w=400"
        },
        BusinessCategory.BARBERSHOP: {
            "label": "Barbería para hombres",
            "image": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=400"
        },
        BusinessCategory.SPA: {
            "label": "Spa",
            "image": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=400"
        },
        BusinessCategory.PARTY: {
            "label": "Fiesta",
            "image": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=400"
        }
    }
    return [{"value": cat.value, "label": data["label"], "image": data["image"]} for cat, data in category_data.items()]


# ==================== ENDPOINTS DE SERVICIOS ====================

@app.get("/api/businesses/{business_id}/services", response_model=List[ServiceResponse], tags=["Servicios"])
async def obtener_servicios_negocio(business_id: str):
    """Obtener todos los servicios de un negocio"""
    business = db.get_business_by_id(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    services = db.get_services_by_business(business_id)
    return [ServiceResponse(
        id=s["id"],
        name=s["name"],
        description=s["description"],
        duration_minutes=s["duration_minutes"],
        credits_cost=s["credits_cost"],
        price_cop=s.get("price_cop", 0),
        max_capacity=s["max_capacity"],
        business_id=s["business_id"],
        is_active=s["is_active"],
        created_at=s["created_at"]
    ) for s in services]


@app.get("/api/services/{service_id}", response_model=ServiceResponse, tags=["Servicios"])
async def obtener_servicio(service_id: str):
    """Obtener un servicio específico por ID"""
    service = db.get_service_by_id(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    return ServiceResponse(
        id=service["id"],
        name=service["name"],
        description=service["description"],
        duration_minutes=service["duration_minutes"],
        credits_cost=service["credits_cost"],
        price_cop=service.get("price_cop", 0),
        max_capacity=service["max_capacity"],
        business_id=service["business_id"],
        is_active=service["is_active"],
        created_at=service["created_at"]
    )


# ==================== ENDPOINTS DE HORARIOS ====================

@app.get("/api/services/{service_id}/schedule", response_model=List[ScheduleSlot], tags=["Horarios"])
async def obtener_horarios_servicio(
    service_id: str,
    date: Optional[str] = Query(None, description="Filtrar por fecha (YYYY-MM-DD)")
):
    """Obtener horarios disponibles para un servicio"""
    service = db.get_service_by_id(service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    slots = db.get_schedule_slots(service_id, date)
    return [ScheduleSlot(
        id=s["id"],
        service_id=s["service_id"],
        date=s["date"],
        start_time=s["start_time"],
        end_time=s["end_time"],
        available_spots=s["available_spots"],
        total_spots=s["total_spots"]
    ) for s in slots]


# ==================== ENDPOINTS DE RESERVAS ====================

@app.post("/api/bookings", response_model=BookingResponse, tags=["Reservas"])
async def crear_reserva(booking_data: BookingCreate, current_user: dict = Depends(get_current_user)):
    """Crear una nueva reserva"""
    # Validar que el servicio existe
    service = db.get_service_by_id(booking_data.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    # Validar que el horario existe y tiene disponibilidad
    slot = db.get_slot_by_id(booking_data.schedule_slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    if slot["available_spots"] <= 0:
        raise HTTPException(status_code=400, detail="No hay cupos disponibles para este horario")
    
    # Verificar que el usuario tiene suficientes créditos
    credits_cost = service["credits_cost"]
    if current_user["credits"] < credits_cost:
        raise HTTPException(status_code=400, detail=f"Créditos insuficientes. Necesitas: {credits_cost}, Tienes: {current_user['credits']}")
    
    # Descontar créditos y reducir disponibilidad
    db.update_user_credits(current_user["id"], -credits_cost)
    db.decrease_slot_availability(booking_data.schedule_slot_id)
    
    # Crear reserva
    business = db.get_business_by_id(service["business_id"])
    booking = db.create_booking({
        "user_id": current_user["id"],
        "service_id": booking_data.service_id,
        "schedule_slot_id": booking_data.schedule_slot_id,
        "credits_used": credits_cost
    })
    
    return BookingResponse(
        id=booking["id"],
        user_id=booking["user_id"],
        service_id=booking["service_id"],
        schedule_slot_id=booking["schedule_slot_id"],
        status=booking["status"],
        credits_used=booking["credits_used"],
        created_at=booking["created_at"],
        service_name=service["name"],
        business_name=business["name"] if business else None,
        date=slot["date"],
        start_time=slot["start_time"]
    )


@app.get("/api/bookings", response_model=List[BookingResponse], tags=["Reservas"])
async def obtener_mis_reservas(current_user: dict = Depends(get_current_user)):
    """Obtener todas las reservas del usuario actual"""
    bookings = db.get_user_bookings(current_user["id"])
    return [BookingResponse(
        id=b["id"],
        user_id=b["user_id"],
        service_id=b["service_id"],
        schedule_slot_id=b["schedule_slot_id"],
        status=b["status"],
        credits_used=b["credits_used"],
        created_at=b["created_at"],
        service_name=b.get("service_name"),
        business_name=b.get("business_name"),
        date=b.get("date"),
        start_time=b.get("start_time")
    ) for b in bookings]


@app.delete("/api/bookings/{booking_id}", tags=["Reservas"])
async def cancelar_reserva(booking_id: str, current_user: dict = Depends(get_current_user)):
    """Cancelar una reserva y reembolsar créditos"""
    booking = db.get_booking_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    if booking["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="No tienes permiso para cancelar esta reserva")
    
    if booking["status"].value == "cancelled":
        raise HTTPException(status_code=400, detail="La reserva ya fue cancelada")
    
    # Reembolsar créditos y aumentar disponibilidad
    db.update_user_credits(current_user["id"], booking["credits_used"])
    db.increase_slot_availability(booking["schedule_slot_id"])
    db.cancel_booking(booking_id)
    
    return {"message": "Reserva cancelada exitosamente", "credits_refunded": booking["credits_used"]}


# ==================== ENDPOINT DE ESTADÍSTICAS ====================

@app.get("/api/stats", tags=["Estadísticas"])
async def obtener_estadisticas():
    """Obtener estadísticas de la plataforma para la página principal"""
    return {
        "total_businesses": len(db.businesses),
        "total_services": len(db.services),
        "cities": ["Bogotá", "Medellín", "Cali", "Barranquilla", "Cartagena"],
        "categories_count": len(BusinessCategory)
    }


# ==================== ENDPOINTS DE ADMINISTRACIÓN ====================

ADMIN_PASSWORD = "admin123"

@app.post("/api/admin/login", tags=["Admin"])
async def admin_login(password: str = Query(...)):
    """Login de administrador con contraseña simple"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    return {"message": "Acceso concedido", "admin": True}


@app.get("/api/admin/businesses", response_model=List[BusinessResponse], tags=["Admin"])
async def admin_obtener_negocios(
    category: Optional[BusinessCategory] = Query(None),
    city: Optional[str] = Query(None),
    password: str = Query(...)
):
    """Obtener todos los negocios (incluyendo inactivos) - Solo admin"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    businesses = db.get_all_businesses_admin(category, city)
    return [BusinessResponse(
        id=b["id"],
        name=b["name"],
        description=b["description"],
        category=b["category"],
        address=b["address"],
        city=b["city"],
        country=b["country"],
        phone=b["phone"],
        email=b["email"],
        image_url=b.get("image_url"),
        rating=b.get("rating", 0),
        owner_id=b["owner_id"],
        is_active=b["is_active"],
        created_at=b["created_at"]
    ) for b in businesses]


@app.post("/api/admin/businesses", response_model=BusinessResponse, tags=["Admin"])
async def admin_crear_negocio(business_data: BusinessCreate, password: str = Query(...)):
    """Crear un nuevo negocio - Solo admin"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    business = db.create_business({
        "name": business_data.name,
        "description": business_data.description,
        "category": business_data.category,
        "address": business_data.address,
        "city": business_data.city,
        "country": business_data.country,
        "phone": business_data.phone,
        "email": business_data.email,
        "image_url": business_data.image_url,
        "rating": business_data.rating,
        "owner_id": business_data.owner_id or "admin"
    })
    
    return BusinessResponse(
        id=business["id"],
        name=business["name"],
        description=business["description"],
        category=business["category"],
        address=business["address"],
        city=business["city"],
        country=business["country"],
        phone=business["phone"],
        email=business["email"],
        image_url=business.get("image_url"),
        rating=business.get("rating", 0),
        owner_id=business["owner_id"],
        is_active=business["is_active"],
        created_at=business["created_at"]
    )


@app.put("/api/admin/businesses/{business_id}", response_model=BusinessResponse, tags=["Admin"])
async def admin_actualizar_negocio(business_id: str, business_data: BusinessUpdate, password: str = Query(...)):
    """Actualizar un negocio - Solo admin"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    update_data = {}
    if business_data.name is not None:
        update_data["name"] = business_data.name
    if business_data.description is not None:
        update_data["description"] = business_data.description
    if business_data.address is not None:
        update_data["address"] = business_data.address
    if business_data.phone is not None:
        update_data["phone"] = business_data.phone
    if business_data.image_url is not None:
        update_data["image_url"] = business_data.image_url
    
    business = db.update_business(business_id, update_data)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    return BusinessResponse(
        id=business["id"],
        name=business["name"],
        description=business["description"],
        category=business["category"],
        address=business["address"],
        city=business["city"],
        country=business["country"],
        phone=business["phone"],
        email=business["email"],
        image_url=business.get("image_url"),
        rating=business.get("rating", 0),
        owner_id=business["owner_id"],
        is_active=business["is_active"],
        created_at=business["created_at"]
    )


@app.patch("/api/admin/businesses/{business_id}/toggle", tags=["Admin"])
async def admin_toggle_negocio(business_id: str, is_active: bool = Query(...), password: str = Query(...)):
    """Habilitar o deshabilitar un negocio - Solo admin"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    business = db.toggle_business_active(business_id, is_active)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    return {"message": f"Negocio {'habilitado' if is_active else 'deshabilitado'} exitosamente", "is_active": is_active}


@app.get("/api/admin/businesses/{business_id}/services", response_model=List[ServiceResponse], tags=["Admin"])
async def admin_obtener_servicios(business_id: str, password: str = Query(...)):
    """Obtener todos los servicios de un negocio (incluyendo inactivos) - Solo admin"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    services = db.get_all_services_by_business_admin(business_id)
    return [ServiceResponse(
        id=s["id"],
        name=s["name"],
        description=s["description"],
        duration_minutes=s["duration_minutes"],
        credits_cost=s["credits_cost"],
        price_cop=s.get("price_cop", 0),
        max_capacity=s["max_capacity"],
        business_id=s["business_id"],
        is_active=s["is_active"],
        created_at=s["created_at"]
    ) for s in services]


@app.post("/api/admin/businesses/{business_id}/services", response_model=ServiceResponse, tags=["Admin"])
async def admin_crear_servicio(business_id: str, service_data: ServiceCreate, password: str = Query(...)):
    """Crear un nuevo servicio para un negocio - Solo admin"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    business = db.get_business_by_id(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Negocio no encontrado")
    
    service = db.create_service({
        "name": service_data.name,
        "description": service_data.description,
        "duration_minutes": service_data.duration_minutes,
        "credits_cost": service_data.credits_cost,
        "price_cop": service_data.price_cop,
        "max_capacity": service_data.max_capacity,
        "business_id": business_id
    })
    
    return ServiceResponse(
        id=service["id"],
        name=service["name"],
        description=service["description"],
        duration_minutes=service["duration_minutes"],
        credits_cost=service["credits_cost"],
        price_cop=service.get("price_cop", 0),
        max_capacity=service["max_capacity"],
        business_id=service["business_id"],
        is_active=service["is_active"],
        created_at=service["created_at"]
    )


@app.put("/api/admin/services/{service_id}", response_model=ServiceResponse, tags=["Admin"])
async def admin_actualizar_servicio(service_id: str, service_data: ServiceUpdate, password: str = Query(...)):
    """Actualizar un servicio - Solo admin"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    update_data = {}
    if service_data.name is not None:
        update_data["name"] = service_data.name
    if service_data.description is not None:
        update_data["description"] = service_data.description
    if service_data.duration_minutes is not None:
        update_data["duration_minutes"] = service_data.duration_minutes
    if service_data.credits_cost is not None:
        update_data["credits_cost"] = service_data.credits_cost
    if service_data.max_capacity is not None:
        update_data["max_capacity"] = service_data.max_capacity
    
    service = db.update_service(service_id, update_data)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    return ServiceResponse(
        id=service["id"],
        name=service["name"],
        description=service["description"],
        duration_minutes=service["duration_minutes"],
        credits_cost=service["credits_cost"],
        price_cop=service.get("price_cop", 0),
        max_capacity=service["max_capacity"],
        business_id=service["business_id"],
        is_active=service["is_active"],
        created_at=service["created_at"]
    )


@app.patch("/api/admin/services/{service_id}/toggle", tags=["Admin"])
async def admin_toggle_servicio(service_id: str, is_active: bool = Query(...), password: str = Query(...)):
    """Habilitar o deshabilitar un servicio - Solo admin"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    service = db.toggle_service_active(service_id, is_active)
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    return {"message": f"Servicio {'habilitado' if is_active else 'deshabilitado'} exitosamente", "is_active": is_active}


@app.patch("/api/admin/services/{service_id}/price", tags=["Admin"])
async def admin_actualizar_precio(service_id: str, credits_cost: int = Query(...), price_cop: int = Query(...), password: str = Query(...)):
    """Actualizar el precio de un servicio - Solo admin"""
    if password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")
    
    service = db.update_service(service_id, {"credits_cost": credits_cost, "price_cop": price_cop})
    if not service:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    return {"message": "Precio actualizado exitosamente", "credits_cost": credits_cost, "price_cop": price_cop}
