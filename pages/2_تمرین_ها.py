import streamlit as st
import json
import random
from utils.exercise_manager import ExerciseManager
from utils.database import DatabaseManager
from utils.code_analyzer import CodeAnalyzer
from utils.persian_text import setup_persian_ui

# تنظیمات صفحه
st.set_page_config(
    page_title="تمرین‌ها - پلتفرم آموزش معکوس",
    page_icon="🧩",
    layout="wide"
)

setup_persian_ui()

def main():
    st.title("🧩 تمرین‌های عملی")
    
    # مدیریت تمرین‌ها
    if 'db_manager' not in st.session_state:
        st.session_state.db_manager = DatabaseManager()
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = st.session_state.db_manager.get_or_create_user()
    
    exercises = st.session_state.db_manager.get_exercises()
    
    if not exercises:
        st.error("هیچ تمرینی یافت نشد")
        return
    
    # انتخاب سطح دشواری
    difficulty_levels = ["مبتدی", "متوسط", "پیشرفته"]
    selected_difficulty = st.selectbox(
        "سطح دشواری را انتخاب کنید:",
        difficulty_levels
    )
    
    # فیلتر تمرین‌ها براساس سطح
    filtered_exercises = [
        ex for ex in exercises 
        if ex.get('difficulty') == selected_difficulty
    ]
    
    if not filtered_exercises:
        st.warning(f"هیچ تمرینی برای سطح {selected_difficulty} یافت نشد")
        return
    
    # انتخاب تمرین
    exercise_titles = [ex['title'] for ex in filtered_exercises]
    selected_exercise_idx = st.selectbox(
        "تمرین را انتخاب کنید:",
        range(len(exercise_titles)),
        format_func=lambda x: exercise_titles[x]
    )
    
    current_exercise = filtered_exercises[selected_exercise_idx]
    
    # نمایش تمرین
    st.markdown("---")
    st.markdown(f"## 📝 {current_exercise['title']}")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # توضیحات تمرین
        st.markdown("### 📖 توضیحات:")
        st.markdown(current_exercise['description'])
        
        # نمایش کد
        st.markdown("### 💻 کد برای تحلیل:")
        st.code(current_exercise['code'], language="python")
        
        # سوالات
        st.markdown("### ❓ سوالات:")
        
        user_answers = {}
        for i, question in enumerate(current_exercise['questions']):
            st.markdown(f"**سوال {i+1}:** {question['question']}")
            
            if question['type'] == 'multiple_choice':
                user_answers[i] = st.radio(
                    "پاسخ را انتخاب کنید:",
                    question['options'],
                    key=f"q_{selected_exercise_idx}_{i}"
                )
            elif question['type'] == 'text':
                user_answers[i] = st.text_area(
                    "پاسخ خود را بنویسید:",
                    key=f"q_{selected_exercise_idx}_{i}",
                    height=100
                )
            elif question['type'] == 'code':
                user_answers[i] = st.text_area(
                    "کد خود را بنویسید:",
                    key=f"q_{selected_exercise_idx}_{i}",
                    height=150
                )
        
        # بررسی پاسخ‌ها
        if st.button("بررسی پاسخ‌ها", type="primary"):
            score = 0
            total_questions = len(current_exercise['questions'])
            
            for i, question in enumerate(current_exercise['questions']):
                user_answer = user_answers.get(i, "")
                correct_answer = question['answer']
                
                if question['type'] == 'multiple_choice':
                    if user_answer == correct_answer:
                        score += 1
                        st.success(f"✅ سوال {i+1}: صحیح")
                    else:
                        st.error(f"❌ سوال {i+1}: نادرست - پاسخ صحیح: {correct_answer}")
                
                elif question['type'] == 'text':
                    # برای سوالات متنی، بررسی ساده
                    if correct_answer.lower() in user_answer.lower():
                        score += 1
                        st.success(f"✅ سوال {i+1}: صحیح")
                    else:
                        st.error(f"❌ سوال {i+1}: پاسخ صحیح: {correct_answer}")
                
                elif question['type'] == 'code':
                    # برای کد، بررسی ساده وجود کلیدواژه‌ها
                    if any(keyword in user_answer for keyword in correct_answer.split()):
                        score += 1
                        st.success(f"✅ سوال {i+1}: صحیح")
                    else:
                        st.error(f"❌ سوال {i+1}: نمونه پاسخ صحیح:")
                        st.code(correct_answer, language="python")
            
            # محاسبه و نمایش نتیجه
            percentage = (score / total_questions) * 100
            st.markdown("---")
            st.markdown(f"## 📊 نتیجه: {score}/{total_questions} ({percentage:.1f}%)")
            
            if percentage >= 80:
                st.success("🎉 عالی! به تمرین بعدی بروید")
            elif percentage >= 60:
                st.warning("⚠️ خوب! اما می‌توانید بهتر شوید")
            else:
                st.error("❌ نیاز به مطالعه بیشتر دارید")
            
            # ذخیره پیشرفت در پایگاه داده
            st.session_state.db_manager.save_user_progress(
                user_id=st.session_state.user_id,
                exercise_id=current_exercise['id'],
                completed=percentage >= 60,  # حداقل 60% برای تکمیل
                score=percentage
            )
            
            # به‌روزرسانی آمار کاربر
            st.session_state.db_manager.update_user_statistics(st.session_state.user_id)
            
            # ذخیره در session state برای سازگاری
            if 'completed_exercises' not in st.session_state.user_progress:
                st.session_state.user_progress['completed_exercises'] = []
            
            exercise_result = {
                'title': current_exercise['title'],
                'difficulty': current_exercise['difficulty'],
                'score': percentage,
                'completed': percentage >= 60
            }
            
            # به‌روزرسانی یا اضافه کردن نتیجه
            existing_idx = None
            for idx, ex in enumerate(st.session_state.user_progress['completed_exercises']):
                if ex['title'] == current_exercise['title']:
                    existing_idx = idx
                    break
            
            if existing_idx is not None:
                st.session_state.user_progress['completed_exercises'][existing_idx] = exercise_result
            else:
                st.session_state.user_progress['completed_exercises'].append(exercise_result)
            
            # ذخیره امتیاز کوئیز
            if 'quiz_scores' not in st.session_state:
                st.session_state.quiz_scores = {}
            st.session_state.quiz_scores[current_exercise['title']] = percentage
    
    with col2:
        # راهنمایی و نکات
        st.markdown("### 💡 راهنمایی:")
        
        if current_exercise.get('hints'):
            for hint in current_exercise['hints']:
                st.info(hint)
        
        # نمایش مفاهیم کلیدی
        if current_exercise.get('concepts'):
            st.markdown("### 🔑 مفاهیم کلیدی:")
            for concept in current_exercise['concepts']:
                st.markdown(f"- {concept}")
        
        # پیشنهاد تمرین‌های مرتبط
        st.markdown("### 🔗 تمرین‌های مرتبط:")
        related_exercises = [
            ex for ex in filtered_exercises 
            if ex['title'] != current_exercise['title']
        ]
        
        if related_exercises:
            for ex in related_exercises[:3]:  # نمایش 3 تمرین مرتبط
                if st.button(f"📚 {ex['title']}", key=f"related_{ex['title']}"):
                    st.rerun()
    
    # نمایش آمار کلی
    st.markdown("---")
    st.markdown("## 📈 آمار پیشرفت")
    
    if st.session_state.user_progress.get('completed_exercises'):
        completed = st.session_state.user_progress['completed_exercises']
        
        # آمار براساس سطح
        difficulty_stats = {}
        for ex in completed:
            diff = ex['difficulty']
            if diff not in difficulty_stats:
                difficulty_stats[diff] = {'count': 0, 'avg_score': 0}
            difficulty_stats[diff]['count'] += 1
            difficulty_stats[diff]['avg_score'] += ex['score']
        
        # محاسبه میانگین
        for diff in difficulty_stats:
            difficulty_stats[diff]['avg_score'] /= difficulty_stats[diff]['count']
        
        # نمایش آمار
        cols = st.columns(len(difficulty_stats))
        for i, (diff, stats) in enumerate(difficulty_stats.items()):
            with cols[i]:
                st.metric(
                    f"سطح {diff}",
                    f"{stats['count']} تمرین",
                    f"{stats['avg_score']:.1f}% میانگین"
                )

if __name__ == "__main__":
    main()
