# edge-AI

# 🧊 ColdStorage AI — Simulation Virtuelle d’IA Embarquée

**Projet éducatif : capteurs → MQTT → modèles IA → Edge Computing → décisions**

---

## 🎯 À propos du projet

ColdStorage AI est un projet éducatif complet permettant d’apprendre l’IA embarquée **sans matériel physique**.  

Il propose un environnement de simulation réaliste incluant :  

- Des capteurs virtuels (température, humidité, eau, lumière…)  
- Un pipeline MQTT opérationnel  
- Un STM32 simulé exécutant des modèles TensorFlow Lite  
- Plusieurs modèles d’IA embarquée  
- Un dashboard pour visualisation en temps réel  

**Objectif :** former aux compétences essentielles en IA embarquée, IoT, edge computing et intégration système.

---

## 📦 Structure du dépôt
├── simulator/ → Simulateurs (capteurs + STM32 virtuel)
├── training/ → Entraînement IA (prédiction, anomalies, optimisation)
├── utils/ → Preprocessing, conversion TFLite, outils ML
├── docker/mosquitto/ → Broker MQTT via Docker
├── dashboard/ → Dashboard Streamlit
├── tflite/ → Modèles convertis en .tflite
├── data/ → Jeux de données simulés
└── README.md → Documentation du projet


---

## 🧠 Compétences éducatives visées

Le projet couvre toutes les couches d’un système IoT + IA embarquée :

### 1. Génération et manipulation de données IoT
- Simulation de signaux capteurs réalistes  
- Introduction de bruit, dérive, anomalies  
- Construction de datasets exploitables pour le ML  

### 2. Entraînement de modèles IA embarqués
- Classification (détection de surchauffe)  
- Autoencoder (anomalies)  
- Régression (optimisation ventilateur/pompe)  
- Normalisation, validation, métriques  

### 3. Conversion TensorFlow → TFLite
- Conversion standard  
- Quantification pour microcontrôleurs  
- Tests d’inférence TFLite  

### 4. Architecture IoT (MQTT)
- Publisher / Subscriber  
- Gestion du flux temps réel  
- Déconnexion/réconnexion, buffers  

### 5. Simulation firmware microcontrôleur
- Buffer circulaire  
- Inference TFLite Micro-like  
- Automatisme : ventilateur, pompe, alertes  

### 6. Visualisation et analyse
- Dashboard temps réel  
- Inspection des anomalies  
- Monitoring des actions automatiques  

---

## 🧪 Scénarios éducatifs intégrés

Chaque scénario correspond à une situation réelle permettant de tester les modèles IA :

1. **Montée progressive de température**  
   - Test du modèle de prédiction  
   - Activation automatique du ventilateur  
   - Analyse de stabilisation thermique  

2. **Porte ouverte**  
   - Lumière augmente, température monte  
   - Étude du bruit et des perturbations externes  

3. **Fuite d’eau ou condensation**  
   - Humidité instable, niveau d’eau anormal  
   - Détection via autoencoder  

4. **Ventilateur bloqué**  
   - PWM = 100% mais température monte  
   - Test de cohérence et d’anomalies métier  

5. **Humidité incohérente**  
   - Sauts brusques d’humidité  
   - Détection des signaux non physiques  

6. **Optimisation IA**  
   - Recommandation de PWM optimal  
   - Durée d’activation de la pompe  
   - Introduction à la régression pour edge AI  

7. **Perte réseau MQTT**  
   - Test de robustesse  
   - Gestion reconnection & continuité  

8. **Bruit et dérive capteurs**  
   - Injection de bruit gaussien  
   - Résilience du preprocessing  
   - Apprentissage des bonnes pratiques ML  

---

## 🛠️ Installation & exécution

1. **Cloner le dépôt**
```bash
https://github.com/HassenJebali/edge-AI.git
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
pip install -r requirements.txt
docker-compose -f docker/mosquitto/docker-compose.yml up -d
python simulator/sensor_simulator.py --scenario heat_ramp
python simulator/stm32_simulator.py
streamlit run dashboard/streamlit_app.py
```
---

##🧩 Architecture générale

Capteurs Virtuels → MQTT → STM32 Virtuel (TFLite) → MQTT → Dashboard
      ↓                            ↓
   Dataset ML              Anomalies / Optimisation

##📘 Objectifs pédagogiques
Créer un pipeline complet IoT + IA embarquée
Entraîner des modèles adaptés au microcontrôleur
Comprendre la valeur du preprocessing et des seuils
Simuler un firmware embarqué avant déploiement
Maîtriser MQTT dans un flux temps réel
Effectuer des tests avancés (latence, bruit, cohérence)
Idéal pour étudiants, ingénieurs débutants, makers et formateurs.

---

##🤝 Contributions
Toutes contributions sont les bienvenues :
Nouveaux scénarios
Nouveaux modèles IA
Intégration ESP32 / STM32 réels
Dashboards avancés
Tutoriels ou notebooks pédagogiques
