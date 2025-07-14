import streamlit as st
import ast
import sys
from io import StringIO
from contextlib import redirect_stdout
from utils.code_analyzer import CodeAnalyzer
from utils.flowchart_generator import FlowchartGenerator
from utils.persian_text import setup_persian_ui

# تنظیمات صفحه
st.set_page_config(
    page_title="تحلیل کد - پلتفرم آموزش معکوس",
    page_icon="🔍",
    layout="wide"
)

setup_persian_ui()

def main():
    st.title("🔍 تحلیل کد پایتون")
    
    # نمونه کدهای از پیش تعریف شده
    sample_codes = {
        "حلقه ساده": """for i in range(5):
    print(f"شماره: {i}")
    if i == 3:
        print("سه رسیدیم!")""",
        
        "تابع محاسبه": """def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

result = calculate_sum([1, 2, 3, 4, 5])
print(f"مجموع: {result}")""",
        
        "کلاس ساده": """class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"سلام، من {self.name} هستم و {self.age} سال دارم"

student = Student("علی", 20)
print(student.introduce())""",
        
        "مدیریت استثنا": """def divide_numbers(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "خطا: تقسیم بر صفر"
    except Exception as e:
        return f"خطا: {e}"

print(divide_numbers(10, 2))
print(divide_numbers(10, 0))"""
    }
    
    # انتخاب نوع ورودی
    input_type = st.radio(
        "نوع ورودی را انتخاب کنید:",
        ["کد دستی", "نمونه کد"],
        horizontal=True
    )
    
    if input_type == "نمونه کد":
        selected_sample = st.selectbox(
            "نمونه کد را انتخاب کنید:",
            list(sample_codes.keys())
        )
        code = sample_codes[selected_sample]
        st.code(code, language="python")
    else:
        code = st.text_area(
            "کد پایتون خود را وارد کنید:",
            height=300,
            placeholder="# کد پایتون خود را اینجا بنویسید...\nprint('سلام دنیا!')"
        )
    
    if code.strip():
        # تحلیل کد
        analyzer = CodeAnalyzer()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("## 📊 تحلیل ساختار کد")
            
            try:
                # تحلیل AST
                tree = ast.parse(code)
                analysis = analyzer.analyze_code(code)
                
                # نمایش اطلاعات کلی
                st.markdown("### اطلاعات کلی:")
                st.write(f"- تعداد خطوط: {len(code.splitlines())}")
                st.write(f"- تعداد متغیرها: {len(analysis.get('variables', []))}")
                st.write(f"- تعداد توابع: {len(analysis.get('functions', []))}")
                st.write(f"- تعداد کلاس‌ها: {len(analysis.get('classes', []))}")
                
                # نمایش متغیرها
                if analysis.get('variables'):
                    st.markdown("### 🔤 متغیرها:")
                    for var in analysis['variables']:
                        st.write(f"- `{var}`")
                
                # نمایش توابع
                if analysis.get('functions'):
                    st.markdown("### 🔧 توابع:")
                    for func in analysis['functions']:
                        st.write(f"- `{func['name']}` (خط {func['line']})")
                        if func.get('args'):
                            st.write(f"  - پارامترها: {', '.join(func['args'])}")
                
                # نمایش کلاس‌ها
                if analysis.get('classes'):
                    st.markdown("### 📦 کلاس‌ها:")
                    for cls in analysis['classes']:
                        st.write(f"- `{cls['name']}` (خط {cls['line']})")
                        if cls.get('methods'):
                            st.write(f"  - متدها: {', '.join(cls['methods'])}")
                
                # نمایش وابستگی‌ها
                if analysis.get('imports'):
                    st.markdown("### 📚 وابستگی‌ها:")
                    for imp in analysis['imports']:
                        st.write(f"- `{imp}`")
                
            except SyntaxError as e:
                st.error(f"خطای نحوی در کد: {e}")
            except Exception as e:
                st.error(f"خطا در تحلیل کد: {e}")
        
        with col2:
            st.markdown("## 🎯 اجرای گام به گام")
            
            # اجرای کد
            if st.button("اجرای کد", type="primary"):
                with st.spinner("در حال اجرا..."):
                    try:
                        # capture output
                        old_stdout = sys.stdout
                        sys.stdout = captured_output = StringIO()
                        
                        # اجرای کد
                        exec(code)
                        
                        # restore stdout
                        sys.stdout = old_stdout
                        
                        # نمایش خروجی
                        output = captured_output.getvalue()
                        if output:
                            st.markdown("### 📤 خروجی:")
                            st.code(output, language="text")
                        else:
                            st.info("کد بدون خروجی اجرا شد")
                            
                    except Exception as e:
                        sys.stdout = old_stdout
                        st.error(f"خطا در اجرای کد: {e}")
            
            # نمایش نمودار جریان
            st.markdown("## 📈 نمودار جریان")
            
            if st.button("تولید نمودار"):
                try:
                    flowchart_gen = FlowchartGenerator()
                    flowchart = flowchart_gen.generate_flowchart(code)
                    
                    if flowchart:
                        st.graphviz_chart(flowchart)
                    else:
                        st.warning("امکان تولید نمودار جریان وجود ندارد")
                        
                except Exception as e:
                    st.error(f"خطا در تولید نمودار: {e}")
        
        # بخش تفسیر و آموزش
        st.markdown("---")
        st.markdown("## 📚 تفسیر و آموزش")
        
        # تولید توضیحات خودکار
        explanations = analyzer.generate_explanations(code)
        
        if explanations:
            for explanation in explanations:
                with st.expander(f"📖 {explanation['title']}"):
                    st.markdown(explanation['content'])
        
        # بخش سوالات و راهنمایی
        st.markdown("## ❓ سوالات و راهنمایی")
        
        questions = analyzer.generate_questions(code)
        
        if questions:
            for i, question in enumerate(questions):
                with st.expander(f"سوال {i+1}: {question['question']}"):
                    user_answer = st.text_area(
                        "پاسخ شما:",
                        key=f"answer_{i}",
                        height=100
                    )
                    
                    if st.button(f"نمایش پاسخ", key=f"show_answer_{i}"):
                        st.success(f"پاسخ: {question['answer']}")
                        
                        if question.get('hint'):
                            st.info(f"راهنمایی: {question['hint']}")

if __name__ == "__main__":
    main()
