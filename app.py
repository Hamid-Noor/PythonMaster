import streamlit as st
import json
import os
from utils.persian_text import setup_persian_ui, get_text
from utils.database import DatabaseManager

# تنظیمات اولیه صفحه
st.set_page_config(
    page_title="پلتفرم آموزش معکوس برنامه‌نویسی پایتون",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنظیم زبان فارسی
setup_persian_ui()

def initialize_session_state():
    """مقداردهی اولیه متغیرهای جلسه"""
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
        st.session_state.db_manager.populate_default_exercises()
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = st.session_state.db_manager.get_or_create_user()
    
    if 'user_progress' not in st.session_state:
        st.session_state.user_progress = {}
    if 'current_exercise' not in st.session_state:
        st.session_state.current_exercise = 0
    if 'quiz_scores' not in st.session_state:
        st.session_state.quiz_scores = {}

def load_user_progress():
    """بارگذاری پیشرفت کاربر از فایل"""
    try:
        if os.path.exists('data/progress.json'):
            with open('data/progress.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_user_progress():
    """ذخیره پیشرفت کاربر در فایل"""
    try:
        os.makedirs('data', exist_ok=True)
        with open('data/progress.json', 'w', encoding='utf-8') as f:
            json.dump(st.session_state.user_progress, f, ensure_ascii=False, indent=2)
    except:
        pass

def main():
    """صفحه اصلی برنامه"""
    initialize_session_state()
    
    # بارگذاری پیشرفت کاربر
    if not st.session_state.user_progress:
        st.session_state.user_progress = load_user_progress()
    
    # سایدبار
    with st.sidebar:
        st.markdown("## 🐍 پلتفرم آموزش معکوس")
        st.markdown("### برنامه‌نویسی پایتون")
        
        # نمایش آمار کلی
        total_exercises = len(st.session_state.user_progress.get('completed_exercises', []))
        st.metric("تمرین‌های تکمیل شده", total_exercises)
        
        avg_score = 0
        if st.session_state.quiz_scores:
            avg_score = sum(st.session_state.quiz_scores.values()) / len(st.session_state.quiz_scores)
        st.metric("میانگین امتیاز", f"{avg_score:.1f}%")
        
        st.markdown("---")
        st.markdown("**راهنمای استفاده:**")
        st.markdown("1. از منوی سمت چپ برای تحلیل کد استفاده کنید")
        st.markdown("2. تمرین‌ها را به ترتیب حل کنید")
        st.markdown("3. پیشرفت خود را بررسی کنید")
    
    # محتوای اصلی
    st.title("🎯 پلتفرم آموزش معکوس برنامه‌نویسی پایتون")
    
    st.markdown("""
    ## خوش آمدید! 👋
    
    این پلتفرم برای کمک به شما در یادگیری تحلیل و درک کد پایتون طراحی شده است.
    با استفاده از ابزارهای تعاملی موجود، می‌توانید:
    
    ### ✨ امکانات موجود:
    - **تحلیل کد**: کد پایتون را گام به گام تحلیل کنید
    - **نمودار جریان**: نمایش بصری ساختار برنامه
    - **تمرین‌های عملی**: حل مسائل واقعی با راهنمایی
    - **ردیابی پیشرفت**: مشاهده عملکرد و پیشرفت خود
    
    ### 🚀 نحوه شروع:
    1. از منوی سمت چپ، صفحه "تحلیل کد" را انتخاب کنید
    2. کد مورد نظر را وارد کنید یا از نمونه‌ها استفاده کنید
    3. تحلیل گام به گام را مطالعه کنید
    4. با تمرین‌ها مهارت خود را تقویت کنید
    
    ### 📚 سطوح آموزشی:
    - **مبتدی**: متغیرها، حلقه‌ها، شرطی‌ها
    - **متوسط**: توابع، کلاس‌ها، استثناها
    - **پیشرفته**: الگوریتم‌ها، ساختارهای داده پیچیده
    """)
    
    # نمایش آمار کلی
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("🎯 تحلیل کد تعاملی")
        st.markdown("کد را گام به گام بررسی کنید")
    
    with col2:
        st.success("🧩 تمرین‌های عملی")
        st.markdown("با حل مسائل واقعی یاد بگیرید")
    
    with col3:
        st.warning("📊 ردیابی پیشرفت")
        st.markdown("عملکرد خود را مشاهده کنید")
    
    # نمایش تمرین‌های اخیر
    st.markdown("---")
    st.markdown("## 📝 تمرین‌های پیشنهادی")
    
    sample_exercises = [
        {"title": "تحلیل حلقه for", "difficulty": "مبتدی", "description": "نحوه کارکرد حلقه‌ها"},
        {"title": "درک توابع", "difficulty": "متوسط", "description": "تعریف و استفاده از توابع"},
        {"title": "کار با کلاس‌ها", "difficulty": "پیشرفته", "description": "برنامه‌نویسی شی‌گرا"}
    ]
    
    cols = st.columns(len(sample_exercises))
    for i, exercise in enumerate(sample_exercises):
        with cols[i]:
            st.markdown(f"**{exercise['title']}**")
            st.markdown(f"سطح: {exercise['difficulty']}")
            st.markdown(f"توضیح: {exercise['description']}")
            if st.button(f"شروع", key=f"start_{i}"):
                st.switch_page("pages/2_تمرین_ها.py")
    
    # ذخیره پیشرفت
    save_user_progress()

if __name__ == "__main__":
    main()
