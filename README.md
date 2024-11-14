# Kevin - Asistente de Operaciones 🤖

Kevin es un asistente virtual especializado en operaciones, que utiliza tecnología RAG (Retrieval Augmented Generation) para proporcionar respuestas precisas basadas en documentación interna y búsquedas web.

## 🚀 Características

- Procesamiento inteligente de documentos PDF y TXT
- Búsqueda semántica en documentos internos
- Integración con búsqueda web vía DuckDuckGo
- Interfaz de chat intuitiva con Streamlit
- Métricas detalladas de uso y costos
- Historial de conversaciones persistente
- Visualización de fuentes consultadas
- Manejo robusto de errores y logging
- Verificación de conexión a internet

## 📋 Requisitos Previos

- Python 3.9 o superior
- Cuenta de Azure OpenAI
- Acceso a Internet para búsquedas web (opcional)
- Suficiente espacio en disco para documentos y logs

## 🛠️ Instalación

1. Clonar el repositorio:

```bash
git clone <url-del-repositorio>
cd OPERATIONS
```

2. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
   - Crear archivo `config/.env` con las siguientes variables:

```env
AZURE_OPENAI_API_KEY=tu_api_key
AZURE_OPENAI_ENDPOINT=tu_endpoint
CHAT_DEPLOYMENT=gpt-4o
EMBEDDING_DEPLOYMENT=text-embeding-model
API_VERSION=2024-02-15-preview
EMBEDDING_API_VERSION=2023-05-15
```

## 📁 Estructura Completa del Proyecto

OPERATIONS/
│
├── src/ # Código fuente principal
│ ├── core/ # Núcleo de la aplicación
│ │ ├── init.py
│ │ ├── config.py # Configuración y variables de entorno
│ │ └── logger.py # Sistema de logging
│ │
│ ├── models/ # Modelos de IA
│ │ ├── init.py
│ │ └── rag_model.py # Implementación del modelo RAG
│ │
│ ├── prompts/ # Versiones del role del sistema
│ │ └── qa_prompts.py # multiples personalidades para el modelo
│ │
│ ├── utils/ # Utilidades generales
│ │ ├── init.py
│ │ ├── document_processor.py # Procesamiento de documentos
│ │ └── token_counter.py # Contador de tokens
│ │
│ └── ui/ # Interfaz de usuario
│ ├── init.py
│ ├── app.py # Aplicación principal
│ └── components/ # Componentes de la UI
│ ├── init.py
│ ├── header.py # Componente de cabecera
│ ├── sidebar.py # Componente de barra lateral
│ └── chat.py # Componente de chat
│
├── config/ # Configuración
│ └── .env # Variables de entorno
│
├── data/ # Datos
│ ├── raw/ # Documentos originales
│ └── processed/ # Documentos procesados
│
├── assets/ # Recursos estáticos
│ └── logo.png # Logo de la aplicación
│
├── logs/ # Archivos de registro
├── tests/ # Tests unitarios
├── main.py # Punto de entrada
├── requirements.txt # Dependencias
└── README.md # Documentación

### 📝 Descripción de los Componentes Principales

#### 🔧 Core

- `config.py`: Gestión de configuración y variables de entorno
- `logger.py`: Sistema centralizado de logging

#### 🤖 Models

- `rag_model.py`: Implementación del modelo RAG con Azure OpenAI

#### 🛠️ Utils

- `document_processor.py`: Procesamiento de documentos PDF y TXT
- `token_counter.py`: Control y métricas de uso de tokens

#### 🎨 UI

- `app.py`: Aplicación principal de Streamlit
- `components/`: Componentes modulares de la interfaz
  - `header.py`: Cabecera con logo y título
  - `sidebar.py`: Panel lateral con configuración
  - `chat.py`: Interfaz de chat y visualización de respuestas

#### 📂 Directorios de Datos

- `config/`: Archivos de configuración y variables de entorno
- `data/`: Almacenamiento de documentos
- `assets/`: Recursos estáticos como imágenes
- `logs/`: Archivos de registro del sistema
- `tests/`: Tests automatizados

## 🚀 Uso

1. Iniciar la aplicación:

```bash
streamlit run main.py
```

2. Cargar documentos:

   - Usar el panel lateral para subir archivos PDF o TXT
   - Hacer clic en "Inicializar/Reinicializar Modelo"
   - Esperar a que se procesen los documentos

3. Interactuar con Kevin:
   - Escribir preguntas en el chat
   - Revisar fuentes y métricas en los detalles de cada respuesta
   - Aprovechar la búsqueda web automática

## 📊 Métricas y Monitoreo

- **Tokens**:

  - Contador de tokens por consulta
  - Acumulado total de tokens
  - Desglose por tipo (pregunta, contexto, web, respuesta)

- **Costos**:

  - Estimación por consulta
  - Acumulado total
  - Basado en tarifa de $0.03 por 1K tokens

- **Tiempo**:

  - Tiempo de respuesta por consulta
  - Timestamp de cada interacción

- **Fuentes**:
  - Documentos internos consultados
  - Resultados de búsqueda web
  - Relevancia de cada fuente

## 🔧 Mantenimiento

### Logs

- Ubicación: `logs/app_YYYYMMDD.log`
- Niveles: INFO, WARNING, ERROR
- Rotación diaria automática

### Documentos

- Formatos: PDF, TXT
- Límite recomendado: 20MB por archivo
- Procesamiento automático de estructura

### Conexión Web

- Verificación automática de conectividad
- Fallback a documentos locales si no hay conexión
- Timeout configurable para búsquedas

## 🤝 Contribución

1. Fork del repositorio
2. Crear rama: `git checkout -b feature/NuevaCaracteristica`
3. Commit cambios: `git commit -am 'Añadir nueva característica'`
4. Push a la rama: `git push origin feature/NuevaCaracteristica`
5. Crear Pull Request

## 📝 Notas Importantes

- Mantener actualizadas las credenciales de Azure
- Revisar periódicamente el uso de tokens
- Hacer backup regular de documentos
- Monitorear los logs para problemas
- Verificar conexión a internet para búsquedas web

## 🆘 Solución de Problemas

### Errores Comunes

1. **Modelo no inicializado**

   - Verificar documentos cargados
   - Comprobar credenciales Azure
   - Reinicializar el modelo

2. **Errores de documentos**

   - Verificar formato (PDF/TXT)
   - Comprobar tamaño
   - Revisar permisos

3. **Problemas de conexión**

   - Verificar internet
   - Comprobar endpoint Azure
   - Revisar firewall/proxy

4. **Errores de búsqueda web**
   - Verificar conexión
   - Comprobar timeout
   - Revisar límites de DuckDuckGo

## 📞 Soporte

Para reportar problemas o solicitar ayuda:

- Crear issue en el repositorio
- Contactar al equipo de soporte
- Consultar documentación Azure OpenAI

## 📄 Licencia

Este proyecto está bajo la licencia [especificar licencia].

---

Desarrollado con ❤️ por [Eugenio García] © 2024
