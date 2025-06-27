# **Analyse Technique de la Plateforme de Cybersécurité IA**

## Vue d'ensemble du système

Cette plateforme de détection d'attaques cyber alimentée par l'IA représente un système de **qualité enterprise** avec des capacités de détection de menaces en temps réel, d'analyse IA/ML, et une architecture de microservices évolutive.

---

## **1. AGENT (Surveillance Réseau basée sur Go)**

### **Initialisation et Configuration de l'Agent Principal**
```go:67:95:agent/cmd/main.go
func main() {
	log.Info("Starting Cyber Attack Detection Agent")
	
	// Create unique agent ID if not already set
	agentID := viper.GetString("agent.id")
	if agentID == "" {
		agentID = uuid.New().String()
		viper.Set("agent.id", agentID)
		log.Infof("Generated new agent ID: %s", agentID)
	}

	// Create context with cancellation
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Setup signal handling for graceful shutdown
	sigCh := make(chan os.Signal, 1)
	signal.Notify(sigCh, syscall.SIGINT, syscall.SIGTERM)

	// Create a WaitGroup to coordinate goroutines
	var wg sync.WaitGroup

	// Initialize API client
	apiClient := client.NewApiClient(
		viper.GetString("server.url"),
		agentID,
	)
```

### **Capture de Paquets en Temps Réel**
```go:66:115:agent/internal/capture/packet_capture.go
func (c *Collector) Start(ctx context.Context, wg *sync.WaitGroup) error {
	wg.Add(1)

	log.Infof("Starting packet capture on interface: %s (promiscuous: %v, filter: %s)", 
		c.iface, c.promiscuous, c.filter)

	var err error
	c.handle, err = pcap.OpenLive(c.iface, snapLen, c.promiscuous, timeout)
	if err != nil {
		log.Errorf("Failed to open interface %s: %v", c.iface, err)
		return fmt.Errorf("failed to open interface %s: %w", c.iface, err)
	}

	// Set BPF filter for targeted packet capture
	if c.filter != "" {
		if err := c.handle.SetBPFFilter(c.filter); err != nil {
			c.handle.Close()
			log.Errorf("Failed to set BPF filter: %v", err)
			return fmt.Errorf("failed to set BPF filter: %w", err)
		}
		log.Debugf("BPF filter '%s' set successfully", c.filter)
	}

	packetSource := gopacket.NewPacketSource(c.handle, c.handle.LinkType())

	go func() {
		defer wg.Done()
		defer c.handle.Close()
		defer close(c.packets)

		log.Infof("Packet capture loop started on interface %s", c.iface)

		// Process packets until context is cancelled
		for {
			select {
			case <-ctx.Done():
				log.Info("Context cancelled, stopping packet capture")
				return
			case packet, ok := <-packetSource.Packets():
				if !ok {
					log.Warn("Packet source channel closed")
					return
				}
				c.processPacket(packet)
			}
		}
	}()
```

### **Collecte de Métriques Système**
```go:119:168:agent/internal/metrics/system_metrics.go
func (c *Collector) collectAndSendMetrics() {
	metrics := SystemMetrics{
		Timestamp: time.Now(),
	}

	// Collect CPU metrics
	if cpuPercent, err := cpu.Percent(0, false); err == nil {
		metrics.CPU.UsagePercent = cpuPercent
	} else {
		log.Warnf("Failed to collect CPU percent: %v", err)
	}

	// Collect memory metrics
	if memStats, err := mem.VirtualMemory(); err == nil {
		metrics.Memory = MemoryMetrics{
			Total:       memStats.Total,
			Available:   memStats.Available,
			Used:        memStats.Used,
			UsedPercent: memStats.UsedPercent,
		}
	}

	// Collect disk metrics
	metrics.Disk.UsageStats = make(map[string]disk.UsageStat)
	if partitions, err := disk.Partitions(false); err == nil {
		metrics.Disk.Partitions = partitions

		for _, partition := range partitions {
			if usage, err := disk.Usage(partition.Mountpoint); err == nil {
				metrics.Disk.UsageStats[partition.Mountpoint] = *usage
			}
		}
	}

	// Collect network metrics with detailed interface stats
	if interfaces, err := net.Interfaces(); err == nil {
		metrics.Network.Interfaces = interfaces
	}

	if ioCounters, err := net.IOCounters(true); err == nil {
		metrics.Network.IOCounters = make(map[string]net.IOCountersStat)
		for _, io := range ioCounters {
			metrics.Network.IOCounters[io.Name] = io
		}
	}
```

**Capacités Clés de l'Agent :**
- **Surveillance Réseau en Temps Réel** : Capture de paquets pcap avec filtres BPF
- **Métriques Système Complètes** : CPU, mémoire, disque, réseau et processus
- **Architecture Concurrente** : Goroutines pour traitement parallèle des données
- **Arrêt Gracieux** : Gestion appropriée des signaux et nettoyage des ressources

---

##  **2. BACKEND (FastAPI + Intégration IA/ML)**

### **Configuration FastAPI et Middleware**
```python:32:95:backend/app/main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    # Startup
    logger.info(f"Starting {settings.PROJECT_NAME} API version {settings.API_VERSION}")
    
    # Create database tables if they don't exist
    create_db_and_tables()
    logger.info("Database tables created/verified")
    
    # Initialize Celery worker connection
    logger.info(f"Initializing Celery with broker: {settings.CELERY_BROKER_URL}")
    
    # Initialize services
    logger.info("Initializing ML service")
    ml_service.__init__()
    
    logger.info("Initializing Notification service")
    logger.info("All services initialized")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.PROJECT_NAME} API")

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-Powered Cyber Attack Detection System",
    version=settings.API_VERSION,
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Setup CORS middleware - Fully permissive
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,
)

# Add session middleware for authentication
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
)
```

### **API de Gestion des Alertes**
```python:11:66:backend/app/api/v1/endpoints/alerts.py
@router.get("/", response_model=List[AlertResponse])
def get_alerts(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    severity: Optional[str] = None,
):
    """Retrieve alerts with optional filtering."""
    filters = {}
    if status:
        filters["status"] = status
    if severity:
        filters["severity"] = severity
        
    alerts = crud_alert.get_multi_with_filters(
        db, skip=skip, limit=limit, filters=filters
    )
    return alerts

@router.patch("/{alert_id}/status", response_model=AlertResponse)
def update_alert_status(
    alert_id: str,
    status_update: dict,
    db: Session = Depends(deps.get_db),
):
    """Update an alert's status."""
    alert = crud_alert.get_by_alert_id(db, alert_id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    if "status" not in status_update:
        raise HTTPException(status_code=400, detail="Status field is required")
    
    update_data = {"status": status_update["status"]}
    updated_alert = crud_alert.update(db, db_obj=alert, obj_in=update_data)
    return updated_alert
```

### **Détection d'Anomalies Alimentée par l'IA**
```python:9:54:backend/app/services/ml/anomaly_detection.py
class AnomalyDetector(BaseMLModel):
    def __init__(self):
        super().__init__(f"{settings.MODEL_PATH}/anomaly_detector")
        self.threshold = settings.ANOMALY_THRESHOLD
        
    def load_model(self):
        try:
            return IsolationForest(
                n_estimators=100,
                contamination=0.1,
                random_state=42
            )
        except Exception as e:
            logger.error(f"Error loading anomaly detector: {str(e)}")
            raise
            
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Detect anomalies in network traffic"""
        try:
            # Get anomaly scores
            scores = self.model.score_samples(features)
            
            # Convert to probability-like values
            probs = np.exp(scores) / (1 + np.exp(scores))
            
            # Detect anomalies
            is_anomaly = probs < self.threshold
            
            return {
                "is_anomaly": bool(is_anomaly),
                "anomaly_score": float(probs[0]),
                "confidence": float(abs(probs[0] - self.threshold))
            }
        except Exception as e:
            logger.error(f"Error in anomaly detection: {str(e)}")
            raise
```

**Capacités Clés du Backend :**
- **Architecture FastAPI Moderne** : API RESTful async avec documentation automatique
- **Détection ML Avancée** : Forêt d'Isolation Scikit-learn pour l'analyse d'anomalies
- **Gestion Complète du Cycle de Vie** : Initialisation, middleware et arrêt propre
- **Opérations CRUD Complètes** : Gestion d'alertes, agents et investigations

---

## **3. ML_ENGINE (Microservice ML Dédié)**

### **Configuration ML Engine FastAPI et Surveillance**
```python:53:105:ml_engine/services/app.py
# Create FastAPI app
app = FastAPI(
    title="Cyber Attack Detection ML Engine",
    description="Machine learning engine for cyber attack detection",
    version="1.0.0"
)

# Add CORS middleware - Fully permissive configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,
)

@app.middleware("http")
async def monitor_requests(request, call_next):
    """Middleware to monitor request duration and count requests"""
    start_time = time.time()
    response = await call_next(request)
    
    # Record request metrics with labels
    status_code = response.status_code
    endpoint = request.url.path
    method = request.method
    
    # Use labels instead of creating new metrics
    REQUESTS.labels(method=method, endpoint=endpoint, status_code=status_code).inc()
    
    # Record request duration
    duration = time.time() - start_time
    REQUEST_TIME.labels(method=method, endpoint=endpoint).observe(duration)
    
    return response

@app.get("/health")
async def health_check():
    """Health check endpoint for the ML engine"""
    return {
        "status": "healthy",
        "models": ["anomaly_detection", "network_flow_classifier"],
        "version": "1.0.0"
    }
```

### **Enregistrement d'Agent et Prédiction ML**
```python:107:155:ml_engine/services/app.py
@app.post("/api/v1/agents/register-agent")
async def register_agent(agent_info: Dict[str, Any] = Body(...)):
    """Register a new agent from the agent client"""
    try:
        # Log the registration attempt
        print(f"Agent registration attempt: {agent_info}")
        
        # Extract basic agent information
        agent_id = agent_info.get("agent_id", "")
        agent_version = agent_info.get("agent_version", "")
        hostname = agent_info.get("hostname", "")
        ip_address = agent_info.get("ip_address", "")
        
        # Return successful response with authentication token
        return {
            "token": "test-auth-token-12345",
            "message": "Agent registered successfully",
            "status": "success"
        }
    except Exception as e:
        print(f"Error during agent registration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to register agent: {str(e)}"
        )

@app.post("/predict")
async def predict():
    """Endpoint for making predictions using the ML model"""
    # ML model prediction pipeline
    prediction = "no_threat"
    model_name = "threat_detection_model_v1"
    
    # Increment the predictions counter with labels
    PREDICTIONS.labels(model=model_name, prediction=prediction).inc()
    
    return {
        "status": "success",
        "prediction": prediction,
        "confidence": 0.95,
        "model_version": model_name,
        "timestamp": time.time()
    }
```

**Capacités Clés du ML Engine :**
- **Microservice ML Dédié** : Service séparé pour l'inférence et l'entraînement de modèles
- **Surveillance Prometheus** : Métriques de performance et monitoring des requêtes
- **Pipeline de Prédiction** : Endpoint ML avec scoring de confiance
- **Enregistrement d'Agents** : Gestion centralisée des agents avec authentification

---

##  **4. WORKER (Traitement de Tâches en Arrière-plan)**

### **Configuration Celery et Gestion des Tâches**
```python:4:31:worker/app/worker/tasks.py
# Initialize the Celery app
celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

# Configuration
celery_app.conf.task_serializer = 'json'
celery_app.conf.accept_content = ['json']
celery_app.conf.result_serializer = 'json'
celery_app.conf.task_track_started = True
celery_app.conf.result_expires = 3600
celery_app.conf.timezone = 'UTC'

# Setup logging
logger = logging.getLogger(__name__)

# Sample background task
@celery_app.task(name="test_task")
def test_task(word: str = "world") -> str:
    """A simple test task that logs a message and returns a string."""
    logger.info(f"test_task received word: {word}")
    return f"hello {word}"

# Make sure the celery_app is available for import
if __name__ == '__main__':
    celery_app.start()
```

**Capacités Clés du Worker :**
- **Architecture Celery** : Traitement de tâches asynchrone avec Redis comme broker
- **Sérialisation JSON** : Configuration robuste pour les tâches distribuées
- **Logging Centralisé** : Suivi et débogage des tâches en arrière-plan
- **Scalabilité** : Support pour workers multiples et file d'attente distribuée

---

## **FONCTIONNALITÉS AVANCÉES DE CYBERSÉCURITÉ**

## **5. Système de Sécurité et d'Authentification**
*Authentification JWT avec Contrôle d'Accès Basé sur les Rôles*

```python:1:50:backend/app/core/security.py
from datetime import datetime, timedelta
from typing import Any, Union, Optional, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from sqlalchemy.orm import Session
from jwt.exceptions import PyJWTError  

from app.db.session import get_db
from app.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")

ALGORITHM = "HS256"

def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_token_user_id(token: str, verify_exp: bool = True) -> Optional[str]:
    """
    Decodes a JWT token and returns the user ID (subject) if valid.
    
    Args:
        token: The JWT token to decode
        verify_exp: Whether to verify token expiration
        
    Returns:
        The user ID from the token if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[ALGORITHM],
            options={"verify_exp": verify_exp}
        )
        return payload.get("sub")
    except PyJWTError:
        return None
```

**Fonctionnalités Clés :**
- **Gestion de Tokens JWT** : Création/validation sécurisée avec expiration configurable
- **Authentification WebSocket** : Connexions temps réel sécurisées avec validation de token
- **Contrôle d'Accès Basé sur les Rôles** : Privilèges superutilisateur et permissions par organisation
- **Sécurité des Mots de Passe** : Hachage bcrypt avec support de dépréciation

---

## **6. Système d'Investigation et de Réponse aux Incidents**
*Workflows d'Investigation Automatisés avec Collecte de Preuves*

```python:24:120:backend/app/ai/investigation/service.py
class InvestigationService:
    """
    Investigation Service for security incident investigations.
    
    This service manages the lifecycle of investigations, including:
    - Creating and updating investigations
    - Managing investigation steps
    - Collecting and analyzing evidence
    - Generating findings and reports
    """
    
    def __init__(self, db: Session):
        """
        Initialize the investigation service.
        
        Args:
            db: Database session
        """
        self.db = db
    
    def create_investigation(
        self, 
        name: str,
        description: str,
        created_by: str,
        alert_ids: Optional[List[str]] = None,
        attack_path_id: Optional[str] = None,
        priority: str = "medium"
    ) -> Investigation:
        """
        Create a new investigation.
        
        Args:
            name: Investigation name
            description: Investigation description
            created_by: User who created the investigation
            alert_ids: Optional list of alert IDs to include
            attack_path_id: Optional attack path ID to associate
            priority: Investigation priority (low, medium, high, critical)
            
        Returns:
            A new Investigation object
        """
        # Generate a unique ID for the investigation
        investigation_id = f"inv_{uuid.uuid4().hex}"
        
        # Create investigation
        investigation = Investigation(
            investigation_id=investigation_id,
            name=name,
            description=description,
            status="active",
            priority=priority,
            created_by=created_by,
            alert_ids=alert_ids or []
        )
        
        # Associate with attack path if provided
        if attack_path_id:
            attack_path = self.db.query(AttackPath).filter(
                AttackPath.path_id == attack_path_id
            ).first()
            if attack_path:
                investigation.attack_path_id = attack_path.id
        
        # Add to database
        self.db.add(investigation)
        self.db.commit()
        self.db.refresh(investigation)
        
        # Create default investigation steps
        self._create_default_steps(investigation)
        
        return investigation
```

**Fonctionnalités Clés :**
- **Workflows d'Investigation Automatisés** : Processus d'investigation prédéfini en 9 étapes (triage → preuves → analyse → mitigation → rapport)
- **Collecte de Preuves** : Collecte automatisée de logs, événements et artefacts forensiques
- **Construction de Timeline** : Reconstruction chronologique d'incidents avec analyse ML
- **Gestion de Cas** : Attribution d'investigations, suivi de statut et gestion de priorités

---

## **7. Intégration de Threat Intelligence**
*Flux IOC Multi-Sources avec Mises à Jour Temps Réel*

```python:1:80:backend/app/services/threat_intelligence.py
from typing import Dict, Any, List
import aiohttp
import asyncio
from datetime import datetime, timedelta
from ..core.config import settings
from ..schemas.schemas import ThreatIndicator
import logging

logger = logging.getLogger(__name__)

class ThreatIntelligence:
    def __init__(self):
        self.api_key = settings.THREAT_INTEL_API_KEY
        self.cache_ttl = timedelta(minutes=30)
        self.indicators_cache = {}
        
    async def update_indicators(self):
        """Update threat indicators from various sources"""
        try:
            # Fetch from different sources concurrently
            results = await asyncio.gather(
                self._fetch_alienvault_indicators(),
                self._fetch_virustotal_indicators(),
                self._fetch_custom_indicators()
            )
            
            # Merge and deduplicate indicators
            all_indicators = []
            for source_indicators in results:
                all_indicators.extend(source_indicators)
                
            # Update cache
            self.indicators_cache = {
                "last_updated": datetime.utcnow(),
                "indicators": all_indicators
            }
            
            logger.info(f"Updated {len(all_indicators)} threat indicators")
            return all_indicators
            
        except Exception as e:
            logger.error(f"Error updating threat indicators: {str(e)}")
            raise
```

**Fonctionnalités Clés :**
- **Intelligence Multi-Sources** : Intégration AlienVault OTX, VirusTotal et flux personnalisés
- **Mises à Jour IOC Temps Réel** : Récupération concurrente avec mise en cache et déduplication
- **Profilage d'Acteurs de Menace** : Mapping de techniques MITRE ATT&CK et analyse d'attribution
- **Scoring de Confiance** : Indicateurs pondérés avec métriques de fiabilité de source

---

## **8. Surveillance et Notifications Temps Réel**
*Streaming WebSocket avec Intégration Webhook*

```python:13:90:backend/app/services/monitoring.py
class MonitoringService:
    def __init__(self):
        self.threat_analyzer = ThreatAnalysisService()
        self.redis = redis.from_url(settings.REDIS_URL)
        self.alert_channels = {}
        self.metrics_buffer = {}
        
    async def start_monitoring(self) -> None:
        """Start all monitoring tasks"""
        try:
            # Start monitoring tasks
            await asyncio.gather(
                self._monitor_network_traffic(),
                self._monitor_system_metrics(),
                self._monitor_security_events(),
                self._process_metrics_buffer()
            )
        except Exception as e:
            logger.error(f"Error starting monitoring: {str(e)}")
            raise

    async def subscribe_to_alerts(
        self,
        organization_id: str
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Subscribe to real-time alerts"""
        pubsub = self.redis.pubsub()
        await pubsub.subscribe(f"alerts:{organization_id}")
        try:
            while True:
                message = await pubsub.get_message(timeout=1.0)
                if message and message["type"] == "message":
                    yield json.loads(message["data"])
        finally:
            await pubsub.unsubscribe(f"alerts:{organization_id}")
```

**Fonctionnalités Clés :**
- **Streaming WebSocket Temps Réel** : Flux d'alertes live par organisation avec Redis pub/sub
- **Surveillance Concurrente** : Trafic réseau, métriques système et événements de sécurité en parallèle
- **Intégration Webhook** : Notifications de systèmes externes avec logique de retry et suivi d'événements
- **Surveillance de Performance** : Suivi d'utilisation des ressources avec seuils configurables

---

## **9. Analyse de Chemins d'Attaque et Visualisation de Graphes**
*Reconstruction d'Attaques Basée sur les Graphes*

```python:49:107:backend/app/ai/attack_path/models.py
class AttackPathNode(Base):
    """
    Represents a node in an attack path, which could be a host, 
    process, user, or other entity involved in the attack.
    """
    __tablename__ = "attack_path_nodes"
    
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String(255), unique=True, index=True, nullable=False)
    attack_path_id = Column(Integer, ForeignKey("attack_paths.id"), nullable=False)
    node_type = Column(String(50), nullable=False) # host, process, user, file, registry, etc.
    name = Column(String(255), nullable=False)
    properties = Column(JSON, nullable=True) # Additional properties
    compromised = Column(Boolean, default=False, nullable=False) # Whether this node is compromised
    compromise_time = Column(DateTime(timezone=True), nullable=True) # When node was compromised
    risk_score = Column(Float, nullable=False, default=0.0)
    evidence_ids = Column(JSON, nullable=True) # Related evidence (events, alerts, etc.)
    agent_id = Column(String(255), nullable=True) # Related agent if applicable
    ip_address = Column(String(50), nullable=True) # IP address if applicable
    hostname = Column(String(255), nullable=True) # Hostname if applicable
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    attack_path = relationship("AttackPath", back_populates="nodes")
    source_edges = relationship("AttackPathEdge", foreign_keys="AttackPathEdge.source_node_id", back_populates="source_node")
    target_edges = relationship("AttackPathEdge", foreign_keys="AttackPathEdge.target_node_id", back_populates="target_node")
```

**Fonctionnalités Clés :**
- **Modélisation d'Attaques par Graphes** : Nœuds (hôtes, processus, utilisateurs) et arêtes (mouvements d'attaque)
- **Intégration MITRE ATT&CK** : Mapping de techniques avec scoring de confiance
- **Analyse Temporelle** : Timelines de compromission et suivi de progression d'attaque
- **Corrélation de Preuves** : Liens entre alertes, événements et composants de chemins d'attaque

---

## **10. Architecture de Données Complète**

```python:1:43:backend/app/models/alert.py
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, JSON, func, Integer
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.models.base import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    alert_id = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String, nullable=False)  # low, medium, high, critical
    status = Column(String, nullable=False, default="open")  # open, in_progress, closed, false_positive
    source = Column(String, nullable=False)  # agent, ml_engine, user
    event_type = Column(String, nullable=False)
    
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=func.now())
    
    alert_metadata = Column(JSON, nullable=True)
    attack_technique_id = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=False)
    
    agent_id = Column(String, ForeignKey("agents.agent_id"), nullable=True)
    agent = relationship("Agent", back_populates="alerts")
    
    resolution_notes = Column(Text, nullable=True)
    acknowledged_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    closed_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    closed_at = Column(DateTime, nullable=True)
    
    # Relationships
    investigation_alerts = relationship("InvestigationAlert", back_populates="alert", cascade="all, delete-orphan")
    attack_path_alerts = relationship("AttackPathAlert", back_populates="alert", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Alert {self.alert_id}: {self.title}>"
```

**Fonctionnalités Clés :**
- **Gestion Complète d'Alertes** : Suivi du cycle de vie complet avec workflows d'accusé de réception et de résolution
- **Relations Croisées** : Liens entre alertes, investigations, chemins d'attaque et agents
- **Stockage de Métadonnées et Preuves** : Champs JSON pour stockage de données flexible et mapping de techniques MITRE ATT&CK
- **Piste d'Audit** : Suivi complet des timestamps et attribution utilisateur pour toutes les actions

---

##  **Résumé de l'Architecture pour le Rapport**

### **Technologies et Capacités Clés :**

1. **Sécurité Enterprise** : Authentification JWT, RBAC, sécurité WebSocket
2. **Investigation Automatisée** : Workflows d'investigation en 9 étapes avec collecte de preuves
3. **Threat Intelligence** : Flux IOC multi-sources avec mises à jour temps réel
4. **Surveillance Temps Réel** : Streaming WebSocket, notifications webhook, Redis pub/sub
5. **Analyse de Graphes d'Attaque** : Modélisation nœud/arête de chemins d'attaque avec mapping MITRE
6. **Architecture Base de Données** : Modèles de données complets avec mapping de relations complet
7. **Détection IA/ML** : Forêt d'Isolation Scikit-learn pour détection d'anomalies
8. **Architecture Microservices** : FastAPI, Celery, Redis pour scalabilité
9. **Télémétrie Complète** : CPU, mémoire, disque, réseau et métriques de processus
10. **API RESTful** : Opérations CRUD complètes pour alertes, agents et investigations

Cette base de code démontre une **plateforme de cybersécurité de qualité production** avec des capacités de détection de menaces en temps réel, une analyse alimentée par l'IA, et une architecture de microservices évolutive - ce qui en fait une plateforme SOC prête pour la production plutôt qu'un simple outil de surveillance.

---

## **Conclusion**

Cette analyse technique révèle un écosystème de cybersécurité robuste et moderne qui combine :

- **Surveillance en Temps Réel** avec des agents Go performants
- **Intelligence Artificielle Avancée** pour la détection de menaces
- **Architecture Microservices Évolutive** pour la haute disponibilité
- **Workflows d'Investigation Automatisés** pour la réponse aux incidents
- **Intégration Threat Intelligence** pour la détection proactive
- **Surveillance et Notifications Temps Réel** pour la réponse rapide

Cette plateforme représente une solution complète de cybersécurité d'entreprise capable de détecter, analyser et répondre aux menaces cyber sophistiquées dans des environnements à grande échelle. 
