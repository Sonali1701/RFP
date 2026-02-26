"""
Simple Frontend for Proposal Processing System
Streamlit interface for uploading and processing proposals
"""

import streamlit as st
import requests
import json
from datetime import datetime
import os
from pathlib import Path
import base64

# Configuration
API_BASE = "http://localhost:8000"

def init_session_state():
    """Initialize session state variables"""
    if 'api_base' not in st.session_state:
        st.session_state.api_base = API_BASE
    if 'docx_bytes' not in st.session_state:
        st.session_state.docx_bytes = None
    if 'doc_report' not in st.session_state:
        st.session_state.doc_report = None
    if 'processing_result' not in st.session_state:
        st.session_state.processing_result = None
    # Ensure processing_result is properly initialized if it exists but is invalid
    elif st.session_state.processing_result is not None:
        if not isinstance(st.session_state.processing_result, dict):
            st.session_state.processing_result = None

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{st.session_state.api_base}/docs")
        return response.status_code == 200
    except:
        return False

def upload_and_process_proposal(proposal_file):
    """Upload and process a proposal"""
    try:
        with open(proposal_file, 'rb') as f:
            files = {"proposal_file": f}

            response = requests.post(
                f"{st.session_state.api_base}/api/v1/process-rfp",
                files=files,
            )
            
            if response.status_code == 200:
                result = response.json()
                st.session_state.processing_result = result
                st.success("Proposal processed successfully!")
                return True
            else:
                st.error(f"Processing failed: {response.status_code}")
                st.error(f"Error: {response.text}")
                return False
                
    except Exception as e:
        st.error(f"Error during processing: {str(e)}")
        return False


def upload_and_generate_docx(proposal_file):
    """Upload and generate a DOCX proposal response"""
    try:
        with open(proposal_file, 'rb') as f:
            files = {"proposal_file": f}
            response = requests.post(
                f"{st.session_state.api_base}/api/v1/process-rfp-doc",
                files=files,
            )

            if response.status_code == 200:
                return response.content

            st.error(f"DOCX generation failed: {response.status_code}")
            st.error(f"Error: {response.text}")
            return None

    except Exception as e:
        st.error(f"Error during DOCX generation: {str(e)}")
        return None


def upload_and_generate_qna_bundle(proposal_file, questions_text):
    """Upload and generate Q&A DOCX + report bundle"""
    try:
        with open(proposal_file, 'rb') as f:
            files = {"proposal_file": f}
            data = {"questions": questions_text}
            response = requests.post(
                f"{st.session_state.api_base}/api/v1/process-rfp-qna",
                files=files,
                data=data,
            )

            if response.status_code == 200:
                payload = response.json()
                docx_b64 = payload.get("docx_base64")
                report = payload.get("report")
                filename = payload.get("filename")
                if docx_b64:
                    docx_bytes = base64.b64decode(docx_b64.encode("utf-8"))
                else:
                    docx_bytes = None
                return {"docx_bytes": docx_bytes, "report": report, "filename": filename}

            st.error(f"Q&A bundle generation failed: {response.status_code}")
            st.error(f"Error: {response.text}")
            return None

    except Exception as e:
        st.error(f"Error during Q&A bundle generation: {str(e)}")
        return None


def upload_and_generate_docx_bundle(proposal_file):
    """Upload and generate DOCX + report bundle"""
    try:
        with open(proposal_file, 'rb') as f:
            files = {"proposal_file": f}
            response = requests.post(
                f"{st.session_state.api_base}/api/v1/process-rfp-doc-bundle",
                files=files,
            )

            if response.status_code == 200:
                payload = response.json()
                docx_b64 = payload.get("docx_base64")
                report = payload.get("report")
                filename = payload.get("filename")
                if docx_b64:
                    docx_bytes = base64.b64decode(docx_b64.encode("utf-8"))
                else:
                    docx_bytes = None
                return {"docx_bytes": docx_bytes, "report": report, "filename": filename}

            st.error(f"DOCX bundle generation failed: {response.status_code}")
            st.error(f"Error: {response.text}")
            return None

    except Exception as e:
        st.error(f"Error during DOCX bundle generation: {str(e)}")
        return None

def list_proposals():
    """List available proposals"""
    return []

def list_responses():
    """List available responses"""
    return []

def export_response_document(generated_response, source_report):
    """Export response document"""
    return False

def main():
    """Main application"""
    st.set_page_config(
        page_title="Proposal Processing System",
        page_icon="📄",
        layout="wide"
    )
    
    init_session_state()
    
    # Check API health
    if not check_api_health():
        st.error("❌ API is not running. Please start backend with: `python start_backend.py`")
        st.info("The backend should be running on http://localhost:8000")
        return

    st.title("📄 RFP Tool")
    
    # Sidebar
    with st.sidebar:
        st.subheader("🔧 Options")
        st.session_state.api_base = st.text_input("Backend URL", value=st.session_state.api_base)

        if st.button("🔄 Clear Results"):
            st.session_state.processing_result = None
            st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📤 Upload", "📄 DOCX Output", "📋 Report", "🧾 JSON Details"])
    
    with tab1:
        st.subheader("📤 Upload RFP")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose an RFP file",
            type=['pdf'],
            help="Upload the RFP PDF. The system will use RAG over your past Responses to draft a proposal response."
        )
        
        if uploaded_file:
            st.success(f"✅ File selected: {uploaded_file.name}")
            
            # File info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("File Size", f"{uploaded_file.size / 1024:.1f} KB")
            with col2:
                st.metric("File Type", uploaded_file.type)
            with col3:
                st.metric("Status", "Ready to Process")
            
            output_mode = st.radio(
                "Output",
                options=["DOCX (TOC)", "DOCX (Q&A)", "JSON (debug/details)"],
                horizontal=True,
            )

            # Save uploaded file temporarily
            temp_dir = "temp_uploads"
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, uploaded_file.name)

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Q&A questions textarea
            questions_text = ""
            if output_mode == "DOCX (Q&A)":
                questions_text = st.text_area(
                    "Enter questions (one per line)",
                    placeholder="What is the submission deadline?\nDescribe the evaluation criteria.\nWhat certifications are required?",
                    height=150,
                )

            col_a, col_b = st.columns([1, 1])
            with col_a:
                if st.button("📝 Generate Output", type="primary"):
                    if output_mode == "DOCX (TOC)":
                        with st.spinner("Generating DOCX (this can take a few minutes)..."):
                            bundle = upload_and_generate_docx_bundle(temp_path)
                            if bundle and bundle.get("docx_bytes"):
                                st.session_state.docx_bytes = bundle.get("docx_bytes")
                                st.session_state.doc_report = bundle.get("report")
                                st.session_state.docx_filename = bundle.get("filename")
                                st.success("DOCX + report generated successfully")
                    elif output_mode == "DOCX (Q&A)":
                        if not questions_text.strip():
                            st.error("Please enter at least one question.")
                        else:
                            with st.spinner("Generating Q&A DOCX (this can take a few minutes)..."):
                                bundle = upload_and_generate_qna_bundle(temp_path, questions_text)
                                if bundle and bundle.get("docx_bytes"):
                                    st.session_state.docx_bytes = bundle.get("docx_bytes")
                                    st.session_state.doc_report = bundle.get("report")
                                    st.session_state.docx_filename = bundle.get("filename")
                                    st.success("Q&A DOCX + report generated successfully")
                    else:
                        with st.spinner("Processing to JSON..."):
                            success = upload_and_process_proposal(temp_path)
                            if success:
                                st.success("JSON result generated")

            with col_b:
                if st.button("🧹 Clear Cached DOCX"):
                    if 'docx_bytes' in st.session_state:
                        st.session_state.docx_bytes = None
                    if 'doc_report' in st.session_state:
                        st.session_state.doc_report = None

            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
        
        # Processing instructions
        with st.expander("📖 How to Use"):
            st.markdown("""
            1. **Upload the RFP PDF**
            2. Choose **DOCX (TOC)**, **DOCX (Q&A)**, or **JSON** (debug/details)
            3. Click **Generate Output**
            4. Download:
               - DOCX from the **DOCX Output** tab
               - Report from the **Report** tab
               - JSON from the **JSON Details** tab

            The system will:
            - Build a proposal-specific Table of Contents (if TOC mode)
            - Use RAG over your past PDFs in the `Responses/` folder
            - Generate section content or Q&A answers with citations
            - Flag sections that require human review
            """)
    
    with tab2:
        st.subheader("📄 DOCX Output")

        if 'docx_bytes' in st.session_state and st.session_state.docx_bytes:
            st.download_button(
                label="📥 Download DOCX",
                data=st.session_state.docx_bytes,
                file_name=(
                    st.session_state.get('docx_filename')
                    or f"proposal_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
                ),
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

            st.info("If the Table of Contents is empty in Word: Right-click the TOC and choose 'Update Field'.")
        else:
            st.info("Generate a DOCX from the Upload tab to download it here.")


    with tab3:
        st.subheader("📋 Generation Report")

        if st.session_state.get('doc_report'):
            report = st.session_state.doc_report

            st.download_button(
                label="📥 Download Report JSON",
                data=json.dumps(report, indent=2),
                file_name=f"generation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
            )

            human_review = report.get("human_review") or []
            if human_review:
                st.warning("Sections requiring human review")
                for h in human_review:
                    st.write(f"- {h}")

            headings = report.get("headings") or {}
            answers = report.get("answers") or {}
            for key, details in {**headings, **answers}.items():
                with st.expander(f"{key}"):
                    st.write(f"Confidence: {details.get('confidence')}")
                    st.write(f"Used RFP: {details.get('used_rfp')}")
                    st.write(f"Used past responses: {details.get('used_past_responses')}")
                    st.write(f"Source breakdown: {details.get('source_breakdown')}")
                    st.write(f"Top source files: {details.get('top_source_files')}")
                    st.write(f"Human review: {details.get('human_review')}")
                    st.write(f"Review reasons: {details.get('review_reasons')}")
        else:
            st.info("Generate a DOCX from the Upload tab to view its report here.")


    with tab4:
        st.subheader("🧾 JSON Details")
        
        if st.session_state.processing_result:
            result = st.session_state.processing_result

            if not isinstance(result, dict) or "result" not in result:
                st.error("❌ Processing result is incomplete. Please process a new RFP.")
                return

            payload = result.get("result", {})
            proposal_data = payload.get("proposal_data", {})
            generated_response = payload.get("generated_response", {})
            rag_info = payload.get("rag", {})

            st.subheader("📊 RFP Analysis")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                title = proposal_data.get('title', 'Unknown')
                st.metric("Title", title[:24] + ("..." if len(title) > 24 else ""))
            with col2:
                st.metric("Requirements", len(proposal_data.get('requirements', [])))
            with col3:
                st.metric("Compliance", len(proposal_data.get('compliance', [])))
            with col4:
                st.metric("OCR Used", "Yes" if rag_info.get("used_ocr") else "No")
            
            # Requirements
            if proposal_data.get('requirements'):
                st.subheader("📋 Extracted Requirements")
                for i, req in enumerate(proposal_data['requirements'], 1):
                    st.write(f"{i}. {req}")
            
            # Generated Response
            st.subheader("📝 Generated Response")

            for section_name, section_payload in generated_response.items():
                with st.expander(f"📄 {section_name}"):
                    if isinstance(section_payload, dict):
                        st.write(section_payload.get("text", ""))
                        cits = section_payload.get("citations", [])
                        if cits:
                            st.caption("Citations")
                            for c in cits:
                                st.write(f"[C{c.get('citation')}] page {c.get('page')} (chunk {c.get('chunk_id')})")
                    else:
                        st.write(section_payload)

            st.subheader("📤 Export")
            st.download_button(
                label="📥 Download JSON Result",
                data=json.dumps(result, indent=2),
                file_name=f"rfp_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
            )
            
        else:
            st.info("No processing results yet. Upload and process a proposal in Upload tab!")
    
    # Footer
    st.markdown("---")
    st.markdown("🚀 **RFP Tool** - Powered by FastAPI, Chroma RAG, Gemini & Streamlit")
    st.markdown("💡 **Tip:** Make sure backend is running with `python start_backend.py`")

if __name__ == "__main__":
    main()
