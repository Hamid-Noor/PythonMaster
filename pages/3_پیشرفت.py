import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta
from utils.persian_text import setup_persian_ui
from utils.database import DatabaseManager

# تنظیمات صفحه
st.set_page_config(
    page_title="پیشرفت - پلتفرم آموزش معکوس",
    page_icon="📊",
    layout="wide"
)

setup_persian_ui()

def main():
    st.title("📊 ردیابی پیشرفت")
    
    # اتصال به پایگاه داده
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = st.session_state.db_manager.get_or_create_user()
    
    # دریافت پیشرفت از پایگاه داده
    db_progress = st.session_state.db_manager.get_user_progress(st.session_state.user_id)
    db_statistics = st.session_state.db_manager.get_user_statistics(st.session_state.user_id)
    
    # بررسی وجود داده‌های پیشرفت
    if not db_progress and not st.session_state.user_progress:
        st.info("هنوز هیچ فعالیتی انجام نداده‌اید. ابتدا تمرین‌ها را حل کنید.")
        return
    
    # آمار کلی
    st.markdown("## 📈 آمار کلی")
    
    completed_exercises = st.session_state.user_progress.get('completed_exercises', [])
    quiz_scores = st.session_state.quiz_scores
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("تعداد تمرین‌های حل شده", len(completed_exercises))
    
    with col2:
        if completed_exercises:
            avg_score = sum(ex['score'] for ex in completed_exercises) / len(completed_exercises)
            st.metric("میانگین امتیاز", f"{avg_score:.1f}%")
        else:
            st.metric("میانگین امتیاز", "0%")
    
    with col3:
        if completed_exercises:
            best_score = max(ex['score'] for ex in completed_exercises)
            st.metric("بهترین امتیاز", f"{best_score:.1f}%")
        else:
            st.metric("بهترین امتیاز", "0%")
    
    with col4:
        if completed_exercises:
            difficulty_counts = {}
            for ex in completed_exercises:
                diff = ex['difficulty']
                difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
            
            most_common = max(difficulty_counts, key=difficulty_counts.get)
            st.metric("سطح فعال", most_common)
        else:
            st.metric("سطح فعال", "-")
    
    # نمودار پیشرفت
    if completed_exercises:
        st.markdown("---")
        st.markdown("## 📊 نمودارهای پیشرفت")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### نمودار امتیازات")
            
            # تبدیل داده‌ها به DataFrame
            df = pd.DataFrame(completed_exercises)
            
            # نمودار خطی امتیازات
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(range(len(df)), df['score'], marker='o', linewidth=2, markersize=8)
            ax.set_xlabel('تمرین')
            ax.set_ylabel('امتیاز (%)')
            ax.set_title('روند پیشرفت امتیازات')
            ax.grid(True, alpha=0.3)
            ax.set_ylim(0, 100)
            
            # اضافه کردن برچسب‌ها
            for i, score in enumerate(df['score']):
                ax.annotate(f'{score:.1f}%', (i, score), 
                          textcoords="offset points", xytext=(0,10), ha='center')
            
            st.pyplot(fig)
        
        with col2:
            st.markdown("### توزیع سطح دشواری")
            
            # نمودار دایره‌ای
            difficulty_counts = df['difficulty'].value_counts()
            
            fig, ax = plt.subplots(figsize=(8, 8))
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
            wedges, texts, autotexts = ax.pie(
                difficulty_counts.values, 
                labels=difficulty_counts.index,
                autopct='%1.1f%%',
                colors=colors,
                startangle=90
            )
            
            # تنظیم فونت برای متن فارسی
            for text in texts:
                text.set_fontsize(12)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
            
            ax.set_title('توزیع تمرین‌ها براساس سطح دشواری', fontsize=14, pad=20)
            st.pyplot(fig)
    
    # جدول تفصیلی
    if completed_exercises:
        st.markdown("---")
        st.markdown("## 📋 جزئیات تمرین‌ها")
        
        # تبدیل به DataFrame برای نمایش بهتر
        df = pd.DataFrame(completed_exercises)
        
        # تنظیم نام ستون‌ها
        df_display = df.copy()
        df_display.columns = ['عنوان', 'سطح', 'امتیاز', 'تکمیل شده']
        df_display['امتیاز'] = df_display['امتیاز'].apply(lambda x: f"{x:.1f}%")
        df_display['تکمیل شده'] = df_display['تکمیل شده'].apply(lambda x: "✅" if x else "❌")
        
        # رنگ‌آمیزی براساس امتیاز
        def highlight_score(val):
            if '%' in str(val):
                score = float(val.replace('%', ''))
                if score >= 80:
                    return 'background-color: #d4edda'
                elif score >= 60:
                    return 'background-color: #fff3cd'
                else:
                    return 'background-color: #f8d7da'
            return ''
        
        styled_df = df_display.style.applymap(highlight_score, subset=['امتیاز'])
        st.dataframe(styled_df, use_container_width=True)
    
    # پیشنهادات بهبود
    st.markdown("---")
    st.markdown("## 💡 پیشنهادات بهبود")
    
    if completed_exercises:
        avg_score = sum(ex['score'] for ex in completed_exercises) / len(completed_exercises)
        
        # تحلیل نقاط قوت و ضعف
        difficulty_performance = {}
        for ex in completed_exercises:
            diff = ex['difficulty']
            if diff not in difficulty_performance:
                difficulty_performance[diff] = []
            difficulty_performance[diff].append(ex['score'])
        
        # محاسبه میانگین برای هر سطح
        for diff in difficulty_performance:
            difficulty_performance[diff] = sum(difficulty_performance[diff]) / len(difficulty_performance[diff])
        
        # تولید پیشنهادات
        suggestions = []
        
        if avg_score < 70:
            suggestions.append("📚 نیاز به مطالعه بیشتر مفاهیم پایه دارید")
        
        if difficulty_performance:
            weakest_level = min(difficulty_performance, key=difficulty_performance.get)
            if difficulty_performance[weakest_level] < 60:
                suggestions.append(f"🎯 روی تمرین‌های سطح {weakest_level} تمرکز کنید")
        
        if len(completed_exercises) < 5:
            suggestions.append("🚀 تمرین‌های بیشتری حل کنید تا مهارت‌تان بهبود یابد")
        
        if not suggestions:
            suggestions.append("🎉 عملکرد شما عالی است! به تمرین‌های پیشرفته‌تر بروید")
        
        for suggestion in suggestions:
            st.info(suggestion)
    
    # اهداف و چالش‌ها
    st.markdown("---")
    st.markdown("## 🎯 اهداف و چالش‌ها")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### اهداف کوتاه‌مدت:")
        daily_goals = [
            "حل 2 تمرین در روز",
            "دستیابی به امتیاز بالای 80%",
            "تکمیل تمرین‌های سطح مبتدی"
        ]
        
        for goal in daily_goals:
            st.markdown(f"- {goal}")
    
    with col2:
        st.markdown("### چالش‌های هفتگی:")
        weekly_challenges = [
            "تحلیل 10 کد مختلف",
            "حل تمرین‌های سطح متوسط",
            "دستیابی به میانگین امتیاز 85%"
        ]
        
        for challenge in weekly_challenges:
            st.markdown(f"- {challenge}")
    
    # دکمه بازنشانی پیشرفت
    st.markdown("---")
    if st.button("🔄 بازنشانی پیشرفت", type="secondary"):
        if st.button("تایید بازنشانی", type="primary"):
            st.session_state.user_progress = {}
            st.session_state.quiz_scores = {}
            st.success("پیشرفت با موفقیت بازنشانی شد")
            st.rerun()

if __name__ == "__main__":
    main()
