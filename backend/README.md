# 🏫 Escuela Horarios API

Sistema de generación automática de horarios escolares. Resuelve el problema real de compatibilidad entre profesores curriculares, grados y módulos horarios usando un algoritmo de backtracking.

---

## 🚀 Stack

- **Python 3.14** + **FastAPI** — API REST
- **PostgreSQL** + **SQLAlchemy** — Base de datos y ORM
- **Alembic** — Migraciones
- **JWT (python-jose + passlib)** — Autenticación
- **ReportLab + pypdf** — Generación de PDFs
- **Uvicorn** — Servidor ASGI

---

## 🧠 El problema que resuelve

A principio de año, las escuelas necesitan armar horarios compatibles entre todos los profesores curriculares (música, inglés, educación física, plástica, etc.). Cada profesor viene ciertos días, tiene una cantidad fija de módulos, y tiene que dar clases a múltiples grados sin superponerse.

Hacerlo a mano es un problema combinatorio complejo. Esta API lo resuelve automáticamente.

---

## 📐 Arquitectura

```
backend/
├── app/
│   ├── models/          # Modelos SQLAlchemy
│   ├── schemas/         # Schemas Pydantic
│   ├── routers/         # Endpoints por entidad
│   ├── services/
│   │   ├── scheduler/   # Algoritmo de backtracking
│   │   └── pdf/         # Generación de grillas PDF
│   └── core/            # Config, seguridad, dependencias
└── alembic/             # Migraciones
```

---

## 📡 Endpoints principales

### Auth
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/auth/registro` | Registrar directora |
| POST | `/auth/login` | Login, devuelve JWT |
| GET | `/auth/me` | Usuario actual |

### Escuela
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/escuelas/` | Crear escuela |
| GET | `/escuelas/{id}` | Obtener escuela |
| GET | `/escuelas/{id}/resumen` | Resumen completo |
| POST | `/escuelas/{id}/modulos` | Agregar módulo horario |
| POST | `/escuelas/{id}/grados` | Agregar grado |
| POST | `/escuelas/{id}/generar-horario` | Generar horario automático |
| POST | `/escuelas/{id}/generar-pdf` | Exportar grillas en PDF |

### Profesores
| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/escuelas/{id}/profesores` | Crear profesor curricular |
| GET | `/escuelas/{id}/profesores` | Listar profesores |

---

## ⚙️ Cómo correrlo localmente

### Requisitos
- Python 3.10+
- PostgreSQL

### Instalación

```bash
git clone https://github.com/TU_USUARIO/escuela-horarios.git
cd escuela-horarios/backend

python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
```

### Configurar variables de entorno

Creá un archivo `.env` en `backend/`:

```env
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/escuela_horarios
SECRET_KEY=tu_clave_secreta
```

### Crear la base de datos

```bash
alembic upgrade head
```

### Cargar datos de prueba (opcional)

```bash
python seed.py
```

### Levantar el servidor

```bash
uvicorn app.main:app --reload
```

La documentación interactiva estará disponible en `http://localhost:8000/docs`.

---

## 🧩 El algoritmo

El scheduler usa **backtracking con constraint checking**. Clasifica el problema como un CSP (Constraint Satisfaction Problem):

- **Variables:** slots a asignar por cada par (profesor, grado)
- **Dominio:** días y módulos disponibles del profesor
- **Restricciones:** ningún profesor ni grado puede estar en dos lugares al mismo tiempo

Los profesores se ordenan por cantidad de slots disponibles (más restrictivos primero) para reducir el espacio de búsqueda.

---

## 📄 Output PDF

El sistema genera un PDF con dos tipos de grillas:

- **Grilla por grado** — muestra cada módulo del día con la maestra de grado o el curricular asignado
- **Grilla por profesor curricular** — muestra a qué grado le da clase en cada módulo

---

## 🗺️ Roadmap

- [x] Backend v1.0.0 — API REST completa
- [ ] Frontend — Wizard de carga + visualización de horarios
- [ ] Mejoras al PDF — estilos, logo de escuela
- [ ] Guardado de horarios generados en DB
- [ ] Múltiples opciones de horario

---

## 👨‍💻 Autor

**Luca Tobias** — [GitHub](https://github.com/TU_USUARIO)

Analista de Sistemas | Estudiante de Física (UBA) | Backend Developer
