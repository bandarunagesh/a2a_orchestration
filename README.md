# Local Containerized Microservices AI Ecosystem

A comprehensive, production-ready AI platform featuring 12 independent agent services orchestrated through a robust microservices architecture. Built with FastAPI, LangGraph, LangFuse, FalkorDB, PostgreSQL, ChromaDB, and integrated with Ollama for open-source LLM capabilities.

## 🏗️ Architecture Overview

### Core Components
- **12 Agent Services**: Specialized AI agents running in isolated FastAPI containers
- **Orchestrator Gateway**: Central entry point for user queries with semantic routing
- **MCP Tools Service**: Standalone utility service for data processing and analysis
- **Frontend Dashboard**: React.js interface for monitoring agent status and message flows
- **Data Layer**: PostgreSQL with synthetic clinical and financial datasets
- **Semantic Layer**: FalkorDB graph database for ontology and metadata management
- **Vector Memory**: ChromaDB for long-term insights and audit logging
- **Telemetry**: LangFuse for comprehensive tracing and performance monitoring

### Agent Chain Flow
```
User Query → Orchestrator → Startup → Conduct → Closeout → Regulatory →
Analyst → Insights → Forecasting → Report Builder → Dashboard Creator →
ETL Orchestrator → Data Profiler → Notifications
```

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- 8GB+ RAM recommended
- Python 3.9+ (for local development)

### Installation & Setup

1. **Clone and navigate to the project:**
   ```bash
   cd d:\AgenticAi\multiagents
   ```

2. **Start all services:**
   ```bash
   docker-compose up --build
   ```
   *Note: The system will automatically pull the Llama 3.2 model on first startup. This may take several minutes.*

3. **Seed databases with synthetic data:**
   ```bash
   # Run bootstrap script (requires environment variables)
   python bootstrap.py
   ```
   Or via Docker:
   ```bash
   docker-compose exec orchestrator_gateway python /app/bootstrap.py
   ```

4. **Access the services:**
   - **Frontend Dashboard**: http://localhost:3001
   - **Orchestrator Gateway**: http://localhost:8001
   - **LangFuse UI**: http://localhost:3000
   - **Agent Services**: http://localhost:8010-8021
   - **MCP Tools**: http://localhost:8030

## 📋 Service Details

### Agent Services (Ports 8010-8021)
Each agent runs in its own container with:
- **FastAPI** web framework
- **LangGraph** for workflow orchestration
- **SqliteSaver** for short-term memory
- **ChromaDB** integration for long-term storage
- **LangFuse** telemetry with trace propagation

| Agent | Port | Purpose |
|-------|------|---------|
| Startup | 8010 | Initial processing and setup |
| Conduct | 8011 | Core business logic execution |
| Closeout | 8012 | Finalization and cleanup |
| Regulatory | 8013 | Compliance and regulatory checks |
| Analyst | 8014 | Data analysis and insights |
| Insights | 8015 | Advanced analytics and reporting |
| Forecasting | 8016 | Predictive modeling |
| Report Builder | 8017 | Automated report generation |
| Dashboard Creator | 8018 | Visualization creation |
| ETL Orchestrator | 8019 | Data pipeline management |
| Data Profiler | 8020 | Data quality assessment |
| Notifications | 8021 | Alert and notification system |

### Supporting Services
- **PostgreSQL (5432)**: Primary data storage
- **FalkorDB (6379)**: Graph database for semantic layer
- **ChromaDB (8000)**: Vector database for embeddings
- **LangFuse (3000)**: Observability and tracing platform
- **Ollama (11434)**: Local LLM inference server

## 🤖 LLM Integration

The system integrates open-source LLMs via Ollama for intelligent processing in key agents:

### Integrated Agents
- **Analyst**: Uses Llama 3.2 for data analysis and insights generation
- **Insights**: Leverages LLM for advanced analytics and pattern recognition
- **Forecasting**: Applies LLM for predictive modeling and trend analysis
- **Report Builder**: Generates comprehensive reports using natural language
- **Dashboard Creator**: Designs dashboard layouts and visualizations

### Model Details
- **Model**: Llama 3.2 (via Ollama)
- **Deployment**: Local containerized inference
- **Cost**: Free and open-source
- **Capabilities**: Text generation, analysis, reasoning

The LLM integration provides intelligent automation while maintaining data privacy through local execution.

## 🔧 Configuration

### Environment Variables
Set these in your `.env` file or docker-compose environment:

```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=unify_plus

# Semantic Layer
FALKORDB_HOST=localhost

# Vector Memory
CHROMADB_HOST=localhost

# Telemetry
LANGFUSE_HOST=http://localhost:3000
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_SECRET_KEY=your-secret-key
```

### Customizing Agents
Each agent follows the same template structure:
- `main.py`: FastAPI app with LangGraph workflow
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container build configuration

To modify agent behavior:
1. Edit the `process_{agent_name}` function
2. Update routing logic in the `/process` endpoint
3. Rebuild with `docker-compose up --build`

## 📊 Data Schema

### PostgreSQL Tables
- **unify_plus**: Core business data (id, name, value, date)
- **ngdp**: National GDP data (id, country, gdp, year)
- **manual_excels**: Uploaded Excel data (id, filename, data JSONB)

### FalkorDB Ontology
- **Ontology**: Clinical/business rules and metadata
- **Business Rules**: Operational constraints
- **Metric Store**: KPI definitions and calculations

## 🔍 API Endpoints

### Orchestrator Gateway
- `POST /query`: Submit user queries for processing

### Agent Services
- `POST /process`: Process A2AState and route to next agent

### MCP Tools Service
- `POST /sql_sandbox`: Execute PostgreSQL queries
- `POST /excel_reader`: Parse Excel files
- `POST /excel_merger`: Combine Excel files
- `POST /python_sandbox`: Execute Python code
- `POST /meltano`: Run Meltano ETL commands
- `POST /file_converter`: Convert file formats

## 📈 Monitoring & Observability

### LangFuse Integration
- **Trace Propagation**: X-Langfuse-Trace-Id header across all services
- **Metrics**: Latency (P95), Reasoning Quality, Tool Use Accuracy
- **Unified Tracing**: Complete request flow visualization

### Health Checks
- Container health checks configured
- Service dependencies managed via docker-compose

## 🛠️ Development

### Local Development Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Start individual services: `uvicorn main:app --reload`
3. Run tests: `pytest`

### Adding New Agents
1. Create new directory under `agents/`
2. Copy template from existing agent
3. Update docker-compose.yml
4. Modify routing chain as needed

### Extending MCP Tools
Add new endpoints in `mcp_tools/main.py` following the existing pattern.

## 🔒 Security Considerations
- Services communicate via HTTPS internally
- Environment variables for sensitive configuration
- Isolated containers prevent cross-service interference
- Audit logging in ChromaDB for compliance

## 🚦 Troubleshooting

### Common Issues
- **Port conflicts**: Ensure ports 3000-8030 are available
- **Memory issues**: Increase Docker memory allocation
- **Database connection**: Verify environment variables
- **Build failures**: Check Docker logs with `docker-compose logs`

### Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs orchestrator_gateway

# Follow logs in real-time
docker-compose logs -f
```

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes with proper testing
4. Submit a pull request

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments
- Built with FastAPI, LangGraph, and modern Python async patterns
- Container orchestration with Docker Compose
- Inspired by enterprise AI platform architectures</content>
<parameter name="filePath">d:\AgenticAi\multiagents\README.md