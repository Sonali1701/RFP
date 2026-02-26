"""
Enhanced Frontend for Proposal Processing System
Modern UI with improved UX, animations, and professional design
"""

import streamlit as st
import requests
import json
from datetime import datetime
import os
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

# Configuration
API_BASE = "http://localhost:8000"

# Custom CSS for modern design
def apply_custom_css():
    st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #1e3a8a;
            --secondary-color: #3b82f6;
            --accent-color: #60a5fa;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --background-color: #f8fafc;
            --card-background: #ffffff;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
        }
        
        /* Hide streamlit elements */
        .stDeployButton {display:none;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stStatus {display: none;}
        
        /* Custom card styles */
        .metric-card {
            background: var(--card-background);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }
        
        /* Button styles */
        .stButton > button {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, var(--secondary-color), var(--accent-color));
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* File uploader styles */
        .stFileUploader {
            border: 2px dashed var(--border-color);
            border-radius: 12px;
            padding: 30px;
            text-align: center;
            background: var(--card-background);
            transition: all 0.3s ease;
        }
        
        .stFileUploader:hover {
            border-color: var(--accent-color);
            background: #f1f5f9;
        }
        
        /* Tab styles */
        .stTabs [data-baseweb="tab-list"] {
            background: var(--card-background);
            border-radius: 12px;
            padding: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        /* Progress bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, var(--secondary-color), var(--accent-color));
            border-radius: 8px;
        }
        
        /* Success message */
        .success-message {
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            padding: 16px;
            border-radius: 8px;
            margin: 10px 0;
            font-weight: 500;
        }
        
        /* Warning message */
        .warning-message {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
            padding: 16px;
            border-radius: 8px;
            margin: 10px 0;
            font-weight: 500;
        }
        
        /* Error message */
        .error-message {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            padding: 16px;
            border-radius: 8px;
            margin: 10px 0;
            font-weight: 500;
        }
        
        /* Info card */
        .info-card {
            background: linear-gradient(135deg, #3b82f6, #2563eb);
            color: white;
            padding: 20px;
            border-radius: 12px;
            margin: 15px 0;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }
        
        /* Loading animation */
        .loading-spinner {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px;
        }
        
        /* Sidebar styles */
        .css-1d391kg {
            background: var(--card-background);
            border-right: 1px solid var(--border-color);
        }
        
        /* Header styles */
        .main-header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        /* Section headers */
        .section-header {
            background: linear-gradient(135deg, #f8fafc, #e2e8f0);
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0 15px 0;
            border-left: 4px solid var(--primary-color);
        }
        
        /* Data table styles */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        
        /* Expandable sections */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'auth_token' not in st.session_state:
        st.session_state.auth_token = None
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'processing_result' not in st.session_state:
        st.session_state.processing_result = None
    if 'processing_history' not in st.session_state:
        st.session_state.processing_history = []
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

def show_login_page():
    """Beautiful login page"""
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Proposal Processing System</h1>
        <p>AI-Powered Government Proposal Analysis & Response Generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>🔐 Secure Login</h2>
            <p>Access your proposal processing dashboard</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=True):
            email = st.text_input(
                "📧 Email Address", 
                value="test@rfp.com",
                help="Enter your registered email"
            )
            password = st.text_input(
                "🔑 Password", 
                type="password",
                value="test123456",
                help="Enter your password"
            )
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit_button = st.form_submit_button("🚀 Login", use_container_width=True)
            
            if submit_button:
                with st.spinner("🔐 Authenticating..."):
                    try:
                        response = requests.post(f"{API_BASE}/auth/login", json={
                            "email": email,
                            "password": password
                        })
                        
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.auth_token = data['access_token']
                            st.session_state.current_user = {
                                "email": email, 
                                "full_name": "Test User",
                                "login_time": datetime.now()
                            }
                            st.markdown('<div class="success-message">✅ Login successful! Redirecting...</div>', unsafe_allow_html=True)
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.markdown('<div class="error-message">❌ Login failed. Please check your credentials.</div>', unsafe_allow_html=True)
                            
                    except Exception as e:
                        st.markdown(f'<div class="error-message">❌ Error during login: {str(e)}</div>', unsafe_allow_html=True)

def show_sidebar():
    """Enhanced sidebar with modern design"""
    with st.sidebar:
        # User profile section
        if st.session_state.current_user:
            st.markdown(f"""
            <div class="info-card">
                <h3>👤 User Profile</h3>
                <p><strong>{st.session_state.current_user['email']}</strong></p>
                <p>🕐 Login: {st.session_state.current_user['login_time'].strftime('%H:%M')}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick actions
        st.markdown('<div class="section-header"><h3>🔧 Quick Actions</h3></div>', unsafe_allow_html=True)
        
        if st.button("🚀 New Proposal", use_container_width=True):
            st.session_state.processing_result = None
            st.rerun()
        
        if st.button("📊 Dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
        
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
        
        # System status
        st.markdown('<div class="section-header"><h3>📊 System Status</h3></div>', unsafe_allow_html=True)
        
        try:
            health_response = requests.get(f"{API_BASE}/health", timeout=3)
            if health_response.status_code == 200:
                health_data = health_response.json()
                st.success("✅ API Online")
                st.info(f"🤖 Gemini: {'✅' if health_data.get('gemini_configured') else '❌'}")
            else:
                st.error("❌ API Offline")
        except:
            st.error("❌ Connection Error")
        
        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.auth_token = None
            st.session_state.current_user = None
            st.session_state.processing_result = None
            st.rerun()

def show_dashboard_stats():
    """Beautiful dashboard with statistics"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        
        # Get data
        proposals_response = requests.get(f"{API_BASE}/simple/list-proposals", headers=headers, timeout=5)
        responses_response = requests.get(f"{API_BASE}/simple/list-responses", headers=headers, timeout=5)
        
        proposals = proposals_response.json()['proposals'] if proposals_response.status_code == 200 else []
        responses = responses_response.json()['responses'] if responses_response.status_code == 200 else []
        
        # Calculate stats
        total_proposals = len(proposals)
        total_responses = len(responses)
        avg_proposal_size = sum(p['size'] for p in proposals) / total_proposals if proposals else 0
        
        # Recent activity
        recent_proposals = sorted(proposals, key=lambda x: x['modified'], reverse=True)[:5]
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h3>📋 Proposals</h3>
                <h1>{}</h1>
                <p>Total files</p>
            </div>
            """.format(total_proposals), unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h3>📁 Responses</h3>
                <h1>{}</h1>
                <p>Available files</p>
            </div>
            """.format(total_responses), unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h3>📊 Avg Size</h3>
                <h1>{:.1f} KB</h1>
                <p>Proposal files</p>
            </div>
            """.format(avg_proposal_size / 1024), unsafe_allow_html=True)
        
        with col4:
            if st.session_state.processing_result:
                st.markdown("""
                <div class="metric-card">
                    <h3>✅ Last Processed</h3>
                    <h1>{}</h1>
                    <p>Requirements</p>
                </div>
                """.format(len(st.session_state.processing_result.get('proposal_analysis', {}).get('requirements', []))), unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h3>🔄 Status</h3>
                    <h1>Ready</h1>
                    <p>System active</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Charts
        if proposals:
            col1, col2 = st.columns(2)
            
            with col1:
                # File size distribution
                sizes = [p['size'] / 1024 for p in proposals]
                fig = px.histogram(x=sizes, nbins=10, title="📊 Proposal File Size Distribution")
                fig.update_layout(showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Recent activity timeline
                if recent_proposals:
                    dates = [pd.to_datetime(p['modified']) for p in recent_proposals]
                    fig = px.scatter(x=dates, y=[1]*len(dates), title="📅 Recent Activity")
                    fig.update_layout(showlegend=False, height=300, yaxis_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
        
        # Recent files table
        if recent_proposals:
            st.markdown('<div class="section-header"><h3>📋 Recent Proposals</h3></div>', unsafe_allow_html=True)
            
            df = pd.DataFrame(recent_proposals)
            df['modified'] = pd.to_datetime(df['modified']).dt.strftime('%Y-%m-%d %H:%M')
            df['size'] = (df['size'] / 1024).round(1).astype(str) + ' KB'
            
            st.dataframe(df[['filename', 'size', 'modified']], use_container_width=True)
        
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {str(e)}")

def show_upload_section():
    """Enhanced upload section"""
    st.markdown('<div class="section-header"><h3>📤 Upload Proposal</h3></div>', unsafe_allow_html=True)
    
    # File upload with drag and drop
    uploaded_file = st.file_uploader(
        "📁 Choose a proposal file or drag & drop",
        type=['txt', 'md', 'pdf', 'docx'],
        help="Upload your government proposal document (TXT, MD, PDF, or DOCX)",
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        # File info card
        st.markdown(f"""
        <div class="metric-card">
            <h3>📄 File Information</h3>
            <p><strong>Name:</strong> {uploaded_file.name}</p>
            <p><strong>Size:</strong> {uploaded_file.size / 1024:.1f} KB</p>
            <p><strong>Type:</strong> {uploaded_file.type}</p>
            <p><strong>Status:</strong> ✅ Ready to Process</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Processing options
        st.markdown('<div class="section-header"><h3>⚙️ Processing Options</h3></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            use_gemini = st.checkbox("🤖 Use AI Enhancement", value=True, help="Use Gemini AI for better responses")
        
        with col2:
            include_risks = st.checkbox("⚠️ Risk Analysis", value=True, help="Include risk assessment")
        
        # Process button with animation
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Process Proposal", type="primary", use_container_width=True):
                with st.spinner("🔄 Processing proposal... This may take a moment..."):
                    # Save uploaded file temporarily
                    temp_dir = "temp_uploads"
                    os.makedirs(temp_dir, exist_ok=True)
                    temp_path = os.path.join(temp_dir, uploaded_file.name)
                    
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Process proposal
                    success = upload_and_process_proposal(temp_path)
                    
                    # Clean up
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                    
                    if success:
                        # Add to history
                        if st.session_state.processing_result:
                            st.session_state.processing_history.append({
                                'timestamp': datetime.now(),
                                'filename': uploaded_file.name,
                                'result': st.session_state.processing_result
                            })
                        st.rerun()

def show_results_section():
    """Enhanced results display"""
    if not st.session_state.processing_result:
        st.markdown("""
        <div class="info-card">
            <h3>📊 No Processing Results</h3>
            <p>Upload and process a proposal to see detailed results here.</p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    result = st.session_state.processing_result
    
    # Check if result has required keys
    if not all(key in result for key in ['proposal_analysis', 'generated_response', 'source_report', 'relevant_responses']):
        st.markdown("""
        <div class="warning-message">
            ⚠️ Processing result is incomplete. Please process a new proposal.
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Results header
    proposal_data = result['proposal_analysis']
    st.markdown(f"""
    <div class="main-header">
        <h1>📊 Processing Results</h1>
        <p>Analysis for: {proposal_data.get('title', 'Unknown Proposal')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📋 Requirements</h3>
            <h1>{len(proposal_data.get('requirements', []))}</h1>
            <p>Extracted items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>✅ Compliance</h3>
            <h1>{len(proposal_data.get('compliance', []))}</h1>
            <p>Requirements</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📁 Sources</h3>
            <h1>{len(result['relevant_responses'])}</h1>
            <p>Relevant files</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📝 Sections</h3>
            <h1>{len(result['generated_response'])}</h1>
            <p>Generated</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Analysis", "📝 Response", "📈 Sources", "⚠️ Risks", "📤 Export"
    ])
    
    with tab1:
        show_proposal_analysis(proposal_data)
    
    with tab2:
        show_generated_response(result['generated_response'])
    
    with tab3:
        show_source_analysis(result['source_report'], result['relevant_responses'])
    
    with tab4:
        show_risk_analysis(result['source_report'])
    
    with tab5:
        show_export_options(result['generated_response'], result['source_report'])

def show_proposal_analysis(proposal_data):
    """Display proposal analysis"""
    st.markdown('<div class="section-header"><h3>📊 Proposal Analysis</h3></div>', unsafe_allow_html=True)
    
    # Requirements section
    if proposal_data.get('requirements'):
        st.markdown("#### 📋 Extracted Requirements")
        for i, req in enumerate(proposal_data['requirements'], 1):
            st.markdown(f"""
            <div class="metric-card">
                <strong>{i}.</strong> {req}
            </div>
            """, unsafe_allow_html=True)
    
    # Compliance section
    if proposal_data.get('compliance'):
        st.markdown("#### ✅ Compliance Requirements")
        for i, comp in enumerate(proposal_data['compliance'], 1):
            st.markdown(f"""
            <div class="metric-card">
                <strong>{i}.</strong> {comp}
            </div>
            """, unsafe_allow_html=True)
    
    # Other details
    col1, col2 = st.columns(2)
    
    with col1:
        if proposal_data.get('scope'):
            st.markdown("#### 🎯 Scope")
            st.markdown(f"""
            <div class="metric-card">
                {proposal_data['scope']}
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if proposal_data.get('timeline'):
            st.markdown("#### 📅 Timeline")
            st.markdown(f"""
            <div class="metric-card">
                {proposal_data['timeline']}
            </div>
            """, unsafe_allow_html=True)

def show_generated_response(generated_response):
    """Display generated response"""
    st.markdown('<div class="section-header"><h3>📝 Generated Response</h3></div>', unsafe_allow_html=True)
    
    sections = [
        ('executive_summary', '📋 Executive Summary'),
        ('technical_approach', '🔧 Technical Approach'),
        ('methodology', '📊 Methodology'),
        ('team_qualifications', '👥 Team Qualifications'),
        ('past_performance', '🏆 Past Performance'),
        ('risk_management', '⚠️ Risk Management'),
        ('compliance', '✅ Compliance'),
        ('pricing', '💰 Pricing'),
        ('timeline', '📅 Timeline')
    ]
    
    for section_key, section_title in sections:
        if section_key in generated_response and generated_response[section_key]:
            with st.expander(section_title):
                st.markdown(f"""
                <div class="metric-card">
                    {generated_response[section_key]}
                </div>
                """, unsafe_allow_html=True)

def show_source_analysis(source_report, relevant_responses):
    """Display source analysis"""
    st.markdown('<div class="section-header"><h3>📈 Source Analysis</h3></div>', unsafe_allow_html=True)
    
    # Source metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📁 Sources Used</h3>
            <h1>{source_report.get('sources_used', 0)}</h1>
            <p>Reference files</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🆕 New Content</h3>
            <h1>{len(source_report.get('new_content', []))}</h1>
            <p>Generated items</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊 Similarity</h3>
            <h1>{source_report.get('average_similarity', 0):.1%}</h1>
            <p>Average match</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Relevant responses
    if relevant_responses:
        st.markdown("#### 📁 Relevant Response Files")
        for i, resp in enumerate(relevant_responses[:5], 1):
            similarity = resp.get('similarity', 0) * 100
            st.markdown(f"""
            <div class="metric-card">
                <strong>{i}.</strong> {Path(resp['file']).name}<br>
                <small>📊 Similarity: {similarity:.1f}%</small>
            </div>
            """, unsafe_allow_html=True)

def show_risk_analysis(source_report):
    """Display risk analysis"""
    st.markdown('<div class="section-header"><h3>⚠️ Risk Analysis</h3></div>', unsafe_allow_html=True)
    
    # Risks
    if source_report.get('risks'):
        st.markdown("#### ⚠️ Identified Risks")
        for risk in source_report['risks']:
            st.markdown(f"""
            <div class="warning-message">
                ⚠️ {risk}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-message">
            ✅ No significant risks identified
        </div>
        """, unsafe_allow_html=True)
    
    # Review checklist
    if source_report.get('review_items'):
        st.markdown("#### ✅ Review Checklist")
        for item in source_report['review_items']:
            st.checkbox(item, key=item)

def show_export_options(generated_response, source_report):
    """Display export options"""
    st.markdown('<div class="section-header"><h3>📤 Export Options</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export Response Document", type="primary", use_container_width=True):
            export_response_document(generated_response, source_report)
    
    with col2:
        if st.button("📊 Export Source Report", use_container_width=True):
            export_source_report(source_report)
    
    # Export format options
    st.markdown("#### 📋 Export Formats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>📄 Word Document</h4>
            <p>Professional format with formatting</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 PDF Report</h4>
            <p>Printable format with charts</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>📋 JSON Data</h4>
            <p>Raw data for integration</p>
        </div>
        """, unsafe_allow_html=True)

def upload_and_process_proposal(proposal_file):
    """Upload and process a proposal"""
    try:
        with open(proposal_file, 'rb') as f:
            files = {"proposal_file": f}
            headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
            
            response = requests.post(
                f"{API_BASE}/simple/complete",
                files=files,
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                st.session_state.processing_result = result
                st.markdown('<div class="success-message">✅ Proposal processed successfully!</div>', unsafe_allow_html=True)
                return True
            else:
                st.markdown(f'<div class="error-message">❌ Processing failed: {response.status_code}</div>', unsafe_allow_html=True)
                return False
                
    except Exception as e:
        st.markdown(f'<div class="error-message">❌ Error during processing: {str(e)}</div>', unsafe_allow_html=True)
        return False

def export_response_document(generated_response, source_report):
    """Export response document"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        
        response = requests.post(
            f"{API_BASE}/simple/export-response",
            json={
                "generated_response": generated_response,
                "source_report": source_report
            },
            headers=headers
        )
        
        if response.status_code == 200:
            filename = f"Proposal_Response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            st.download_button(
                label="📥 Download Word Document",
                data=response.content,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
            st.markdown('<div class="success-message">✅ Document ready for download!</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="error-message">❌ Export failed: {response.status_code}</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.markdown(f'<div class="error-message">❌ Error exporting document: {str(e)}</div>', unsafe_allow_html=True)

def export_source_report(source_report):
    """Export source report"""
    try:
        # Convert to JSON for download
        json_data = json.dumps(source_report, indent=2, default=str)
        filename = f"Source_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        st.download_button(
            label="📥 Download Source Report",
            data=json_data,
            file_name=filename,
            mime="application/json",
            use_container_width=True
        )
        st.markdown('<div class="success-message">✅ Source report ready for download!</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.markdown(f'<div class="error-message">❌ Error exporting source report: {str(e)}</div>', unsafe_allow_html=True)

def list_proposals():
    """List available proposals"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.get(f"{API_BASE}/simple/list-proposals", headers=headers)
        
        if response.status_code == 200:
            return response.json()['proposals']
        else:
            return []
            
    except Exception as e:
        return []

def list_responses():
    """List available responses"""
    try:
        headers = {"Authorization": f"Bearer {st.session_state.auth_token}"}
        response = requests.get(f"{API_BASE}/simple/list-responses", headers=headers)
        
        if response.status_code == 200:
            return response.json()['responses']
        else:
            return []
            
    except Exception as e:
        return []

def check_api_health():
    """Check if API is running"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def main():
    """Main application with enhanced UI"""
    # Apply custom CSS
    apply_custom_css()
    
    # Page configuration
    st.set_page_config(
        page_title="Proposal Processing System",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Check API health
    if not check_api_health():
        st.markdown("""
        <div class="error-message">
            ❌ API is not running. Please start backend with: <code>python ultra_simple.py</code>
        </div>
        """, unsafe_allow_html=True)
        st.info("💡 The backend should be running on http://localhost:8000")
        return
    
    # Login section
    if not st.session_state.auth_token:
        show_login_page()
        return
    
    # Main interface
    show_sidebar()
    
    # Main content
    st.markdown("""
    <div class="main-header">
        <h1>🚀 Proposal Processing System</h1>
        <p>AI-Powered Government Proposal Analysis & Response Generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 Upload & Process", 
        "📊 Dashboard", 
        "📋 Proposals", 
        "📁 Responses"
    ])
    
    with tab1:
        show_upload_section()
        st.markdown("---")
        show_results_section()
    
    with tab2:
        show_dashboard_stats()
    
    with tab3:
        st.markdown('<div class="section-header"><h3>📋 Available Proposals</h3></div>', unsafe_allow_html=True)
        
        proposals = list_proposals()
        
        if proposals:
            df = pd.DataFrame(proposals)
            df['modified'] = pd.to_datetime(df['modified']).dt.strftime('%Y-%m-%d %H:%M')
            df['size'] = (df['size'] / 1024).round(1).astype(str) + ' KB'
            
            st.dataframe(df[['filename', 'size', 'modified']], use_container_width=True)
        else:
            st.markdown("""
            <div class="info-card">
                <h3>📋 No Proposals Found</h3>
                <p>Upload your first proposal in the Upload tab!</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="section-header"><h3>📁 Available Responses</h3></div>', unsafe_allow_html=True)
        
        responses = list_responses()
        
        if responses:
            df = pd.DataFrame(responses)
            df['modified'] = pd.to_datetime(df['modified']).dt.strftime('%Y-%m-%d %H:%M')
            df['size'] = (df['size'] / 1024).round(1).astype(str) + ' KB'
            
            st.dataframe(df[['filename', 'size', 'modified']], use_container_width=True)
        else:
            st.markdown("""
            <div class="info-card">
                <h3>📁 No Response Files Found</h3>
                <p>Add your past responses to the Responses folder!</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; padding: 20px;">
        🚀 <strong>Enhanced Proposal Processing System</strong> - Powered by FastAPI & Streamlit<br>
        <small>With AI-Powered Analysis & Modern UI Design</small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
