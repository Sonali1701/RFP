"""
Simple Proposal API - Clean, straightforward API for proposal processing
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any
import os
from datetime import datetime
from pathlib import Path

from core.simple_database import get_db
from models.user import User
from services.simple_proposal import proposal_processor
from services.simple_document_export import simple_document_export
from api.auth import get_current_user

router = APIRouter()

@router.post("/process")
async def process_proposal(
    proposal_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Process a proposal and generate response
    """
    try:
        # Save uploaded proposal
        proposals_dir = Path("C:/Users/vs510/PycharmProjects/RFP/Proposal")
        proposals_dir.mkdir(exist_ok=True)
        
        proposal_path = proposals_dir / proposal_file.filename
        with open(proposal_path, "wb") as f:
            content = await proposal_file.read()
            f.write(content)
        
        # Process proposal
        result = proposal_processor.process_proposal(str(proposal_path))
        
        return {
            "status": "success",
            "result": result,
            "message": "Proposal processed successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Proposal processing failed: {str(e)}"
        )

@router.post("/export-response")
async def export_response_document(
    generated_response: Dict[str, Any],
    source_report: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Export response as Word document
    """
    try:
        # Prepare document data
        document_data = {
            'title': source_report.get('proposal_title', 'Proposal Response'),
            'client_name': 'Government Agency',
            'submission_date': datetime.now().strftime('%B %d, %Y'),
            'prepared_by': 'Your Organization',
            **generated_response
        }
        
        # Generate document
        doc_bytes = simple_document_export.generate_proposal_response_document(
            document_data, source_report
        )
        
        # Return file
        from fastapi.responses import Response
        return Response(
            content=doc_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename=Proposal_Response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Document export failed: {str(e)}"
        )

@router.post("/export-report")
async def export_source_report(
    source_report: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Export source report as Word document
    """
    try:
        # Generate document
        doc_bytes = simple_document_export.generate_source_report_document(source_report)
        
        # Return file
        from fastapi.responses import Response
        return Response(
            content=doc_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename=Source_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report export failed: {str(e)}"
        )

@router.post("/complete")
async def complete_workflow(
    proposal_file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Complete workflow: process proposal and return everything
    """
    try:
        # Save and process proposal
        proposals_dir = Path("C:/Users/vs510/PycharmProjects/RFP/Proposal")
        proposals_dir.mkdir(exist_ok=True)
        
        proposal_path = proposals_dir / proposal_file.filename
        with open(proposal_path, "wb") as f:
            content = await proposal_file.read()
            f.write(content)
        
        # Process proposal
        result = proposal_processor.process_proposal(str(proposal_path))
        
        # Generate documents
        response_doc = await export_response_document(
            result['generated_response'], 
            result['source_report'], 
            db, 
            current_user
        )
        
        report_doc = await export_source_report(
            result['source_report'], 
            db, 
            current_user
        )
        
        return {
            "status": "success",
            "proposal_analysis": result['proposal_data'],
            "generated_response": result['generated_response'],
            "source_report": result['source_report'],
            "relevant_responses": result['relevant_responses'],
            "documents": {
                "response_document": "Generated successfully",
                "source_report": "Generated successfully"
            },
            "message": "Complete workflow executed successfully"
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Complete workflow failed: {str(e)}"
        )

@router.get("/list-proposals")
async def list_proposals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List available proposals"""
    try:
        proposals_dir = Path("C:/Users/vs510/PycharmProjects/RFP/Proposal")
        proposals = []
        
        if proposals_dir.exists():
            for file_path in proposals_dir.glob("*"):
                if file_path.is_file():
                    proposals.append({
                        "filename": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
        
        return {"proposals": proposals, "count": len(proposals)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list proposals: {str(e)}"
        )

@router.get("/list-responses")
async def list_responses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List available responses"""
    try:
        responses_dir = Path("C:/Users/vs510/PycharmProjects/RFP/Responses")
        responses = []
        
        if responses_dir.exists():
            for file_path in responses_dir.glob("*"):
                if file_path.is_file():
                    responses.append({
                        "filename": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
        
        return {"responses": responses, "count": len(responses)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list responses: {str(e)}"
        )
