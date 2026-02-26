from typing import Union
from ..core.config import settings

# Import storage services
from ..services.memory_storage import MemoryStorageService
from ..core.database import SessionLocal, engine


class StorageService:
    """Storage abstraction layer that switches between memory and database based on TESTING_MODE"""
    
    def __init__(self):
        if settings.testing_mode:
            print("🧪 Using Memory Storage (Testing Mode)")
            self.service = MemoryStorageService()
        else:
            print("🗄️ Using Database Storage (Production Mode)")
            self.service = DatabaseStorageService()
    
    async def create_user(self, user_data):
        return await self.service.create_user(user_data)
    
    async def get_user_by_email(self, email):
        return await self.service.get_user_by_email(email)
    
    async def get_user(self, user_id):
        return await self.service.get_user(user_id)
    
    async def get_users(self, skip=0, limit=100):
        return await self.service.get_users(skip, limit)
    
    async def create_rfp(self, rfp_data):
        return await self.service.create_rfp(rfp_data)
    
    async def get_rfp(self, rfp_id):
        return await self.service.get_rfp(rfp_id)
    
    async def get_rfps(self, skip=0, limit=100, status=None):
        return await self.service.get_rfps(skip, limit, status)
    
    async def update_rfp(self, rfp_id, update_data):
        return await self.service.update_rfp(rfp_id, update_data)
    
    async def create_question(self, question_data):
        return await self.service.create_question(question_data)
    
    async def get_questions_by_rfp(self, rfp_id, skip=0, limit=100):
        return await self.service.get_questions_by_rfp(rfp_id, skip, limit)
    
    async def create_response(self, response_data):
        return await self.service.create_response(response_data)
    
    async def get_responses_by_rfp(self, rfp_id):
        return await self.service.get_responses_by_rfp(rfp_id)
    
    async def create_content(self, content_data):
        return await self.service.create_content(content_data)
    
    async def get_content(self, content_id):
        return await self.service.get_content(content_id)
    
    async def search_content(self, query, limit=10, content_type=None):
        return await self.service.search_content(query, limit, content_type)
    
    async def get_dashboard_stats(self):
        return await self.service.get_dashboard_stats()
    
    async def log_activity(self, activity_data):
        return await self.service.log_activity(activity_data)
    
    async def get_activities(self, rfp_id=None, limit=50):
        return await self.service.get_activities(rfp_id, limit)


class DatabaseStorageService:
    """Database storage service wrapper for production mode"""
    
    def __init__(self):
        pass
    
    async def create_user(self, user_data):
        # Import here to avoid circular imports
        from ..models.user import User
        from ..core.security import get_password_hash
        
        db = SessionLocal()
        try:
            hashed_password = get_password_hash(user_data["password"])
            db_user = User(
                email=user_data["email"],
                username=user_data["username"],
                full_name=user_data["full_name"],
                hashed_password=hashed_password,
                role=user_data.get("role", "sales"),
                is_active=True,
                is_verified=True
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return self._user_to_dict(db_user)
        finally:
            db.close()
    
    async def get_user_by_email(self, email):
        from ..models.user import User
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            return self._user_to_dict(user) if user else None
        finally:
            db.close()
    
    async def get_user(self, user_id):
        from ..models.user import User
        
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            return self._user_to_dict(user) if user else None
        finally:
            db.close()
    
    async def get_users(self, skip=0, limit=100):
        from ..models.user import User
        
        db = SessionLocal()
        try:
            users = db.query(User).offset(skip).limit(limit).all()
            return [self._user_to_dict(user) for user in users]
        finally:
            db.close()
    
    async def create_rfp(self, rfp_data):
        from ..models.rfp import RFP
        
        db = SessionLocal()
        try:
            db_rfp = RFP(
                title=rfp_data["title"],
                description=rfp_data["description"],
                client_name=rfp_data["client_name"],
                client_industry=rfp_data.get("client_industry"),
                client_contact=rfp_data.get("client_contact"),
                rfp_number=rfp_data.get("rfp_number"),
                submission_deadline=rfp_data.get("submission_deadline"),
                estimated_value=rfp_data.get("estimated_value"),
                contract_duration=rfp_data.get("contract_duration"),
                priority=rfp_data.get("priority", "medium"),
                assigned_to_id=rfp_data.get("assigned_to_id"),
                original_filename=rfp_data.get("original_filename"),
                file_size=rfp_data.get("file_size"),
                file_type=rfp_data.get("file_type"),
                page_count=rfp_data.get("page_count"),
                created_by_id=rfp_data.get("created_by_id")
            )
            db.add(db_rfp)
            db.commit()
            db.refresh(db_rfp)
            return self._rfp_to_dict(db_rfp)
        finally:
            db.close()
    
    async def get_rfp(self, rfp_id):
        from ..models.rfp import RFP
        
        db = SessionLocal()
        try:
            rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
            return self._rfp_to_dict(rfp) if rfp else None
        finally:
            db.close()
    
    async def get_rfps(self, skip=0, limit=100, status=None):
        from ..models.rfp import RFP
        
        db = SessionLocal()
        try:
            query = db.query(RFP)
            if status:
                query = query.filter(RFP.status == status)
            rfps = query.offset(skip).limit(limit).all()
            return [self._rfp_to_dict(rfp) for rfp in rfps]
        finally:
            db.close()
    
    async def update_rfp(self, rfp_id, update_data):
        from ..models.rfp import RFP
        
        db = SessionLocal()
        try:
            rfp = db.query(RFP).filter(RFP.id == rfp_id).first()
            if rfp:
                for key, value in update_data.items():
                    if hasattr(rfp, key):
                        setattr(rfp, key, value)
                db.commit()
                db.refresh(rfp)
                return self._rfp_to_dict(rfp)
            return None
        finally:
            db.close()
    
    async def create_question(self, question_data):
        from ..models.question import Question
        
        db = SessionLocal()
        try:
            db_question = Question(
                rfp_id=question_data["rfp_id"],
                question_text=question_data["question_text"],
                question_number=question_data.get("question_number"),
                section=question_data.get("section"),
                subsection=question_data.get("subsection"),
                question_type=question_data.get("question_type", "essay"),
                priority=question_data.get("priority", "medium"),
                category=question_data.get("category"),
                subcategory=question_data.get("subcategory"),
                topic_area=question_data.get("topic_area"),
                max_words=question_data.get("max_words"),
                max_characters=question_data.get("max_characters"),
                is_mandatory=question_data.get("is_mandatory", True),
                is_disqualifier=question_data.get("is_disqualifier", False)
            )
            db.add(db_question)
            db.commit()
            db.refresh(db_question)
            return self._question_to_dict(db_question)
        finally:
            db.close()
    
    async def get_questions_by_rfp(self, rfp_id, skip=0, limit=100):
        from ..models.question import Question
        
        db = SessionLocal()
        try:
            questions = db.query(Question).filter(Question.rfp_id == rfp_id).offset(skip).limit(limit).all()
            return [self._question_to_dict(question) for question in questions]
        finally:
            db.close()
    
    async def create_response(self, response_data):
        from ..models.response import Response
        
        db = SessionLocal()
        try:
            db_response = Response(
                rfp_id=response_data["rfp_id"],
                question_id=response_data["question_id"],
                answer_text=response_data["answer_text"],
                source_type=response_data.get("source_type", "ai_generated"),
                source_content_id=response_data.get("source_content_id"),
                confidence_score=response_data.get("confidence_score", 0.8),
                similarity_score=response_data.get("similarity_score", 0.0),
                status=response_data.get("status", "draft"),
                version=1,
                is_compliant=response_data.get("is_compliant", True),
                compliance_notes=response_data.get("compliance_notes"),
                risk_score=response_data.get("risk_score", 0.2),
                quality_score=response_data.get("quality_score", 0.8),
                completeness_score=response_data.get("completeness_score", 0.8),
                accuracy_score=response_data.get("accuracy_score", 0.8),
                created_by_id=response_data.get("created_by_id")
            )
            db.add(db_response)
            db.commit()
            db.refresh(db_response)
            return self._response_to_dict(db_response)
        finally:
            db.close()
    
    async def get_responses_by_rfp(self, rfp_id):
        from ..models.response import Response
        
        db = SessionLocal()
        try:
            responses = db.query(Response).filter(Response.rfp_id == rfp_id).all()
            return [self._response_to_dict(response) for response in responses]
        finally:
            db.close()
    
    async def create_content(self, content_data):
        from ..models.content import Content
        
        db = SessionLocal()
        try:
            db_content = Content(
                title=content_data["title"],
                content=content_data["content"],
                content_type=content_data.get("content_type"),
                category=content_data.get("category"),
                subcategory=content_data.get("subcategory"),
                industry=content_data.get("industry"),
                geography=content_data.get("geography"),
                product_line=content_data.get("product_line"),
                service_area=content_data.get("service_area"),
                status=content_data.get("status", "pending"),
                version="1.0",
                is_public=content_data.get("is_public", True),
                is_locked=content_data.get("is_locked", False),
                usage_count=0,
                success_rate=0.0,
                confidence_score=content_data.get("confidence_score", 0.8),
                compliance_score=content_data.get("compliance_score", 0.9),
                readability_score=content_data.get("readability_score", 0.8),
                created_by_id=content_data.get("created_by_id")
            )
            db.add(db_content)
            db.commit()
            db.refresh(db_content)
            return self._content_to_dict(db_content)
        finally:
            db.close()
    
    async def get_content(self, content_id):
        from ..models.content import Content
        
        db = SessionLocal()
        try:
            content = db.query(Content).filter(Content.id == content_id).first()
            return self._content_to_dict(content) if content else None
        finally:
            db.close()
    
    async def search_content(self, query, limit=10, content_type=None):
        from ..models.content import Content
        
        db = SessionLocal()
        try:
            db_query = db.query(Content)
            
            if content_type:
                db_query = db_query.filter(Content.content_type == content_type)
            
            # Simple text search for now
            if query:
                db_query = db_query.filter(
                    (Content.title.ilike(f"%{query}%") | 
                     Content.content.ilike(f"%{query}%"))
                )
            
            contents = db_query.limit(limit).all()
            return [self._content_to_dict(content) for content in contents]
        finally:
            db.close()
    
    async def get_dashboard_stats(self):
        from ..models.rfp import RFP
        from ..models.response import Response
        from ..models.question import Question
        
        db = SessionLocal()
        try:
            total_rfps = db.query(RFP).count()
            active_rfps = db.query(RFP).filter(
                RFP.status.in_(["draft", "in_progress", "under_review"])
            ).count()
            submitted_rfps = db.query(RFP).filter(RFP.status == "submitted").count()
            won_rfps = db.query(RFP).filter(RFP.status == "won").count()
            
            total_questions = db.query(Question).count()
            answered_questions = db.query(Response).filter(Response.status == "approved").count()
            
            return {
                "rfp_stats": {
                    "total": total_rfps,
                    "active": active_rfps,
                    "submitted": submitted_rfps,
                    "won": won_rfps,
                    "win_rate": (won_rfps / submitted_rfps * 100) if submitted_rfps > 0 else 0.0
                },
                "response_stats": {
                    "total_questions": total_questions,
                    "answered_questions": answered_questions,
                    "completion_rate": (answered_questions / total_questions * 100) if total_questions > 0 else 0.0
                },
                "upcoming_deadlines": 0
            }
        finally:
            db.close()
    
    async def log_activity(self, activity_data):
        from ..models.workflow import Activity
        
        db = SessionLocal()
        try:
            activity = Activity(
                rfp_id=activity_data.get("rfp_id"),
                user_id=activity_data.get("user_id"),
                activity_type=activity_data.get("activity_type"),
                description=activity_data.get("description"),
                metadata=activity_data.get("metadata", {})
            )
            db.add(activity)
            db.commit()
            db.refresh(activity)
            return self._activity_to_dict(activity)
        finally:
            db.close()
    
    async def get_activities(self, rfp_id=None, limit=50):
        from ..models.workflow import Activity
        
        db = SessionLocal()
        try:
            query = db.query(Activity)
            if rfp_id:
                query = query.filter(Activity.rfp_id == rfp_id)
            
            activities = query.order_by(Activity.created_at.desc()).limit(limit).all()
            return [self._activity_to_dict(activity) for activity in activities]
        finally:
            db.close()
    
    # Helper methods to convert models to dicts
    def _user_to_dict(self, user):
        if not user:
            return None
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role,
            "is_active": user.is_active,
            "is_verified": user.is_verified,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }
    
    def _rfp_to_dict(self, rfp):
        if not rfp:
            return None
        return {
            "id": rfp.id,
            "title": rfp.title,
            "description": rfp.description,
            "client_name": rfp.client_name,
            "client_industry": rfp.client_industry,
            "status": rfp.status,
            "priority": rfp.priority,
            "created_at": rfp.created_at,
            "updated_at": rfp.updated_at
        }
    
    def _question_to_dict(self, question):
        if not question:
            return None
        return {
            "id": question.id,
            "rfp_id": question.rfp_id,
            "question_text": question.question_text,
            "question_type": question.question_type,
            "priority": question.priority,
            "created_at": question.created_at
        }
    
    def _response_to_dict(self, response):
        if not response:
            return None
        return {
            "id": response.id,
            "rfp_id": response.rfp_id,
            "question_id": response.question_id,
            "answer_text": response.answer_text,
            "source_type": response.source_type,
            "confidence_score": response.confidence_score,
            "status": response.status,
            "created_at": response.created_at
        }
    
    def _content_to_dict(self, content):
        if not content:
            return None
        return {
            "id": content.id,
            "title": content.title,
            "content": content.content,
            "content_type": content.content_type,
            "category": content.category,
            "status": content.status,
            "created_at": content.created_at
        }
    
    def _activity_to_dict(self, activity):
        if not activity:
            return None
        return {
            "id": activity.id,
            "rfp_id": activity.rfp_id,
            "user_id": activity.user_id,
            "activity_type": activity.activity_type,
            "description": activity.description,
            "created_at": activity.created_at
        }
