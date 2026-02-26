# Agentic AI RFP Automation Platform

An intelligent, autonomous platform that revolutionizes Request for Proposal (RFP) processes through AI-driven automation, semantic understanding, and continuous learning.

## 🚀 Features

### Core Capabilities
- **Multi-format RFP Ingestion**: Word, PDF, Excel, CSV, ZIP files and email integration
- **AI-Powered Parsing**: OCR for scanned documents, deadline detection, mandatory question identification
- **Smart Content Library**: Centralized repository with version control and metadata tagging
- **Autonomous Response Generation**: Semantic matching, context-aware drafting, confidence scoring
- **Workflow Automation**: SME assignment, progress tracking, SLA enforcement
- **Compliance Management**: Risk detection, security control mapping, regulatory compliance
- **Analytics & Intelligence**: Win rate tracking, performance metrics, continuous optimization

### AI Agents
- **RFP Intake Agent**: Document processing and initial parsing
- **Question Classification Agent**: Categorization and routing
- **Answer Retrieval Agent**: Semantic search and content matching
- **Answer Drafting Agent**: Context-aware response generation
- **Compliance and Risk Agent**: Risk assessment and compliance checking
- **SME Orchestration Agent**: Expert coordination and assignment
- **Quality Assurance Agent**: Review and validation
- **Learning and Optimization Agent**: Continuous improvement

## 🏗️ Architecture

```
├── backend/                 # FastAPI backend services
│   ├── api/                # API endpoints
│   ├── core/               # Core business logic
│   ├── models/             # Database models
│   ├── services/           # Business services
│   └── utils/              # Utilities and helpers
├── agents/                 # AI agents
│   ├── intake/             # RFP intake processing
│   ├── classification/     # Question categorization
│   ├── retrieval/          # Content retrieval
│   ├── drafting/           # Response generation
│   ├── compliance/         # Risk and compliance
│   ├── sme/               # SME coordination
│   ├── qa/                # Quality assurance
│   └── learning/          # Learning and optimization
├── database/               # Database schemas and migrations
├── frontend/              # Streamlit/React dashboard
├── tests/                 # Test suites
└── docs/                  # Documentation
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy
- **Authentication**: JWT with OAuth2
- **Task Queue**: Celery with Redis
- **Vector Storage**: ChromaDB/Weaviate

### AI/ML
- **LLMs**: OpenAI GPT-4, Anthropic Claude
- **Embeddings**: Sentence Transformers
- **Vector Search**: FAISS, ChromaDB
- **Document Processing**: PyPDF2, python-docx, OCR

### Frontend
- **Dashboard**: Streamlit (MVP), React (Phase 2)
- **Visualization**: Plotly, D3.js
- **UI Components**: Tailwind CSS, shadcn/ui

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- Redis 6+
- Node.js 16+ (for React frontend)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd rfp-automation-platform
```

2. **Set up virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env .env
# Edit .env with your configuration
```

5. **Set up database**
```bash
# Create database
createdb rfp_platform

# Run migrations
alembic upgrade head
```

6. **Start services**
```bash
# Start Redis
redis-server

# Start Celery worker
celery -A backend.core.celery worker --loglevel=info

# Start FastAPI server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Start Streamlit dashboard (in new terminal)
streamlit run frontend/dashboard.py
```

## 📖 API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501

## 🔧 Configuration

### Environment Variables
See `.env.example` for all available configuration options.

### Database Configuration
The platform supports both PostgreSQL and MySQL databases. See setup guides:
- [PostgreSQL Setup](docs/deployment.md#database-setup)
- [MySQL Setup](docs/mysql-setup.md)

Default configuration uses PostgreSQL. To use MySQL, update your `.env`:
```env
DATABASE_URL=mysql://username:password@localhost:3306/rfp_platform
```

### AI Model Configuration
Configure Gemini and Anthropic API keys in your environment to enable AI features.

```env
# AI Services
GEMINI_API_KEY=your-gemini-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key  # Optional fallback
```

### Testing Mode
For rapid development and testing without database setup:

```env
# Enable testing mode (uses local memory storage)
TESTING_MODE=true

# Disable testing mode (uses database)
TESTING_MODE=false
```

📖 **See [Testing Mode Guide](docs/testing-mode.md)** for complete instructions.

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov-report=html

# Run specific test file
pytest tests/test_api.py
```

## 📊 Features by Phase

### MVP (Current)
- RFP parsing and ingestion
- Basic auto-fill functionality
- Content library management
- Simple workflow tracking
- Basic analytics dashboard

### Phase 2 (Planned)
- Advanced AI agents
- Risk detection and compliance
- Learning and optimization models
- Enhanced collaboration features

### Phase 3 (Future)
- Predictive win scoring
- Fully autonomous RFP handling
- Advanced integrations (CRM, PM tools)
- Multi-tenant architecture

## 🔒 Security

- SOC 2 Type II ready
- ISO 27001 aligned
- Encryption at rest and in transit
- Role-based access control
- Audit logging and compliance tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation in `/docs`

---

Built with ❤️ for proposal teams everywhere.
