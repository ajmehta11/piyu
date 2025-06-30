import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict

# Configure the page
st.set_page_config(
    page_title="💖 Grievance Portal",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for pink theme with better contrast and popup
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
    }
    
    .chat-container {
        background: #ffffff;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(233, 30, 99, 0.2);
        border: 3px solid #e91e63;
        margin: 20px 0;
    }
    
    .header-title {
        color: #880e4f;
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(136, 14, 79, 0.1);
    }
    
    .success-message {
        background: #e8f5e8;
        color: #2e7d32;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid #4caf50;
        text-align: center;
        margin: 15px 0;
        font-weight: bold;
    }
    
    .stTextArea > div > div > textarea {
        border-radius: 15px;
        border: 3px solid #e91e63;
        background-color: #ffffff;
        color: #212529;
        font-size: 16px;
    }
    
    .stSelectbox > div > div > select {
        border-radius: 15px;
        border: 3px solid #e91e63;
        background-color: #ffffff;
        color: #212529;
        font-size: 16px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #e91e63 0%, #ad1457 100%);
        color: #ffffff !important;
        border-radius: 25px;
        border: none;
        padding: 15px 40px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 6px 20px rgba(233, 30, 99, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(233, 30, 99, 0.5);
        color: #ffffff !important;
    }
    
    /* Override Streamlit's default text colors */
    .stMarkdown, .stText, div[data-testid="stMarkdownContainer"] p {
        color: #212529 !important;
    }
    
    /* Form labels */
    .stSelectbox label, .stTextArea label {
        color: #880e4f !important;
        font-weight: bold !important;
        font-size: 18px !important;
    }
    
    /* Cute feature buttons */
    .cute-button {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        color: #880e4f;
        border-radius: 20px;
        border: 2px solid #e91e63;
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
        margin: 5px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
    }
    
    .cute-button:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
    }
    
    /* Popup styles */
    .popup-overlay {
        position: relative;
        width: 100%;
        padding: 20px 0;
        background-color: transparent;
        z-index: 1;
        display: flex;
        justify-content: center;
        align-items: center;
    }
    
    .popup-content {
        background: linear-gradient(135deg, #fce4ec 0%, #f8bbd9 100%);
        border-radius: 30px;
        padding: 40px;
        text-align: center;
        box-shadow: 0 20px 60px rgba(233, 30, 99, 0.4);
        border: 4px solid #e91e63;
        max-width: 500px;
        width: 90%;
        animation: popupFadeIn 0.5s ease-out;
    }
    
    @keyframes popupFadeIn {
        from {
            opacity: 0;
            transform: scale(0.7) translateY(-20px);
        }
        to {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
    }
    
    .popup-title {
        color: #880e4f;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(136, 14, 79, 0.1);
    }
    
    .popup-message {
        color: #212529;
        font-size: 20px;
        margin-bottom: 30px;
        font-weight: bold;
    }
    
    .popup-close-btn {
        background: linear-gradient(135deg, #e91e63 0%, #ad1457 100%);
        color: #ffffff;
        border: none;
        border-radius: 25px;
        padding: 15px 30px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(233, 30, 99, 0.4);
        transition: all 0.3s ease;
        margin-top: 20px;
        display: inline-block;
    }
    
    .popup-close-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(233, 30, 99, 0.5);
    }
    
    .close-button-container {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, 50px);
        z-index: 10002;
        text-align: center;
    }
    
    .popup-image {
        max-width: 200px;
        max-height: 200px;
        border-radius: 15px;
        border: 3px solid #e91e63;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.3);
    }
    
    /* Animation container */
    .animation-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 9999;
        overflow: hidden;
    }
    
    /* Falling animations */
    @keyframes fall {
        0% {
            transform: translateY(-100px) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
    
    @keyframes bounce {
        0%, 20%, 60%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-20px);
        }
        80% {
            transform: translateY(-10px);
        }
    }
    
    .falling-item {
        position: absolute;
        animation: fall 3s linear infinite;
        font-size: 30px;
    }
    
    .bouncing-item {
        animation: bounce 2s infinite;
        font-size: 25px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing grievances, animations, and popup
if 'grievances' not in st.session_state:
    st.session_state.grievances = []
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'animation_active' not in st.session_state:
    st.session_state.animation_active = False
if 'animation_type' not in st.session_state:
    st.session_state.animation_type = ""
if 'popup_shown' not in st.session_state:
    st.session_state.popup_shown = False

# Function to close popup
def close_popup():
    st.session_state.popup_shown = True

# Function to send email
def send_grievance_email(priority, grievance_text, timestamp):
    try:
        # Email configuration - you'll need to set up these credentials
        sender_email = "aryanistrying@gmail.com"  # Replace with your email
        sender_password = "iitw auam ilgv cszs"   # Replace with your app password
        receiver_email = "aryanistrying@gmail.com"
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"Grievance Priority: {priority}"
        
        # Email body
        body = f"""
        New Grievance Submitted
        
        Priority Level: {priority}
        Submission Time: {timestamp}
        
        Grievance Details:
        {grievance_text}
        
        ---
        Sent from Piyuu Grievance Portal 💖
        """
        
        message.attach(MIMEText(body, "plain"))
        
        # Gmail SMTP configuration
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send email
        text = message.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False

# Show popup on first load
if not st.session_state.popup_shown:
    # Check if there's an uploaded image or use the local image
    popup_image_html = ""
    
    # Try to use your local image first
    try:
        import base64
        with open("image.jpeg", "rb") as img_file:
            image_bytes = img_file.read()
            image_b64 = base64.b64encode(image_bytes).decode()
            popup_image_html = f'<img src="data:image/jpeg;base64,{image_b64}" alt="Love Image" class="popup-image" />'
    except FileNotFoundError:
        # Fallback to uploaded image if local file not found
        if 'popup_image' in st.session_state and st.session_state.popup_image is not None:
            import base64
            image_bytes = st.session_state.popup_image.read()
            st.session_state.popup_image.seek(0)
            image_b64 = base64.b64encode(image_bytes).decode()
            popup_image_html = f'<img src="data:image/png;base64,{image_b64}" alt="Love Image" class="popup-image" />'
        else:
            # Default heart emoji
            popup_image_html = '<div style="font-size: 60px; margin: 20px 0;">💖</div>'
    
    # Show popup as a card instead of overlay
    st.markdown(f"""
    <div class="popup-overlay">
        <div class="popup-content">
            <div class="popup-title">💖 Welcome Baby! 💖</div>
            {popup_image_html}
            <div class="popup-message">
                I'm sorry baby, I am stupid and I love you! 💕
            </div>
            <div style="font-size: 30px; margin: 20px 0; animation: bounce 2s infinite;">
                💖 🥺 💖 🥺 💖
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Button will now be clearly visible below the popup card
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💖 Close Welcome Message & Continue 💖", key="close_popup_btn"):
            st.session_state.popup_shown = True
            st.rerun()

# Only show main content if popup is closed
if st.session_state.popup_shown:
    
    # Sidebar for popup image upload (only show when popup is closed)
    with st.sidebar:
        st.markdown("### 🖼️ Popup Image Settings")
        uploaded_image = st.file_uploader(
            "Upload image for welcome popup",
            type=['png', 'jpg', 'jpeg', 'gif'],
            help="This image will appear in the welcome popup"
        )
        
        if uploaded_image is not None:
            st.session_state.popup_image = uploaded_image
            st.success("Image uploaded! It will show in the popup next time.")
            
        if st.button("🔄 Reset Popup (Test)"):
            st.session_state.popup_shown = False
            st.rerun()
    
    # Main header
    st.markdown('<h1 class="header-title">💖 Piyuu Grievance Portal 💖</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #880e4f; font-size: 20px; font-weight: bold;">✨ Share your concerns here. Arohi loves you💖✨</p>', unsafe_allow_html=True)

    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        # Grievance form
        with st.form(key='grievance_form', clear_on_submit=True):
            priority = st.selectbox(
                "⚡ Priority Level",
                ["Pat on head", "Forehead kiss", "Baby Me", "Slushies", "100 kisses on face", "Cuddle for multiple hours"],
                index=1
            )
            
            grievance_text = st.text_area(
                "💭 Tell us about your grievance...",
                placeholder="Please describe your concern in detail. I am here to listen! 💕",
                height=200
            )
            
            if st.form_submit_button("💖 Submit Grievance") and grievance_text:
                # Create grievance entry
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                grievance_entry = {
                    'id': len(st.session_state.grievances) + 1,
                    'priority': priority,
                    'text': grievance_text,
                    'timestamp': timestamp,
                    'status': 'Submitted'
                }
                
                st.session_state.grievances.append(grievance_entry)
                
                # Send email notification
                email_sent = send_grievance_email(priority, grievance_text, timestamp)
                
                if email_sent:
                    st.session_state.show_success = True
                    st.session_state.email_status = "sent"
                else:
                    st.session_state.show_success = True
                    st.session_state.email_status = "failed"
                
                st.rerun()
        
        # Success message
        if st.session_state.show_success:
            if hasattr(st.session_state, 'email_status'):
                if st.session_state.email_status == "sent":
                    st.markdown(
                        '<div class="success-message">✨ Thank you! Your grievance has been submitted successfully and emailed to Arohi! I care about your concerns! Our trained executive Arohi will be back with you shortly. In the meanwhile, I am sorry and I love you. 💕</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        '<div class="success-message">✨ Thank you! Your grievance has been submitted successfully. Email notification failed, but your grievance is saved. I care about your concerns! 💕</div>',
                        unsafe_allow_html=True
                    )
            else:
                st.markdown(
                    '<div class="success-message">✨ Thank you! Your grievance has been submitted successfully. I care about your concerns! Our trained executive Arohi will be back with you shortly. In the meanwhile, I am sorry and I love you. 💕</div>',
                    unsafe_allow_html=True
                )
            
            # Reset success message after showing
            if st.button("✅ Acknowledged"):
                st.session_state.show_success = False
                if hasattr(st.session_state, 'email_status'):
                    delattr(st.session_state, 'email_status')
                st.rerun()

    # Cute feature buttons section
    st.markdown("---")
    st.markdown('<h3 style="text-align: center; color: #880e4f; margin: 20px 0;">🎀 Cute Features to Brighten Your Day! 🎀</h3>', unsafe_allow_html=True)

    # Create columns for cute buttons
    cute_col1, cute_col2, cute_col3, cute_col4 = st.columns(4)

    with cute_col1:
        if st.button("🧸 Teddy Rain"):
            st.session_state.animation_active = True
            st.session_state.animation_type = "teddy"
            st.rerun()

    with cute_col2:
        if st.button("🌈 Rainbow Magic"):
            st.session_state.animation_active = True
            st.session_state.animation_type = "rainbow"
            st.rerun()

    with cute_col3:
        if st.button("💖 Heart Storm"):
            st.session_state.animation_active = True
            st.session_state.animation_type = "hearts"
            st.rerun()

    with cute_col4:
        if st.button("✨ Sparkle Shower"):
            st.session_state.animation_active = True
            st.session_state.animation_type = "sparkles"
            st.rerun()

    # Animation display
    if st.session_state.animation_active:
        if st.session_state.animation_type == "teddy":
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #ffe0f4 0%, #ffc1e3 100%); border-radius: 20px; margin: 20px 0; border: 3px solid #e91e63;">
                <div style="font-size: 40px; animation: bounce 1s infinite;">
                    🧸 🐻 🧸 🐨 🧸 🐻 🧸
                </div>
                <h2 style="color: #880e4f; margin: 15px 0;">Teddy Bear Hugs! 🤗</h2>
                <p style="color: #212529; font-size: 18px;">Sending you warm, cuddly teddy bear hugs! 💕</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif st.session_state.animation_type == "rainbow":
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); border-radius: 20px; margin: 20px 0; border: 3px solid #e91e63;">
                <div style="font-size: 40px; animation: bounce 1.5s infinite;">
                    🌈 🦄 🌈 ⭐ 🌈 🦄 🌈
                </div>
                <h2 style="color: #880e4f; margin: 15px 0;">Rainbow Magic! ✨</h2>
                <p style="color: #212529; font-size: 18px;">Every storm ends with a beautiful rainbow! 🌈</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif st.session_state.animation_type == "hearts":
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #ffeef8 0%, #ffe0f0 100%); border-radius: 20px; margin: 20px 0; border: 3px solid #e91e63;">
                <div style="font-size: 40px; animation: bounce 0.8s infinite;">
                    💖 💕 💗 💝 💘 💞 💖
                </div>
                <h2 style="color: #880e4f; margin: 15px 0;">Love & Support! 💕</h2>
                <p style="color: #212529; font-size: 18px;">You are loved and your feelings are valid! 💖</p>
            </div>
            """, unsafe_allow_html=True)
            
        elif st.session_state.animation_type == "sparkles":
            st.markdown("""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #e8f4f8 0%, #d1ecf1 100%); border-radius: 20px; margin: 20px 0; border: 3px solid #e91e63;">
                <div style="font-size: 40px; animation: bounce 1.2s infinite;">
                    ✨ ⭐ 🌟 💫 ⚡ 🎆 ✨
                </div>
                <h2 style="color: #880e4f; margin: 15px 0;">You're Amazing! ⭐</h2>
                <p style="color: #212529; font-size: 18px;">You sparkle brighter than any star! Keep shining! ✨</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Auto-hide after 3 seconds by adding a reset button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🌸 Close Animation"):
                st.session_state.animation_active = False
                st.rerun()

    # Footer
    st.markdown("---")
    st.markdown('<p style="text-align: center; color: #880e4f; font-style: italic; font-size: 18px; font-weight: bold;">💖 I love you Piyuuuuuuuuuuuu!💖</p>', unsafe_allow_html=True)