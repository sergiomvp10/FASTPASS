import os
from typing import Dict, List, Optional
from datetime import datetime
import uuid
from app.models import (
    UserRole, SubscriptionPlan, BusinessCategory, BookingStatus,
    UserResponse, BusinessResponse, ServiceResponse, ScheduleSlot, BookingResponse
)

# In-memory database for MVP
# In production, this would be replaced with a real database

class Database:
    def __init__(self):
        self.users: Dict[str, dict] = {}
        self.businesses: Dict[str, dict] = {}
        self.services: Dict[str, dict] = {}
        self.schedule_slots: Dict[str, dict] = {}
        self.bookings: Dict[str, dict] = {}
        self._seed_data()
    
    def _seed_data(self):
        # Create sample businesses for demo - Boyacá, Colombia
        sample_businesses = [
            {
                "id": str(uuid.uuid4()),
                "name": "Yoga Duitama Studio",
                "description": "Estudio de yoga con clases de Hatha, Vinyasa, Yin y meditación guiada en el centro de Duitama.",
                "category": BusinessCategory.YOGA,
                "address": "Calle 16 #15-20",
                "city": "Duitama",
                "country": "Colombia",
                "phone": "+57 608 345 6789",
                "email": "namaste@yogaduitama.co",
                "image_url": "https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=800",
                "rating": 4.9,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Pilates Studio Tunja",
                "description": "Estudio de Pilates con reformer, mat y clases personalizadas en el centro histórico.",
                "category": BusinessCategory.PILATES,
                "address": "Cra 10 #19-50",
                "city": "Tunja",
                "country": "Colombia",
                "phone": "+57 608 890 1234",
                "email": "info@pilatestunja.co",
                "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=800",
                "rating": 4.9,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Spinning Center Sogamoso",
                "description": "Centro de ciclismo indoor con clases de spinning de alta intensidad y música motivadora.",
                "category": BusinessCategory.CYCLING,
                "address": "Cra 11 #14-75",
                "city": "Sogamoso",
                "country": "Colombia",
                "phone": "+57 608 234 5678",
                "email": "info@spinningsogamoso.co",
                "image_url": "https://images.unsplash.com/photo-1534787238916-9ba6764efd4f?w=800",
                "rating": 4.7,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Iron Gym Duitama",
                "description": "Gimnasio especializado en entrenamiento de fuerza con equipos de última generación.",
                "category": BusinessCategory.STRENGTH,
                "address": "Calle 18 #15-28",
                "city": "Duitama",
                "country": "Colombia",
                "phone": "+57 608 789 0123",
                "email": "info@irongymduitama.co",
                "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800",
                "rating": 4.8,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Dance Studio Tunja",
                "description": "Academia de danza con clases de salsa, bachata, urbano y contemporáneo.",
                "category": BusinessCategory.DANCE,
                "address": "Calle 20 #9-105",
                "city": "Tunja",
                "country": "Colombia",
                "phone": "+57 608 901 2345",
                "email": "baila@dancestudiotunja.co",
                "image_url": "https://images.unsplash.com/photo-1508700929628-666bc8bd84ea?w=800",
                "rating": 4.8,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Boxing Club Sogamoso",
                "description": "Club de boxeo con clases para principiantes y avanzados, entrenamiento funcional incluido.",
                "category": BusinessCategory.BOXING,
                "address": "Cra 12 #11-50",
                "city": "Sogamoso",
                "country": "Colombia",
                "phone": "+57 608 567 8901",
                "email": "info@boxingsogamoso.co",
                "image_url": "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=800",
                "rating": 4.7,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Running Club Duitama",
                "description": "Club de corredores con entrenamientos grupales, planes personalizados y carreras mensuales.",
                "category": BusinessCategory.RUNNING,
                "address": "Parque de los Libertadores",
                "city": "Duitama",
                "country": "Colombia",
                "phone": "+57 608 456 7890",
                "email": "corre@runningduitama.co",
                "image_url": "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800",
                "rating": 4.6,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Dojo Artes Marciales Tunja",
                "description": "Academia de artes marciales con clases de karate, taekwondo, jiu-jitsu y MMA.",
                "category": BusinessCategory.MARTIAL_ARTS,
                "address": "Cra 9 #22-71",
                "city": "Tunja",
                "country": "Colombia",
                "phone": "+57 608 678 9012",
                "email": "sensei@dojotunja.co",
                "image_url": "https://images.unsplash.com/photo-1555597673-b21d5c935865?w=800",
                "rating": 4.9,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "La Barbería Clásica Duitama",
                "description": "Barbería clásica para hombres con cortes, afeitado y tratamientos para barba estilo tradicional.",
                "category": BusinessCategory.BARBERSHOP,
                "address": "Calle 15 #16-53",
                "city": "Duitama",
                "country": "Colombia",
                "phone": "+57 608 123 4567",
                "email": "citas@barberiaduitama.co",
                "image_url": "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=800",
                "rating": 4.8,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Spa Serena Sogamoso",
                "description": "Spa de lujo con masajes, tratamientos faciales, sauna y jacuzzi en el centro de Sogamoso.",
                "category": BusinessCategory.SPA,
                "address": "Cra 10 #12-24",
                "city": "Sogamoso",
                "country": "Colombia",
                "phone": "+57 608 456 7890",
                "email": "reservas@spasogamoso.co",
                "image_url": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=800",
                "rating": 4.8,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Club Élite Tunja",
                "description": "Discoteca de alto nivel con música electrónica, house y reggaetón. Ambiente exclusivo y VIP.",
                "category": BusinessCategory.PARTY,
                "address": "Zona Rosa, Calle 19 #10-15",
                "city": "Tunja",
                "country": "Colombia",
                "phone": "+57 608 555 1234",
                "email": "reservas@clubelitetunja.co",
                "image_url": "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=800",
                "rating": 4.7,
                "owner_id": "system",
                "is_active": True,
                "created_at": datetime.utcnow()
            }
        ]
        
        for business in sample_businesses:
            self.businesses[business["id"]] = business
        
        # Create sample services for each business
        # Precios en COP con ~30% de descuento sobre precio normal
        service_templates = {
            BusinessCategory.YOGA: [
                {"name": "Hatha Yoga", "description": "Clase de yoga tradicional para todos los niveles", "duration_minutes": 60, "credits_cost": 6, "price_cop": 7500, "max_capacity": 15},
                {"name": "Vinyasa Flow", "description": "Yoga dinámico con secuencias fluidas", "duration_minutes": 75, "credits_cost": 7, "price_cop": 9000, "max_capacity": 12},
                {"name": "Meditación Guiada", "description": "Sesión de meditación y mindfulness", "duration_minutes": 30, "credits_cost": 4, "price_cop": 5000, "max_capacity": 20},
            ],
            BusinessCategory.PILATES: [
                {"name": "Mat Pilates", "description": "Clase de Pilates en colchoneta", "duration_minutes": 50, "credits_cost": 6, "price_cop": 8000, "max_capacity": 12},
                {"name": "Reformer", "description": "Clase en máquina reformer", "duration_minutes": 50, "credits_cost": 10, "price_cop": 15000, "max_capacity": 6},
                {"name": "Pilates Privado", "description": "Sesión individual personalizada", "duration_minutes": 50, "credits_cost": 15, "price_cop": 25000, "max_capacity": 1},
            ],
            BusinessCategory.CYCLING: [
                {"name": "Spinning Básico", "description": "Clase de ciclismo indoor para principiantes", "duration_minutes": 45, "credits_cost": 5, "price_cop": 6000, "max_capacity": 25},
                {"name": "Spinning Intenso", "description": "Clase de alta intensidad con intervalos", "duration_minutes": 50, "credits_cost": 7, "price_cop": 8000, "max_capacity": 20},
                {"name": "Cycling con Ritmo", "description": "Spinning al ritmo de la música", "duration_minutes": 45, "credits_cost": 6, "price_cop": 7000, "max_capacity": 25},
            ],
            BusinessCategory.STRENGTH: [
                {"name": "Entrenamiento de Fuerza", "description": "Clase grupal de levantamiento de pesas", "duration_minutes": 60, "credits_cost": 5, "price_cop": 5000, "max_capacity": 15},
                {"name": "Sesión Personal", "description": "Entrenamiento personalizado con coach", "duration_minutes": 60, "credits_cost": 12, "price_cop": 18000, "max_capacity": 1},
                {"name": "Circuito de Fuerza", "description": "Entrenamiento en circuito con pesas", "duration_minutes": 45, "credits_cost": 4, "price_cop": 4500, "max_capacity": 12},
            ],
            BusinessCategory.DANCE: [
                {"name": "Salsa", "description": "Clase de salsa para todos los niveles", "duration_minutes": 60, "credits_cost": 6, "price_cop": 7000, "max_capacity": 20},
                {"name": "Bachata", "description": "Aprende a bailar bachata", "duration_minutes": 60, "credits_cost": 6, "price_cop": 7000, "max_capacity": 20},
                {"name": "Urbano", "description": "Clase de baile urbano y hip-hop", "duration_minutes": 60, "credits_cost": 7, "price_cop": 8000, "max_capacity": 18},
            ],
            BusinessCategory.BOXING: [
                {"name": "Boxeo Básico", "description": "Introducción al boxeo y técnicas básicas", "duration_minutes": 60, "credits_cost": 7, "price_cop": 8000, "max_capacity": 15},
                {"name": "Boxeo Cardio", "description": "Entrenamiento cardiovascular con boxeo", "duration_minutes": 45, "credits_cost": 6, "price_cop": 7000, "max_capacity": 20},
                {"name": "Sparring", "description": "Práctica de combate supervisada", "duration_minutes": 60, "credits_cost": 10, "price_cop": 12000, "max_capacity": 10},
            ],
            BusinessCategory.RUNNING: [
                {"name": "Entrenamiento Grupal", "description": "Sesión de running en grupo", "duration_minutes": 60, "credits_cost": 4, "price_cop": 4000, "max_capacity": 30},
                {"name": "Intervalos", "description": "Entrenamiento de intervalos de alta intensidad", "duration_minutes": 45, "credits_cost": 5, "price_cop": 5000, "max_capacity": 25},
                {"name": "Técnica de Carrera", "description": "Mejora tu técnica de running", "duration_minutes": 60, "credits_cost": 7, "price_cop": 8000, "max_capacity": 15},
            ],
            BusinessCategory.MARTIAL_ARTS: [
                {"name": "Karate", "description": "Clase de karate tradicional", "duration_minutes": 60, "credits_cost": 7, "price_cop": 8000, "max_capacity": 15},
                {"name": "Taekwondo", "description": "Arte marcial coreano", "duration_minutes": 60, "credits_cost": 7, "price_cop": 8000, "max_capacity": 15},
                {"name": "Jiu-Jitsu", "description": "Arte marcial brasileño de grappling", "duration_minutes": 75, "credits_cost": 9, "price_cop": 12000, "max_capacity": 12},
            ],
            BusinessCategory.BARBERSHOP: [
                {"name": "Corte Clásico", "description": "Corte de cabello tradicional para hombres", "duration_minutes": 30, "credits_cost": 5, "price_cop": 12000, "max_capacity": 1},
                {"name": "Corte + Barba", "description": "Corte de cabello y arreglo de barba", "duration_minutes": 45, "credits_cost": 8, "price_cop": 18000, "max_capacity": 1},
                {"name": "Afeitado Clásico", "description": "Afeitado con navaja y toalla caliente", "duration_minutes": 30, "credits_cost": 6, "price_cop": 15000, "max_capacity": 1},
            ],
            BusinessCategory.SPA: [
                {"name": "Masaje Relajante", "description": "Masaje corporal completo para relajación", "duration_minutes": 60, "credits_cost": 12, "price_cop": 25000, "max_capacity": 1},
                {"name": "Facial Hidratante", "description": "Tratamiento facial de hidratación profunda", "duration_minutes": 45, "credits_cost": 10, "price_cop": 20000, "max_capacity": 1},
                {"name": "Circuito Spa", "description": "Acceso a sauna, vapor y jacuzzi", "duration_minutes": 120, "credits_cost": 8, "price_cop": 18000, "max_capacity": 10},
            ],
            BusinessCategory.PARTY: [
                {"name": "Entrada General", "description": "Acceso a la discoteca con entrada prioritaria", "duration_minutes": 240, "credits_cost": 6, "price_cop": 15000, "max_capacity": 50},
                {"name": "Mesa VIP", "description": "Mesa reservada en zona VIP con botella incluida", "duration_minutes": 240, "credits_cost": 15, "price_cop": 80000, "max_capacity": 8},
                {"name": "Experiencia Premium", "description": "Acceso VIP con mesa, botella premium y servicio exclusivo", "duration_minutes": 240, "credits_cost": 25, "price_cop": 150000, "max_capacity": 6},
            ],
        }
        
        for business_id, business in self.businesses.items():
            category = business["category"]
            if category in service_templates:
                for service_data in service_templates[category]:
                    service_id = str(uuid.uuid4())
                    service = {
                        "id": service_id,
                        "business_id": business_id,
                        "is_active": True,
                        "created_at": datetime.utcnow(),
                        **service_data
                    }
                    self.services[service_id] = service
                    
                    # Create schedule slots for the next 7 days
                    self._create_schedule_slots(service_id, service_data["max_capacity"])
    
    def _create_schedule_slots(self, service_id: str, max_capacity: int):
        from datetime import timedelta
        base_date = datetime.utcnow().date()
        time_slots = ["09:00", "10:00", "11:00", "12:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
        
        for day_offset in range(7):
            date = base_date + timedelta(days=day_offset)
            for start_time in time_slots:
                slot_id = str(uuid.uuid4())
                hour = int(start_time.split(":")[0])
                end_time = f"{hour + 1:02d}:00"
                
                self.schedule_slots[slot_id] = {
                    "id": slot_id,
                    "service_id": service_id,
                    "date": date.isoformat(),
                    "start_time": start_time,
                    "end_time": end_time,
                    "available_spots": max_capacity,
                    "total_spots": max_capacity
                }
    
    # User methods
    def create_user(self, user_data: dict) -> dict:
        user_id = str(uuid.uuid4())
        user = {
            "id": user_id,
            "role": UserRole.USER,
            "credits": 20,  # Free credits for new users
            "subscription_plan": None,
            "created_at": datetime.utcnow(),
            **user_data
        }
        self.users[user_id] = user
        return user
    
    def get_user_by_email(self, email: str) -> Optional[dict]:
        for user in self.users.values():
            if user["email"] == email:
                return user
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[dict]:
        return self.users.get(user_id)
    
    def update_user_credits(self, user_id: str, credits_change: int) -> bool:
        if user_id in self.users:
            self.users[user_id]["credits"] += credits_change
            return True
        return False
    
    def update_user_subscription(self, user_id: str, plan: SubscriptionPlan, credits: int) -> bool:
        if user_id in self.users:
            self.users[user_id]["subscription_plan"] = plan
            self.users[user_id]["credits"] += credits
            return True
        return False
    
    # Business methods
    def get_all_businesses(self, category: Optional[BusinessCategory] = None, city: Optional[str] = None) -> List[dict]:
        businesses = list(self.businesses.values())
        if category:
            businesses = [b for b in businesses if b["category"] == category]
        if city:
            businesses = [b for b in businesses if city.lower() in b["city"].lower()]
        return [b for b in businesses if b["is_active"]]
    
    def get_business_by_id(self, business_id: str) -> Optional[dict]:
        return self.businesses.get(business_id)
    
    def create_business(self, business_data: dict) -> dict:
        business_id = str(uuid.uuid4())
        business = {
            "id": business_id,
            "is_active": True,
            "created_at": datetime.utcnow(),
            **business_data
        }
        self.businesses[business_id] = business
        return business
    
    # Service methods
    def get_services_by_business(self, business_id: str) -> List[dict]:
        return [s for s in self.services.values() if s["business_id"] == business_id and s["is_active"]]
    
    def get_service_by_id(self, service_id: str) -> Optional[dict]:
        return self.services.get(service_id)
    
    def create_service(self, service_data: dict) -> dict:
        service_id = str(uuid.uuid4())
        service = {
            "id": service_id,
            "is_active": True,
            "created_at": datetime.utcnow(),
            **service_data
        }
        self.services[service_id] = service
        self._create_schedule_slots(service_id, service_data.get("max_capacity", 1))
        return service
    
    # Schedule methods
    def get_schedule_slots(self, service_id: str, date: Optional[str] = None) -> List[dict]:
        slots = [s for s in self.schedule_slots.values() if s["service_id"] == service_id]
        if date:
            slots = [s for s in slots if s["date"] == date]
        return [s for s in slots if s["available_spots"] > 0]
    
    def get_slot_by_id(self, slot_id: str) -> Optional[dict]:
        return self.schedule_slots.get(slot_id)
    
    def decrease_slot_availability(self, slot_id: str) -> bool:
        if slot_id in self.schedule_slots and self.schedule_slots[slot_id]["available_spots"] > 0:
            self.schedule_slots[slot_id]["available_spots"] -= 1
            return True
        return False
    
    def increase_slot_availability(self, slot_id: str) -> bool:
        if slot_id in self.schedule_slots:
            slot = self.schedule_slots[slot_id]
            if slot["available_spots"] < slot["total_spots"]:
                slot["available_spots"] += 1
                return True
        return False
    
    # Booking methods
    def create_booking(self, booking_data: dict) -> dict:
        booking_id = str(uuid.uuid4())
        booking = {
            "id": booking_id,
            "status": BookingStatus.CONFIRMED,
            "created_at": datetime.utcnow(),
            **booking_data
        }
        self.bookings[booking_id] = booking
        return booking
    
    def get_user_bookings(self, user_id: str) -> List[dict]:
        bookings = [b for b in self.bookings.values() if b["user_id"] == user_id]
        # Enrich with service and business info
        enriched = []
        for booking in bookings:
            service = self.get_service_by_id(booking["service_id"])
            slot = self.get_slot_by_id(booking["schedule_slot_id"])
            if service and slot:
                business = self.get_business_by_id(service["business_id"])
                enriched.append({
                    **booking,
                    "service_name": service["name"],
                    "business_name": business["name"] if business else "Unknown",
                    "date": slot["date"],
                    "start_time": slot["start_time"]
                })
        return enriched
    
    def get_booking_by_id(self, booking_id: str) -> Optional[dict]:
        return self.bookings.get(booking_id)
    
    def cancel_booking(self, booking_id: str) -> bool:
        if booking_id in self.bookings:
            self.bookings[booking_id]["status"] = BookingStatus.CANCELLED
            return True
        return False
    
    # Admin methods
    def get_all_businesses_admin(self, category: Optional[BusinessCategory] = None, city: Optional[str] = None) -> List[dict]:
        """Get all businesses including inactive ones (for admin)"""
        businesses = list(self.businesses.values())
        if category:
            businesses = [b for b in businesses if b["category"] == category]
        if city:
            businesses = [b for b in businesses if city.lower() in b["city"].lower()]
        return businesses
    
    def update_business(self, business_id: str, update_data: dict) -> Optional[dict]:
        """Update a business"""
        if business_id not in self.businesses:
            return None
        for key, value in update_data.items():
            if value is not None:
                self.businesses[business_id][key] = value
        return self.businesses[business_id]
    
    def toggle_business_active(self, business_id: str, is_active: bool) -> Optional[dict]:
        """Enable or disable a business"""
        if business_id not in self.businesses:
            return None
        self.businesses[business_id]["is_active"] = is_active
        return self.businesses[business_id]
    
    def get_all_services_by_business_admin(self, business_id: str) -> List[dict]:
        """Get all services including inactive ones (for admin)"""
        return [s for s in self.services.values() if s["business_id"] == business_id]
    
    def update_service(self, service_id: str, update_data: dict) -> Optional[dict]:
        """Update a service"""
        if service_id not in self.services:
            return None
        for key, value in update_data.items():
            if value is not None:
                self.services[service_id][key] = value
        return self.services[service_id]
    
    def toggle_service_active(self, service_id: str, is_active: bool) -> Optional[dict]:
        """Enable or disable a service"""
        if service_id not in self.services:
            return None
        self.services[service_id]["is_active"] = is_active
        return self.services[service_id]
    
    def delete_service(self, service_id: str) -> bool:
        """Delete a service"""
        if service_id in self.services:
            del self.services[service_id]
            return True
        return False


# Global database instance
db = Database()
