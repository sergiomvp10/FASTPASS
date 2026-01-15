import { useState, useEffect, useRef, useCallback } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Tabs, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Toaster } from '@/components/ui/sonner';
import { toast } from 'sonner';
import { 
  Search, MapPin, Star, Clock, Users, CreditCard, Menu, X, 
  Dumbbell, Heart, Sparkles, Scissors, Zap, User, LogOut,
  Calendar, Check
} from 'lucide-react';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const useScrollAnimation = () => {
  const observerRef = useRef<IntersectionObserver | null>(null);
  
  const observe = useCallback((element: HTMLElement | null) => {
    if (!element) return;
    
    if (!observerRef.current) {
      observerRef.current = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              entry.target.classList.add('visible');
            }
          });
        },
        { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
      );
    }
    
    observerRef.current.observe(element);
  }, []);
  
  return observe;
};

interface Business {
  id: string;
  name: string;
  description: string;
  category: string;
  address: string;
  city: string;
  country: string;
  phone: string;
  email: string;
  image_url: string;
  rating: number;
  is_active: boolean;
}

interface Service {
  id: string;
  name: string;
  description: string;
  duration_minutes: number;
  credits_cost: number;
  price_cop: number;
  max_capacity: number;
  business_id: string;
}

interface ScheduleSlot {
  id: string;
  service_id: string;
  date: string;
  start_time: string;
  end_time: string;
  available_spots: number;
  total_spots: number;
}

interface Booking {
  id: string;
  service_name: string;
  business_name: string;
  date: string;
  start_time: string;
  status: string;
  credits_used: number;
}

interface UserType {
  id: string;
  email: string;
  full_name: string;
  credits: number;
  subscription_plan: string | null;
}

interface Category {
  value: string;
  label: string;
  image?: string;
}

interface SubscriptionPlan {
  plan: string;
  credits_per_month: number;
  price_usd: number;
  features: string[];
}

const Logo = ({ className = "" }: { className?: string }) => (
  <div className={`flex items-center gap-2 ${className}`}>
    <div className="w-10 h-10 rounded-full overflow-hidden border-2 border-white shadow-md flex items-center justify-center">
      <div className="w-full h-full flex flex-col">
        <div className="h-1/2 bg-yellow-400"></div>
        <div className="h-1/4 bg-blue-600"></div>
        <div className="h-1/4 bg-red-600"></div>
      </div>
    </div>
    <span className="text-xl font-bold text-gray-900">NextBooking Col</span>
  </div>
);

const categoryIcons: Record<string, React.ReactNode> = {
  yoga: <Heart className="w-5 h-5" />,
  pilates: <Heart className="w-5 h-5" />,
  cycling: <Zap className="w-5 h-5" />,
  strength: <Dumbbell className="w-5 h-5" />,
  dance: <Sparkles className="w-5 h-5" />,
  boxing: <Zap className="w-5 h-5" />,
  running: <Zap className="w-5 h-5" />,
  martial_arts: <Zap className="w-5 h-5" />,
  barbershop: <Scissors className="w-5 h-5" />,
  spa: <Sparkles className="w-5 h-5" />,
  party: <Sparkles className="w-5 h-5" />,
};

const LandingPage = ({ 
  onGetStarted, 
  onLogin,
  onBrowse 
}: { 
  onGetStarted: () => void;
  onLogin: () => void;
  onBrowse: () => void;
}) => {
  const observe = useScrollAnimation();
  const images = [
    'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400',
    'https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=400',
    'https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=400',
    'https://images.unsplash.com/photo-1560066984-138dadb4c035?w=400',
    'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=400',
    'https://images.unsplash.com/photo-1534258936925-c58bed479fcb?w=400',
    'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400',
    'https://images.unsplash.com/photo-1600334089648-b0d9d3028eb2?w=400',
    'https://images.unsplash.com/photo-1604654894610-df63bc536371?w=400',
    'https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=400',
    'https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=400',
    'https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=400',
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="fixed top-0 left-0 right-0 bg-white z-50 border-b">
        <nav className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <Logo />
          <div className="hidden md:flex items-center gap-6">
            <button onClick={onBrowse} className="text-gray-600 hover:text-gray-900">Buscar</button>
            <button className="text-gray-600 hover:text-gray-900">Planes</button>
            <button className="text-gray-600 hover:text-gray-900">Cómo funciona</button>
            <button onClick={onLogin} className="text-gray-600 hover:text-gray-900">Iniciar sesión</button>
            <Button onClick={onGetStarted} className="bg-blue-600 hover:bg-blue-700">
              Comenzar
            </Button>
          </div>
          <Button variant="ghost" className="md:hidden" size="icon">
            <Menu className="w-6 h-6" />
          </Button>
        </nav>
      </header>

      <section className="pt-16 min-h-screen relative overflow-hidden">
        <div className="absolute inset-0 grid grid-cols-4 md:grid-cols-6 gap-2 p-2 opacity-90">
          {images.map((img, i) => (
            <div 
              key={i} 
              className={`rounded-2xl overflow-hidden ${i % 3 === 0 ? 'row-span-2' : ''}`}
              style={{ 
                backgroundImage: `url(${img})`,
                backgroundSize: 'cover',
                backgroundPosition: 'center'
              }}
            />
          ))}
        </div>
        
        <div className="absolute inset-0 bg-gradient-to-b from-white/30 via-white/50 to-white/80" />
        
        <div className="relative z-10 flex items-center justify-center min-h-screen px-4">
          <Card className="max-w-lg w-full bg-white/95 backdrop-blur shadow-2xl">
            <CardHeader className="text-center pb-2">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 rounded-full overflow-hidden border-4 border-white shadow-lg flex flex-col">
                  <div className="h-1/2 bg-yellow-400"></div>
                  <div className="h-1/4 bg-blue-600"></div>
                  <div className="h-1/4 bg-red-600"></div>
                </div>
              </div>
              <CardTitle className="text-3xl md:text-4xl font-bold">
                ¡Hola, somos NextBooking Col!
              </CardTitle>
              <CardDescription className="text-lg mt-4 text-gray-600">
                Bienvenido a la membresía única para todo lo relacionado con fitness, bienestar y belleza en Colombia.
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4 pt-4">
              <Button 
                onClick={onGetStarted} 
                className="w-full bg-blue-600 hover:bg-blue-700 text-lg py-6"
              >
                Comenzar ahora
              </Button>
              <Button 
                onClick={onBrowse} 
                variant="outline" 
                className="w-full text-lg py-6"
              >
                Explorar clases y citas
              </Button>
            </CardContent>
          </Card>
        </div>

        <div className="absolute left-4 top-1/3 z-10 hidden md:block">
          <div className="bg-blue-600 text-white px-4 py-2 rounded-lg shadow-lg transform -rotate-6">
            <p className="font-bold">Una membresía</p>
            <p className="text-sm">para reservar todo</p>
          </div>
        </div>
      </section>

      <section className="py-20 bg-white overflow-hidden">
        <div className="max-w-6xl mx-auto px-4">
          <h2 ref={observe} className="animate-fade-up text-3xl font-bold text-center mb-12">¿Por qué NextBooking Col?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div ref={observe} className="animate-on-scroll stagger-1 text-center">
              <div className="w-64 h-48 mx-auto mb-6 rounded-2xl overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400" 
                  alt="Gimnasio"
                  className="w-full h-full object-cover"
                />
              </div>
              <h3 className="text-xl font-semibold mb-2">Sin limitaciones</h3>
              <p className="text-gray-600">
                Reserva en cualquier estudio, gimnasio, salón o spa que quieras, las veces que quieras.
              </p>
            </div>
            <div ref={observe} className="animate-on-scroll stagger-2 text-center">
              <div className="w-64 h-48 mx-auto mb-6 rounded-2xl overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=400" 
                  alt="Spa"
                  className="w-full h-full object-cover"
                />
              </div>
              <h3 className="text-xl font-semibold mb-2">Sin estrés</h3>
              <p className="text-gray-600">
                Haz ejercicio, recibe un masaje o incluso un manicure con la misma membresía.
              </p>
            </div>
            <div ref={observe} className="animate-on-scroll stagger-3 text-center">
              <div className="w-64 h-48 mx-auto mb-6 rounded-2xl overflow-hidden">
                <img 
                  src="https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=400" 
                  alt="Calendario"
                  className="w-full h-full object-cover"
                />
              </div>
              <h3 className="text-xl font-semibold mb-2">Sin compromisos</h3>
              <p className="text-gray-600">
                Las membresías son mensuales y cambiar tu plan es muy fácil.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="py-20 bg-blue-50 overflow-hidden">
        <div className="max-w-6xl mx-auto px-4">
          <h2 ref={observe} className="animate-fade-up text-3xl font-bold text-center mb-4">Explora nuestras categorías</h2>
          <p ref={observe} className="animate-fade-up text-gray-600 text-center mb-12 max-w-2xl mx-auto">
            Descubre una amplia variedad de actividades para tu bienestar físico y mental
          </p>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            {[
              { name: "Yoga", image: "https://images.unsplash.com/photo-1545205597-3d9d02c29597?w=400" },
              { name: "Pilates", image: "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400" },
              { name: "Ciclismo", image: "https://images.unsplash.com/photo-1534787238916-9ba6764efd4f?w=400" },
              { name: "Fuerza", image: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400" },
              { name: "Danza", image: "https://images.unsplash.com/photo-1508700929628-666bc8bd84ea?w=400" },
              { name: "Boxeo", image: "https://images.unsplash.com/photo-1549719386-74dfcbf7dbed?w=400" },
              { name: "Carrera", image: "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=400" },
              { name: "Artes marciales", image: "https://images.unsplash.com/photo-1555597673-b21d5c935865?w=400" },
              { name: "Barbería", image: "https://images.unsplash.com/photo-1585747860715-2ba37e788b70?w=400" },
              { name: "Spa", image: "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=400" },
              { name: "Fiesta", image: "https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?w=400" },
            ].map((cat, i) => (
              <div 
                key={i}
                ref={observe}
                className={`animate-on-scroll relative rounded-2xl overflow-hidden cursor-pointer group`}
                style={{ transitionDelay: `${i * 0.05}s` }}
                onClick={onBrowse}
              >
                <div className="aspect-square">
                  <img 
                    src={cat.image} 
                    alt={cat.name}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                </div>
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent" />
                <div className="absolute bottom-3 left-3 right-3">
                  <p className="text-white font-semibold text-sm md:text-base">{cat.name}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 bg-gray-50 overflow-hidden">
        <div className="max-w-6xl mx-auto px-4">
          <h2 ref={observe} className="animate-fade-up text-3xl font-bold text-center mb-12">Cómo funciona NextBooking Col</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div ref={observe} className="animate-on-scroll stagger-1 text-center">
              <div className="w-20 h-20 mx-auto mb-6 bg-blue-100 rounded-full flex items-center justify-center">
                <CreditCard className="w-10 h-10 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Sistema de Créditos</h3>
              <p className="text-gray-600">
                Pagas una suscripción mensual y recibes créditos que canjeas por clases o servicios. El costo en créditos varía según la popularidad del lugar y la hora.
              </p>
            </div>
            <div ref={observe} className="animate-on-scroll stagger-2 text-center">
              <div className="w-20 h-20 mx-auto mb-6 bg-blue-100 rounded-full flex items-center justify-center">
                <MapPin className="w-10 h-10 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Variedad</h3>
              <p className="text-gray-600">
                Accedes a una red de gimnasios, estudios boutique, spas y salones. No estás atado a un solo lugar.
              </p>
            </div>
            <div ref={observe} className="animate-on-scroll stagger-3 text-center">
              <div className="w-20 h-20 mx-auto mb-6 bg-blue-100 rounded-full flex items-center justify-center">
                <Calendar className="w-10 h-10 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Flexibilidad</h3>
              <p className="text-gray-600">
                Puedes combinar diferentes actividades y reservar según tu horario y preferencias, creando una rutina personalizada.
              </p>
            </div>
          </div>
        </div>
      </section>

      <div className="fixed bottom-0 left-0 right-0 bg-gradient-to-r from-yellow-500 via-yellow-400 to-yellow-500 py-2 z-40 marquee-container">
        <div className="animate-marquee inline-block">
          <span className="text-gray-900 font-semibold text-sm tracking-widest px-8">
            EL BIENESTAR ES UNA TENDENCIA
          </span>
          <span className="text-gray-900 font-semibold text-sm tracking-widest px-8">
            EL BIENESTAR ES UNA TENDENCIA
          </span>
          <span className="text-gray-900 font-semibold text-sm tracking-widest px-8">
            EL BIENESTAR ES UNA TENDENCIA
          </span>
          <span className="text-gray-900 font-semibold text-sm tracking-widest px-8">
            EL BIENESTAR ES UNA TENDENCIA
          </span>
        </div>
      </div>

      <footer className="bg-gray-900 text-white py-12 pb-16">
        <div className="max-w-6xl mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-8 h-8 rounded-full overflow-hidden flex flex-col">
                  <div className="h-1/2 bg-yellow-400"></div>
                  <div className="h-1/4 bg-blue-600"></div>
                  <div className="h-1/4 bg-red-600"></div>
                </div>
                <span className="text-lg font-bold">NextBooking Col</span>
              </div>
              <p className="text-gray-400 text-sm">
                La plataforma líder de bienestar y fitness en Colombia.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Compañía</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white">Sobre nosotros</a></li>
                <li><a href="#" className="hover:text-white">Carreras</a></li>
                <li><a href="#" className="hover:text-white">Prensa</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Soporte</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white">Centro de ayuda</a></li>
                <li><a href="#" className="hover:text-white">Contáctanos</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400 text-sm">
                <li><a href="#" className="hover:text-white">Términos de uso</a></li>
                <li><a href="#" className="hover:text-white">Política de privacidad</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400 text-sm">
            © 2024 NextBooking Col. Todos los derechos reservados.
          </div>
        </div>
      </footer>
    </div>
  );
};

const AuthModal = ({ 
  isOpen, 
  onClose, 
  onSuccess,
  initialTab = 'login'
}: { 
  isOpen: boolean;
  onClose: () => void;
  onSuccess: (token: string) => void;
  initialTab?: 'login' | 'register';
}) => {
  const [tab, setTab] = useState<'login' | 'register'>(initialTab);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    full_name: '',
    phone: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const endpoint = tab === 'login' ? '/api/auth/login' : '/api/auth/register';
      const body = tab === 'login' 
        ? { email: formData.email, password: formData.password }
        : formData;

      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error en la autenticación');
      }

      const data = await response.json();
      localStorage.setItem('token', data.access_token);
      onSuccess(data.access_token);
      toast.success(tab === 'login' ? '¡Bienvenido de vuelta!' : '¡Cuenta creada exitosamente!');
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Error en la autenticación');
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 rounded-full overflow-hidden flex flex-col">
              <div className="h-1/2 bg-yellow-400"></div>
              <div className="h-1/4 bg-blue-600"></div>
              <div className="h-1/4 bg-red-600"></div>
            </div>
          </div>
          <DialogTitle className="text-center text-2xl">
            {tab === 'login' ? 'Iniciar sesión' : 'Crear cuenta'}
          </DialogTitle>
          <DialogDescription className="text-center">
            {tab === 'login' 
              ? 'Ingresa a tu cuenta de NextBooking Col' 
              : 'Únete a NextBooking Col y obtén 20 créditos gratis'}
          </DialogDescription>
        </DialogHeader>

        <Tabs value={tab} onValueChange={(v) => setTab(v as 'login' | 'register')}>
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="login">Iniciar sesión</TabsTrigger>
            <TabsTrigger value="register">Registrarse</TabsTrigger>
          </TabsList>

          <form onSubmit={handleSubmit} className="space-y-4 mt-4">
            {tab === 'register' && (
              <>
                <div>
                  <Label htmlFor="full_name">Nombre completo</Label>
                  <Input
                    id="full_name"
                    value={formData.full_name}
                    onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                    placeholder="Tu nombre"
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="phone">Teléfono</Label>
                  <Input
                    id="phone"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    placeholder="+57 300 123 4567"
                  />
                </div>
              </>
            )}
            <div>
              <Label htmlFor="email">Correo electrónico</Label>
              <Input
                id="email"
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="tu@email.com"
                required
              />
            </div>
            <div>
              <Label htmlFor="password">Contraseña</Label>
              <Input
                id="password"
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                placeholder="********"
                required
              />
            </div>
            <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700" disabled={loading}>
              {loading ? 'Cargando...' : (tab === 'login' ? 'Iniciar sesión' : 'Crear cuenta')}
            </Button>
          </form>
        </Tabs>
      </DialogContent>
    </Dialog>
  );
};

const SearchPage = ({
  user,
  onLogout,
  onSelectBusiness,
  onViewProfile
}: {
  user: UserType | null;
  onLogout: () => void;
  onSelectBusiness: (business: Business) => void;
  onViewProfile: () => void;
}) => {
  const [businesses, setBusinesses] = useState<Business[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [selectedCity, setSelectedCity] = useState<string>('');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  const cities = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena'];

  useEffect(() => {
    fetchCategories();
    fetchBusinesses();
  }, [selectedCategory, selectedCity]);

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${API_URL}/api/categories`);
      const data = await response.json();
      setCategories(data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchBusinesses = async () => {
    setLoading(true);
    try {
      let url = `${API_URL}/api/businesses`;
      const params = new URLSearchParams();
      if (selectedCategory) params.append('category', selectedCategory);
      if (selectedCity) params.append('city', selectedCity);
      if (params.toString()) url += `?${params.toString()}`;

      const response = await fetch(url);
      const data = await response.json();
      setBusinesses(data);
    } catch (error) {
      console.error('Error fetching businesses:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredBusinesses = businesses.filter(b => 
    b.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    b.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="fixed top-0 left-0 right-0 bg-white z-50 border-b">
        <nav className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex items-center justify-between">
            <Logo />
            
            <div className="hidden md:flex items-center gap-4 flex-1 max-w-2xl mx-8">
              <div className="relative flex-1">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <Input
                  placeholder="Yoga, pilates, masajes..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="pl-10"
                />
              </div>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <Select value={selectedCity} onValueChange={setSelectedCity}>
                  <SelectTrigger className="w-48 pl-10">
                    <SelectValue placeholder="Ciudad" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">Todas las ciudades</SelectItem>
                    {cities.map(city => (
                      <SelectItem key={city} value={city}>{city}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="flex items-center gap-4">
              {user ? (
                <>
                  <div className="hidden md:flex items-center gap-2 text-sm">
                    <CreditCard className="w-4 h-4 text-blue-600" />
                    <span className="font-semibold">{user.credits} créditos</span>
                  </div>
                  <Button variant="ghost" onClick={onViewProfile}>
                    <User className="w-5 h-5 mr-2" />
                    <span className="hidden md:inline">{user.full_name}</span>
                  </Button>
                  <Button variant="ghost" size="icon" onClick={onLogout}>
                    <LogOut className="w-5 h-5" />
                  </Button>
                </>
              ) : (
                <Button className="bg-blue-600 hover:bg-blue-700">
                  Comenzar
                </Button>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2 mt-4 overflow-x-auto pb-2">
            <Button
              variant={selectedCategory === '' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setSelectedCategory('')}
              className={selectedCategory === '' ? 'bg-blue-600' : ''}
            >
              Todos
            </Button>
            {categories.map(cat => (
              <Button
                key={cat.value}
                variant={selectedCategory === cat.value ? 'default' : 'outline'}
                size="sm"
                onClick={() => setSelectedCategory(cat.value)}
                className={selectedCategory === cat.value ? 'bg-blue-600' : ''}
              >
                {categoryIcons[cat.value]}
                <span className="ml-2">{cat.label}</span>
              </Button>
            ))}
          </div>
        </nav>
      </header>

      <main className="pt-36 pb-8 px-4 max-w-7xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">
          {selectedCategory 
            ? `${categories.find(c => c.value === selectedCategory)?.label || 'Negocios'} en ${selectedCity || 'Colombia'}`
            : `Estudios de fitness y bienestar en ${selectedCity || 'Colombia'}`
          }
        </h1>

        {loading ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3, 4, 5, 6].map(i => (
              <Card key={i} className="animate-pulse">
                <div className="h-48 bg-gray-200 rounded-t-lg" />
                <CardContent className="p-4">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2" />
                  <div className="h-3 bg-gray-200 rounded w-1/2" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredBusinesses.map(business => (
              <Card 
                key={business.id} 
                className="cursor-pointer hover:shadow-lg transition-shadow overflow-hidden"
                onClick={() => onSelectBusiness(business)}
              >
                <div className="relative h-48">
                  <img
                    src={business.image_url}
                    alt={business.name}
                    className="w-full h-full object-cover"
                  />
                  <Badge className="absolute top-3 left-3 bg-white text-gray-800">
                    {categories.find(c => c.value === business.category)?.label}
                  </Badge>
                </div>
                <CardContent className="p-4">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-semibold text-lg">{business.name}</h3>
                      <p className="text-sm text-gray-500 flex items-center gap-1">
                        <MapPin className="w-4 h-4" />
                        {business.address}, {business.city}
                      </p>
                    </div>
                    <div className="flex items-center gap-1 text-sm">
                      <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
                      <span className="font-semibold">{business.rating}</span>
                    </div>
                  </div>
                  <p className="text-sm text-gray-600 mt-2 line-clamp-2">
                    {business.description}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {!loading && filteredBusinesses.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No se encontraron negocios con los filtros seleccionados.</p>
          </div>
        )}
      </main>
    </div>
  );
};

const BusinessDetailPage = ({
  business,
  user,
  onBack,
  onLogin,
  onBookingSuccess
}: {
  business: Business;
  user: UserType | null;
  onBack: () => void;
  onLogin: () => void;
  onBookingSuccess: () => void;
}) => {
  const [services, setServices] = useState<Service[]>([]);
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [scheduleSlots, setScheduleSlots] = useState<ScheduleSlot[]>([]);
  const [selectedDate, setSelectedDate] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [bookingLoading, setBookingLoading] = useState(false);

  const dates = Array.from({ length: 7 }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() + i);
    return date.toISOString().split('T')[0];
  });

  useEffect(() => {
    fetchServices();
  }, [business.id]);

  useEffect(() => {
    if (selectedService) {
      fetchSchedule();
    }
  }, [selectedService, selectedDate]);

  const fetchServices = async () => {
    try {
      const response = await fetch(`${API_URL}/api/businesses/${business.id}/services`);
      const data = await response.json();
      setServices(data);
      if (data.length > 0) {
        setSelectedService(data[0]);
      }
    } catch (error) {
      console.error('Error fetching services:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchSchedule = async () => {
    if (!selectedService) return;
    try {
      let url = `${API_URL}/api/services/${selectedService.id}/schedule`;
      if (selectedDate) url += `?date=${selectedDate}`;
      const response = await fetch(url);
      const data = await response.json();
      setScheduleSlots(data);
    } catch (error) {
      console.error('Error fetching schedule:', error);
    }
  };

  const handleBooking = async (slot: ScheduleSlot) => {
    if (!user) {
      onLogin();
      return;
    }

    if (!selectedService) return;

    if (user.credits < selectedService.credits_cost) {
      toast.error(`Créditos insuficientes. Necesitas ${selectedService.credits_cost} créditos.`);
      return;
    }

    setBookingLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/bookings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          service_id: selectedService.id,
          schedule_slot_id: slot.id
        })
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Error al crear la reserva');
      }

      toast.success('¡Reserva creada exitosamente!');
      onBookingSuccess();
      fetchSchedule();
    } catch (error) {
      toast.error(error instanceof Error ? error.message : 'Error al crear la reserva');
    } finally {
      setBookingLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr + 'T00:00:00');
    const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
    const months = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'];
    return `${days[date.getDay()]} ${date.getDate()} ${months[date.getMonth()]}`;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="fixed top-0 left-0 right-0 bg-white z-50 border-b">
        <nav className="max-w-7xl mx-auto px-4 py-3 flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={onBack}>
            <X className="w-6 h-6" />
          </Button>
          <Logo />
        </nav>
      </header>

      <div className="pt-16 h-64 md:h-80 relative">
        <img
          src={business.image_url}
          alt={business.name}
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
        <div className="absolute bottom-4 left-4 text-white">
          <h1 className="text-3xl font-bold">{business.name}</h1>
          <p className="flex items-center gap-2 mt-1">
            <MapPin className="w-4 h-4" />
            {business.address}, {business.city}
          </p>
          <div className="flex items-center gap-2 mt-1">
            <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
            <span className="font-semibold">{business.rating}</span>
          </div>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle>Acerca de</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">{business.description}</p>
                <div className="mt-4 space-y-2">
                  <p className="flex items-center gap-2 text-sm">
                    <MapPin className="w-4 h-4 text-gray-400" />
                    {business.address}, {business.city}, {business.country}
                  </p>
                  <p className="flex items-center gap-2 text-sm">
                    <span className="text-gray-400">Tel:</span>
                    {business.phone}
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card className="mt-6">
              <CardHeader>
                <CardTitle>Servicios disponibles</CardTitle>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="space-y-4">
                    {[1, 2, 3].map(i => (
                      <div key={i} className="animate-pulse h-20 bg-gray-100 rounded" />
                    ))}
                  </div>
                ) : (
                  <div className="space-y-3">
                    {services.map(service => (
                      <div
                        key={service.id}
                        className={`p-4 rounded-lg border-2 cursor-pointer transition-colors ${
                          selectedService?.id === service.id 
                            ? 'border-blue-600 bg-blue-50' 
                            : 'border-gray-200 hover:border-gray-300'
                        }`}
                        onClick={() => setSelectedService(service)}
                      >
                        <div className="flex items-start justify-between">
                          <div>
                            <h4 className="font-semibold">{service.name}</h4>
                            <p className="text-sm text-gray-600">{service.description}</p>
                            <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
                              <span className="flex items-center gap-1">
                                <Clock className="w-4 h-4" />
                                {service.duration_minutes} min
                              </span>
                              <span className="flex items-center gap-1">
                                <Users className="w-4 h-4" />
                                {service.max_capacity} {service.max_capacity === 1 ? 'persona' : 'personas'}
                              </span>
                            </div>
                          </div>
                          <div className="text-right">
                            <Badge className="bg-blue-600">
                              {service.credits_cost} créditos
                            </Badge>
                            {service.price_cop > 0 && (
                              <p className="text-sm text-gray-500 mt-1">
                                ${service.price_cop.toLocaleString('es-CO')} COP
                              </p>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          <div>
            <Card className="sticky top-24">
              <CardHeader>
                <CardTitle>Reservar</CardTitle>
                {selectedService && (
                  <CardDescription>
                    {selectedService.name} - {selectedService.credits_cost} créditos
                    {selectedService.price_cop > 0 && ` ($${selectedService.price_cop.toLocaleString('es-CO')} COP)`}
                  </CardDescription>
                )}
              </CardHeader>
              <CardContent>
                <div className="mb-4">
                  <Label className="mb-2 block">Selecciona una fecha</Label>
                  <div className="flex gap-2 overflow-x-auto pb-2">
                    {dates.map(date => (
                      <Button
                        key={date}
                        variant={selectedDate === date ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => setSelectedDate(date)}
                        className={`flex-shrink-0 ${selectedDate === date ? 'bg-blue-600' : ''}`}
                      >
                        {formatDate(date)}
                      </Button>
                    ))}
                  </div>
                </div>

                <div>
                  <Label className="mb-2 block">Horarios disponibles</Label>
                  {scheduleSlots.length > 0 ? (
                    <div className="grid grid-cols-3 gap-2">
                      {scheduleSlots.slice(0, 9).map(slot => (
                        <Button
                          key={slot.id}
                          variant="outline"
                          size="sm"
                          onClick={() => handleBooking(slot)}
                          disabled={bookingLoading || slot.available_spots === 0}
                          className="text-sm"
                        >
                          {slot.start_time}
                          {slot.available_spots < slot.total_spots && (
                            <span className="text-xs text-gray-400 ml-1">
                              ({slot.available_spots})
                            </span>
                          )}
                        </Button>
                      ))}
                    </div>
                  ) : (
                    <p className="text-sm text-gray-500 text-center py-4">
                      {selectedDate 
                        ? 'No hay horarios disponibles para esta fecha' 
                        : 'Selecciona una fecha para ver horarios'}
                    </p>
                  )}
                </div>

                {user && (
                  <div className="mt-4 p-3 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600">
                      Tus créditos: <span className="font-semibold text-blue-600">{user.credits}</span>
                    </p>
                  </div>
                )}

                {!user && (
                  <Button 
                    className="w-full mt-4 bg-blue-600 hover:bg-blue-700"
                    onClick={onLogin}
                  >
                    Inicia sesión para reservar
                  </Button>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
};

const ProfilePage = ({
  user,
  onBack,
  onLogout,
  onRefreshUser
}: {
  user: UserType;
  onBack: () => void;
  onLogout: () => void;
  onRefreshUser: () => void;
}) => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [plans, setPlans] = useState<SubscriptionPlan[]>([]);
  const [loading, setLoading] = useState(true);
  const [subscribing, setSubscribing] = useState(false);

  useEffect(() => {
    fetchBookings();
    fetchPlans();
  }, []);

  const fetchBookings = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/bookings`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setBookings(data);
    } catch (error) {
      console.error('Error fetching bookings:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPlans = async () => {
    try {
      const response = await fetch(`${API_URL}/api/subscriptions`);
      const data = await response.json();
      setPlans(data);
    } catch (error) {
      console.error('Error fetching plans:', error);
    }
  };

  const handleSubscribe = async (plan: string) => {
    setSubscribing(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/subscriptions/${plan}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) {
        throw new Error('Error al suscribirse');
      }

      toast.success('¡Suscripción exitosa! Tus créditos han sido actualizados.');
      onRefreshUser();
    } catch (error) {
      toast.error('Error al procesar la suscripción');
    } finally {
      setSubscribing(false);
    }
  };

  const handleCancelBooking = async (bookingId: string) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/bookings/${bookingId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (!response.ok) {
        throw new Error('Error al cancelar la reserva');
      }

      toast.success('Reserva cancelada. Créditos reembolsados.');
      fetchBookings();
      onRefreshUser();
    } catch (error) {
      toast.error('Error al cancelar la reserva');
    }
  };

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 0
    }).format(price);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="fixed top-0 left-0 right-0 bg-white z-50 border-b">
        <nav className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="icon" onClick={onBack}>
              <X className="w-6 h-6" />
            </Button>
            <Logo />
          </div>
          <Button variant="ghost" onClick={onLogout}>
            <LogOut className="w-5 h-5 mr-2" />
            Cerrar sesión
          </Button>
        </nav>
      </header>

      <main className="pt-24 pb-8 px-4 max-w-4xl mx-auto">
        <Card className="mb-8">
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
                <User className="w-8 h-8 text-blue-600" />
              </div>
              <div>
                <h2 className="text-2xl font-bold">{user.full_name}</h2>
                <p className="text-gray-500">{user.email}</p>
              </div>
            </div>
            <div className="mt-6 p-4 bg-blue-50 rounded-lg flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Créditos disponibles</p>
                <p className="text-3xl font-bold text-blue-600">{user.credits}</p>
              </div>
              {user.subscription_plan && (
                <Badge className="bg-blue-600 text-lg px-4 py-2">
                  Plan {user.subscription_plan.charAt(0).toUpperCase() + user.subscription_plan.slice(1)}
                </Badge>
              )}
            </div>
          </CardContent>
        </Card>

        <h3 className="text-xl font-bold mb-4">Comprar créditos</h3>
        <div className="max-w-md mb-8">
          {plans.map(plan => (
            <Card 
              key={plan.plan}
              className={`${user.subscription_plan === plan.plan ? 'border-2 border-blue-600' : 'border-2 border-gray-200'}`}
            >
              <CardHeader className="text-center">
                <CardTitle className="text-2xl">
                  20 Créditos
                  {user.subscription_plan === plan.plan && (
                    <Badge className="bg-blue-600 ml-2">Activo</Badge>
                  )}
                </CardTitle>
                <CardDescription>
                  <span className="text-3xl font-bold text-gray-900">{formatPrice(plan.price_usd)}</span>
                  <span className="text-gray-500"> COP</span>
                </CardDescription>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2 mb-4">
                  {plan.features.map((feature, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm">
                      <Check className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
                      {feature}
                    </li>
                  ))}
                </ul>
                <Button
                  className="w-full bg-blue-600 hover:bg-blue-700"
                  disabled={subscribing || user.subscription_plan === plan.plan}
                  onClick={() => handleSubscribe(plan.plan)}
                >
                  {user.subscription_plan === plan.plan ? 'Ya tienes este plan' : 'Comprar créditos'}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        <h3 className="text-xl font-bold mb-4">Mis reservas</h3>
        {loading ? (
          <div className="space-y-4">
            {[1, 2, 3].map(i => (
              <div key={i} className="animate-pulse h-24 bg-gray-100 rounded" />
            ))}
          </div>
        ) : bookings.length > 0 ? (
          <div className="space-y-4">
            {bookings.map(booking => (
              <Card key={booking.id}>
                <CardContent className="pt-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-semibold">{booking.service_name}</h4>
                      <p className="text-sm text-gray-500">{booking.business_name}</p>
                      <div className="flex items-center gap-4 mt-2 text-sm">
                        <span className="flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {booking.date}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {booking.start_time}
                        </span>
                        <Badge variant={booking.status === 'confirmed' ? 'default' : 'secondary'}>
                          {booking.status === 'confirmed' ? 'Confirmada' : 
                           booking.status === 'cancelled' ? 'Cancelada' : booking.status}
                        </Badge>
                      </div>
                    </div>
                    {booking.status === 'confirmed' && (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleCancelBooking(booking.id)}
                      >
                        Cancelar
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <CardContent className="py-8 text-center">
              <Calendar className="w-12 h-12 mx-auto text-gray-300 mb-4" />
              <p className="text-gray-500">No tienes reservas aún</p>
              <Button className="mt-4" onClick={onBack}>
                Explorar servicios
              </Button>
            </CardContent>
          </Card>
        )}
      </main>
    </div>
  );
};

const CitySelector = ({ onSelectCity }: { onSelectCity: (city: string) => void }) => {
  const cities = [
    { name: "Duitama", image: "https://images.unsplash.com/photo-1518105779142-d975f22f1b0a?w=800" },
    { name: "Tunja", image: "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800" },
    { name: "Sogamoso", image: "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800" },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col items-center justify-center p-4">
      <div className="text-center mb-12">
        <div className="flex justify-center mb-6">
          <div className="w-20 h-20 rounded-full overflow-hidden border-4 border-white shadow-lg flex flex-col">
            <div className="h-1/2 bg-yellow-400"></div>
            <div className="h-1/4 bg-blue-600"></div>
            <div className="h-1/4 bg-red-600"></div>
          </div>
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-2">NextBooking Col</h1>
        <p className="text-xl text-gray-600">Selecciona tu ciudad</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl w-full">
        {cities.map((city) => (
          <button
            key={city.name}
            onClick={() => onSelectCity(city.name)}
            className="group relative rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-105"
          >
            <div className="aspect-video">
              <img 
                src={city.image} 
                alt={city.name}
                className="w-full h-full object-cover"
              />
            </div>
            <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
            <div className="absolute bottom-0 left-0 right-0 p-6">
              <h3 className="text-2xl font-bold text-white">{city.name}</h3>
              <p className="text-white/80 text-sm mt-1">Boyacá, Colombia</p>
            </div>
          </button>
        ))}
      </div>
    </div>
  );
};

function App() {
  const [page, setPage] = useState<'city' | 'landing' | 'search' | 'business' | 'profile'>('city');
  const [, setSelectedCity] = useState<string | null>(null);
  const [user, setUser] = useState<UserType | null>(null);
  const [selectedBusiness, setSelectedBusiness] = useState<Business | null>(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [authModalTab, setAuthModalTab] = useState<'login' | 'register'>('login');

  useEffect(() => {
    const token = localStorage.getItem('token');
    const savedCity = localStorage.getItem('selectedCity');
    if (token) {
      fetchUser(token);
    }
    if (savedCity) {
      setSelectedCity(savedCity);
      setPage('landing');
    }
  }, []);

  const fetchUser = async (token: string) => {
    try {
      const response = await fetch(`${API_URL}/api/auth/me`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setUser(data);
      } else {
        localStorage.removeItem('token');
      }
    } catch (error) {
      console.error('Error fetching user:', error);
    }
  };

  const handleAuthSuccess = (token: string) => {
    fetchUser(token);
    setShowAuthModal(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setPage('landing');
    toast.success('Sesión cerrada');
  };

  const handleGetStarted = () => {
    setAuthModalTab('register');
    setShowAuthModal(true);
  };

  const handleLogin = () => {
    setAuthModalTab('login');
    setShowAuthModal(true);
  };

  const handleSelectBusiness = (business: Business) => {
    setSelectedBusiness(business);
    setPage('business');
  };

  const handleRefreshUser = () => {
    const token = localStorage.getItem('token');
    if (token) {
      fetchUser(token);
    }
  };

  const handleSelectCity = (city: string) => {
    setSelectedCity(city);
    localStorage.setItem('selectedCity', city);
    setPage('landing');
  };

  return (
    <>
      <Toaster position="top-center" />
      
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onSuccess={handleAuthSuccess}
        initialTab={authModalTab}
      />

      {page === 'city' && (
        <CitySelector onSelectCity={handleSelectCity} />
      )}

      {page === 'landing' && (
        <LandingPage
          onGetStarted={handleGetStarted}
          onLogin={handleLogin}
          onBrowse={() => setPage('search')}
        />
      )}

      {page === 'search' && (
        <SearchPage
          user={user}
          onLogout={handleLogout}
          onSelectBusiness={handleSelectBusiness}
          onViewProfile={() => setPage('profile')}
        />
      )}

      {page === 'business' && selectedBusiness && (
        <BusinessDetailPage
          business={selectedBusiness}
          user={user}
          onBack={() => setPage('search')}
          onLogin={handleLogin}
          onBookingSuccess={handleRefreshUser}
        />
      )}

      {page === 'profile' && user && (
        <ProfilePage
          user={user}
          onBack={() => setPage('search')}
          onLogout={handleLogout}
          onRefreshUser={handleRefreshUser}
        />
      )}
    </>
  );
}

export default App;
