from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from contextlib import asynccontextmanager
import uvicorn
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import List, Dict, Any, Optional

# Import AI services
from services.ai_integration import ai_integration_service
from services.sample_content import sample_content_service
from services.knowledge_base import enhanced_knowledge_base, KnowledgeBaseItem

# Import API routers
from api.knowledge_base import router as knowledge_base_router
from api.document_export import router as document_export_router
from api.proposal_analysis import router as proposal_analysis_router
from api.simple_proposal import router as simple_proposal_router

# Simple FastAPI app for testing
app = FastAPI(
    title="Agentic AI RFP Automation Platform",
    description="An intelligent platform for automating RFP processes with AI agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(knowledge_base_router, prefix="/api/v1/knowledge-base", tags=["Knowledge Base"])
app.include_router(document_export_router, prefix="/api/v1/documents", tags=["Document Export"])
app.include_router(proposal_analysis_router, prefix="/api/v1/proposals", tags=["Proposal Analysis"])
app.include_router(simple_proposal_router, prefix="/api/v1/simple", tags=["Simple Proposal"])

# JWT Configuration
SECRET_KEY = "your-super-secret-key-change-this-in-production-123456789"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test user data
TEST_USER = {
    "email": "test@rfp.com",
    "password": "test123456",
    "full_name": "Test User",
    "role": "admin",
    "id": 1
}

# Pydantic models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "user"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str

# AI Request/Response Models
class QuestionAnalysisRequest(BaseModel):
    question: str
    context: Optional[Dict[str, Any]] = None

class ResponseGenerationRequest(BaseModel):
    question: str
    analysis: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None

class ComplianceCheckRequest(BaseModel):
    response_text: str
    category: Optional[str] = None

class ContentSearchRequest(BaseModel):
    query: str
    category: Optional[str] = None

# Knowledge Base Models
class KnowledgeBaseItemCreate(BaseModel):
    title: str
    content: str
    content_type: str = "document"
    category: str
    subcategory: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
    author: Optional[str] = None
    access_level: str = "internal"

class KnowledgeBaseItemUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    content_type: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    access_level: Optional[str] = None

class KnowledgeBaseSearchRequest(BaseModel):
    query: str
    category: Optional[str] = None
    content_type: Optional[str] = None
    limit: int = 10
    search_strategy: str = "hybrid"  # keyword, semantic, hybrid

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Authentication endpoints
@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Register a new user"""
    # Simple validation - in testing mode, just accept any user
    if user.email == TEST_USER["email"]:
        # Return existing test user
        return UserResponse(
            id=TEST_USER["id"],
            email=TEST_USER["email"],
            full_name=TEST_USER["full_name"],
            role=TEST_USER["role"]
        )
    
    # Create new user (simplified)
    return UserResponse(
        id=2,
        email=user.email,
        full_name=user.full_name,
        role=user.role
    )

@app.post("/api/v1/auth/login", response_model=Token)
async def login(user_credentials: UserLogin):
    """Login user and return token"""
    # Check if it's our test user
    if (user_credentials.email == TEST_USER["email"] and 
        user_credentials.password == TEST_USER["password"]):
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": TEST_USER["email"], "role": TEST_USER["role"]},
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": TEST_USER["id"],
                "email": TEST_USER["email"],
                "full_name": TEST_USER["full_name"],
                "role": TEST_USER["role"]
            }
        )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user():
    """Get current user info (simplified for testing)"""
    return UserResponse(
        id=TEST_USER["id"],
        email=TEST_USER["email"],
        full_name=TEST_USER["full_name"],
        role=TEST_USER["role"]
    )

# AI Integration Endpoints
@app.post("/api/v1/ai/analyze-question")
async def analyze_question(request: QuestionAnalysisRequest):
    """Analyze RFP question using AI + knowledge base"""
    try:
        result = ai_integration_service.analyze_question(request.question, request.context)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing question: {str(e)}"
        )

@app.post("/api/v1/ai/generate-response")
async def generate_response(request: ResponseGenerationRequest):
    """Generate RFP response using AI + knowledge base"""
    try:
        result = ai_integration_service.generate_response(
            request.question, request.analysis, request.context
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating response: {str(e)}"
        )

@app.post("/api/v1/ai/check-compliance")
async def check_compliance(request: ComplianceCheckRequest):
    """Check compliance using AI + rule-based system"""
    try:
        result = ai_integration_service.check_compliance(
            request.response_text, request.category
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking compliance: {str(e)}"
        )

@app.post("/api/v1/content/search")
async def search_content(request: ContentSearchRequest):
    """Search knowledge base content"""
    try:
        results = sample_content_service.search_content(request.query, request.category)
        return {
            "query": request.query,
            "category": request.category,
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching content: {str(e)}"
        )

@app.get("/api/v1/content/templates")
async def get_templates():
    """Get all available templates"""
    try:
        templates = sample_content_service.get_all_templates()
        return {
            "templates": templates,
            "total": len(templates)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting templates: {str(e)}"
        )

@app.get("/api/v1/content/templates/{template_id}")
async def get_template(template_id: int):
    """Get specific template by ID"""
    try:
        template = sample_content_service.get_template(template_id)
        if not template:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Template {template_id} not found"
            )
        return template
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting template: {str(e)}"
        )

# Knowledge Base Management Endpoints
@app.post("/api/v1/knowledge-base/items")
async def create_knowledge_item(item: KnowledgeBaseItemCreate):
    """Create a new knowledge base item"""
    try:
        kb_item = KnowledgeBaseItem(
            id="",  # Will be generated
            title=item.title,
            content=item.content,
            content_type=item.content_type,
            category=item.category,
            subcategory=item.subcategory,
            tags=item.tags,
            metadata=item.metadata,
            author=item.author,
            access_level=item.access_level
        )
        
        item_id = enhanced_knowledge_base.add_knowledge_item(kb_item)
        
        return {
            "id": item_id,
            "message": "Knowledge base item created successfully",
            "item": enhanced_knowledge_base.get_knowledge_item(item_id).__dict__
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating knowledge item: {str(e)}"
        )

@app.get("/api/v1/knowledge-base/items/{item_id}")
async def get_knowledge_item(item_id: str):
    """Get a specific knowledge base item"""
    try:
        item = enhanced_knowledge_base.get_knowledge_item(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Knowledge item {item_id} not found"
            )
        return item.__dict__
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting knowledge item: {str(e)}"
        )

@app.put("/api/v1/knowledge-base/items/{item_id}")
async def update_knowledge_item(item_id: str, updates: KnowledgeBaseItemUpdate):
    """Update a knowledge base item"""
    try:
        # Convert to dict and remove None values
        update_data = {k: v for k, v in updates.dict().items() if v is not None}
        
        success = enhanced_knowledge_base.update_knowledge_item(item_id, update_data)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Knowledge item {item_id} not found"
            )
        
        return {
            "message": "Knowledge base item updated successfully",
            "item": enhanced_knowledge_base.get_knowledge_item(item_id).__dict__
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating knowledge item: {str(e)}"
        )

@app.delete("/api/v1/knowledge-base/items/{item_id}")
async def delete_knowledge_item(item_id: str):
    """Delete a knowledge base item"""
    try:
        success = enhanced_knowledge_base.delete_knowledge_item(item_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Knowledge item {item_id} not found"
            )
        
        return {"message": "Knowledge base item deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting knowledge item: {str(e)}"
        )

@app.post("/api/v1/knowledge-base/search")
async def search_knowledge_base(request: KnowledgeBaseSearchRequest):
    """Search knowledge base with advanced filtering and semantic search"""
    try:
        results = enhanced_knowledge_base.search_knowledge_base(
            query=request.query,
            category=request.category,
            content_type=request.content_type,
            limit=request.limit,
            search_strategy=request.search_strategy
        )
        
        return {
            "query": request.query,
            "filters": {
                "category": request.category,
                "content_type": request.content_type,
                "search_strategy": request.search_strategy
            },
            "results": results,
            "total": len(results)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error searching knowledge base: {str(e)}"
        )

@app.get("/api/v1/knowledge-base/categories")
async def get_knowledge_base_categories():
    """Get all knowledge base categories and subcategories"""
    try:
        categories = enhanced_knowledge_base.get_categories()
        return {"categories": categories}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting categories: {str(e)}"
        )

@app.get("/api/v1/knowledge-base/content-types")
async def get_knowledge_base_content_types():
    """Get all available content types"""
    try:
        content_types = enhanced_knowledge_base.get_content_types()
        return {"content_types": content_types}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting content types: {str(e)}"
        )

@app.get("/api/v1/knowledge-base/items")
async def get_knowledge_base_items(category: str = None, subcategory: str = None):
    """Get knowledge base items by category"""
    try:
        items = enhanced_knowledge_base.get_items_by_category(category, subcategory)
        return {
            "category": category,
            "subcategory": subcategory,
            "items": [item.__dict__ for item in items],
            "total": len(items)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting knowledge base items: {str(e)}"
        )

@app.get("/api/v1/knowledge-base/analytics")
async def get_knowledge_base_analytics():
    """Get knowledge base analytics and usage statistics"""
    try:
        analytics = enhanced_knowledge_base.get_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting analytics: {str(e)}"
        )

@app.post("/api/v1/knowledge-base/bulk-import")
async def bulk_import_knowledge_base(items: List[Dict[str, Any]]):
    """Bulk import knowledge base items"""
    try:
        result = enhanced_knowledge_base.bulk_import(items)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error during bulk import: {str(e)}"
        )

@app.get("/api/v1/knowledge-base/export")
async def export_knowledge_base(category: str = None):
    """Export knowledge base items"""
    try:
        export_data = enhanced_knowledge_base.export_knowledge_base(category)
        return export_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting knowledge base: {str(e)}"
        )

@app.get("/api/v1/knowledge-base/items/{item_id}/similar")
async def find_similar_content(item_id: str, limit: int = 5):
    """Find content similar to a specific knowledge base item"""
    try:
        similar_items = enhanced_knowledge_base.find_similar_content(item_id, limit)
        return {
            "item_id": item_id,
            "similar_items": similar_items,
            "total": len(similar_items)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error finding similar content: {str(e)}"
        )

# Original endpoints
@app.get("/")
async def root():
    return {
        "message": "Agentic AI RFP Automation Platform",
        "version": "1.0.0",
        "status": "running",
        "testing_mode": True
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "testing_mode": True,
        "storage": "memory"
    }

@app.get("/api/v1/info")
async def api_info():
    return {
        "platform": "RFP Automation Platform",
        "ai_service": "Google Gemini + Enhanced Knowledge Base",
        "storage": "Memory (Testing Mode)",
        "features": [
            "Document Processing",
            "AI-Powered Analysis",
            "Response Generation",
            "Compliance Checking",
            "Content Library Search",
            "Template Management",
            "Enhanced Knowledge Base",
            "Advanced Search & Filtering",
            "Knowledge Analytics",
            "Bulk Import/Export",
            "Hybrid AI + Rule-Based System"
        ],
        "available_endpoints": [
            "Authentication: /api/v1/auth/*",
            "AI Services: /api/v1/ai/*",
            "Content: /api/v1/content/*",
            "Knowledge Base: /api/v1/knowledge-base/*",
            "Documentation: /docs"
        ],
        "knowledge_base": {
            "total_items": len(enhanced_knowledge_base.knowledge_base),
            "categories": len(enhanced_knowledge_base.categories),
            "content_types": enhanced_knowledge_base.get_content_types(),
            "search_capabilities": ["text_search", "category_filter", "content_type_filter", "relevance_scoring"],
            "management_features": ["create", "read", "update", "delete", "bulk_import", "export", "analytics"]
        }
    }

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🧪 Using Memory Storage (Testing Mode)")
    print("🚀 FastAPI server starting...")
    yield
    # Shutdown
    print("🛑 FastAPI server shutting down...")

if __name__ == "__main__":
    uvicorn.run(
        "backend.main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
