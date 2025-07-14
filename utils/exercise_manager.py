import json
import os
import random
from typing import List, Dict, Any, Optional

class ExerciseManager:
    """مدیریت تمرین‌ها و بارگذاری آن‌ها"""
    
    def __init__(self, exercises_file: str = "data/exercises.json"):
        self.exercises_file = exercises_file
        self.exercises = []
        self.current_exercise_index = 0
    
    def load_exercises(self) -> List[Dict[str, Any]]:
        """بارگذاری تمرین‌ها از فایل"""
        try:
            if os.path.exists(self.exercises_file):
                with open(self.exercises_file, 'r', encoding='utf-8') as f:
                    self.exercises = json.load(f)
            else:
                # اگر فایل وجود ندارد، تمرین‌های پیش‌فرض ایجاد کن
                self.exercises = self._create_default_exercises()
                self.save_exercises()
            
            return self.exercises
        except Exception as e:
            print(f"خطا در بارگذاری تمرین‌ها: {e}")
            return self._create_default_exercises()
    
    def save_exercises(self) -> bool:
        """ذخیره تمرین‌ها در فایل"""
        try:
            os.makedirs(os.path.dirname(self.exercises_file), exist_ok=True)
            with open(self.exercises_file, 'w', encoding='utf-8') as f:
                json.dump(self.exercises, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"خطا در ذخیره تمرین‌ها: {e}")
            return False
    
    def _create_default_exercises(self) -> List[Dict[str, Any]]:
        """ایجاد تمرین‌های پیش‌فرض"""
        return [
            {
                "id": 1,
                "title": "تحلیل حلقه for ساده",
                "difficulty": "مبتدی",
                "description": "در این تمرین، نحوه کارکرد حلقه for در پایتون را یاد خواهید گرفت.",
                "code": """for i in range(5):
    print(f"عدد: {i}")
    if i == 3:
        print("رسیدیم به سه!")""",
                "concepts": [
                    "حلقه for",
                    "تابع range",
                    "f-string",
                    "دستور if"
                ],
                "hints": [
                    "حلقه for از 0 شروع می‌شود",
                    "range(5) اعداد 0 تا 4 تولید می‌کند",
                    "f-string برای قالب‌بندی رشته استفاده می‌شود"
                ],
                "questions": [
                    {
                        "question": "این حلقه چند بار اجرا می‌شود؟",
                        "type": "multiple_choice",
                        "options": ["4 بار", "5 بار", "6 بار", "نامحدود"],
                        "answer": "5 بار"
                    },
                    {
                        "question": "مقدار i در اولین تکرار چیست؟",
                        "type": "multiple_choice",
                        "options": ["0", "1", "2", "3"],
                        "answer": "0"
                    },
                    {
                        "question": "چه زمانی پیام 'رسیدیم به سه!' چاپ می‌شود؟",
                        "type": "text",
                        "answer": "وقتی i برابر 3 باشد"
                    }
                ]
            },
            {
                "id": 2,
                "title": "تحلیل تابع محاسبه مجموع",
                "difficulty": "متوسط",
                "description": "در این تمرین، نحوه تعریف و استفاده از توابع را بررسی می‌کنیم.",
                "code": """def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

result = calculate_sum([1, 2, 3, 4, 5])
print(f"مجموع: {result}")""",
                "concepts": [
                    "تعریف تابع",
                    "پارامتر تابع",
                    "حلقه for",
                    "return statement",
                    "فراخوانی تابع"
                ],
                "hints": [
                    "تابع با کلیدواژه def تعریف می‌شود",
                    "پارامتر numbers لیستی از اعداد دریافت می‌کند",
                    "متغیر total برای جمع کردن استفاده می‌شود"
                ],
                "questions": [
                    {
                        "question": "نام تابع چیست؟",
                        "type": "text",
                        "answer": "calculate_sum"
                    },
                    {
                        "question": "این تابع چه کاری انجام می‌دهد؟",
                        "type": "multiple_choice",
                        "options": ["اعداد را ضرب می‌کند", "اعداد را جمع می‌کند", "اعداد را تقسیم می‌کند", "اعداد را کم می‌کند"],
                        "answer": "اعداد را جمع می‌کند"
                    },
                    {
                        "question": "مقدار بازگشتی تابع برای لیست [1, 2, 3, 4, 5] چیست؟",
                        "type": "multiple_choice",
                        "options": ["10", "15", "20", "25"],
                        "answer": "15"
                    }
                ]
            },
            {
                "id": 3,
                "title": "تحلیل کلاس Student",
                "difficulty": "پیشرفته",
                "description": "در این تمرین، مفاهیم برنامه‌نویسی شی‌گرا را بررسی می‌کنیم.",
                "code": """class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def introduce(self):
        return f"سلام، من {self.name} هستم و {self.age} سال دارم"
    
    def is_adult(self):
        return self.age >= 18

student = Student("علی", 20)
print(student.introduce())
print(f"بزرگسال است: {student.is_adult()}")""",
                "concepts": [
                    "تعریف کلاس",
                    "سازنده (__init__)",
                    "متدهای کلاس",
                    "self parameter",
                    "ایجاد شیء",
                    "فراخوانی متد"
                ],
                "hints": [
                    "کلاس با کلیدواژه class تعریف می‌شود",
                    "__init__ سازنده کلاس است",
                    "self به شیء جاری اشاره می‌کند",
                    "متدها توابع درون کلاس هستند"
                ],
                "questions": [
                    {
                        "question": "نام کلاس چیست؟",
                        "type": "text",
                        "answer": "Student"
                    },
                    {
                        "question": "متد __init__ چه کاری انجام می‌دهد؟",
                        "type": "multiple_choice",
                        "options": ["شیء را حذف می‌کند", "شیء را مقداردهی می‌کند", "شیء را کپی می‌کند", "شیء را چاپ می‌کند"],
                        "answer": "شیء را مقداردهی می‌کند"
                    },
                    {
                        "question": "متد is_adult چه زمانی True برمی‌گرداند؟",
                        "type": "text",
                        "answer": "وقتی سن 18 یا بیشتر باشد"
                    }
                ]
            },
            {
                "id": 4,
                "title": "مدیریت استثنا",
                "difficulty": "متوسط",
                "description": "در این تمرین، نحوه مدیریت خطاها و استثناها را یاد می‌گیریم.",
                "code": """def divide_numbers(a, b):
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        return "خطا: تقسیم بر صفر"
    except Exception as e:
        return f"خطا: {e}"

print(divide_numbers(10, 2))
print(divide_numbers(10, 0))
print(divide_numbers("10", 2))""",
                "concepts": [
                    "try-except",
                    "مدیریت استثنا",
                    "ZeroDivisionError",
                    "Exception handling",
                    "نوع خطا"
                ],
                "hints": [
                    "try-except برای مدیریت خطا استفاده می‌شود",
                    "ZeroDivisionError هنگام تقسیم بر صفر رخ می‌دهد",
                    "Exception کلاس والد همه خطاهاست"
                ],
                "questions": [
                    {
                        "question": "نتیجه divide_numbers(10, 2) چیست؟",
                        "type": "multiple_choice",
                        "options": ["5.0", "خطا: تقسیم بر صفر", "خطا", "10"],
                        "answer": "5.0"
                    },
                    {
                        "question": "نتیجه divide_numbers(10, 0) چیست؟",
                        "type": "multiple_choice",
                        "options": ["0", "خطا: تقسیم بر صفر", "inf", "None"],
                        "answer": "خطا: تقسیم بر صفر"
                    },
                    {
                        "question": "چرا از try-except استفاده می‌شود؟",
                        "type": "text",
                        "answer": "برای مدیریت خطاها و جلوگیری از توقف برنامه"
                    }
                ]
            },
            {
                "id": 5,
                "title": "کار با لیست و حلقه",
                "difficulty": "مبتدی",
                "description": "در این تمرین، کار با لیست‌ها و حلقه‌ها را یاد می‌گیریم.",
                "code": """numbers = [1, 2, 3, 4, 5]
even_numbers = []

for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)

print(f"اعداد زوج: {even_numbers}")
print(f"تعداد اعداد زوج: {len(even_numbers)}")""",
                "concepts": [
                    "لیست",
                    "حلقه for",
                    "شرط if",
                    "عملگر modulo",
                    "متد append",
                    "تابع len"
                ],
                "hints": [
                    "عملگر % باقی‌مانده تقسیم را برمی‌گرداند",
                    "اعداد زوج باقی‌مانده تقسیم بر 2 آنها صفر است",
                    "append برای اضافه کردن به لیست استفاده می‌شود"
                ],
                "questions": [
                    {
                        "question": "کدام اعداد در لیست even_numbers قرار می‌گیرند؟",
                        "type": "multiple_choice",
                        "options": ["[1, 3, 5]", "[2, 4]", "[1, 2, 3, 4, 5]", "[]"],
                        "answer": "[2, 4]"
                    },
                    {
                        "question": "تعداد اعداد زوج چیست؟",
                        "type": "multiple_choice",
                        "options": ["1", "2", "3", "4"],
                        "answer": "2"
                    },
                    {
                        "question": "شرط num % 2 == 0 چه کاری انجام می‌دهد؟",
                        "type": "text",
                        "answer": "بررسی می‌کند که آیا عدد زوج است یا نه"
                    }
                ]
            },
            {
                "id": 6,
                "title": "تحلیل دیکشنری",
                "difficulty": "متوسط",
                "description": "در این تمرین، کار با دیکشنری‌ها را یاد می‌گیریم.",
                "code": """student_grades = {
    "علی": 85,
    "فاطمه": 92,
    "حسن": 78,
    "زهرا": 95
}

total_grade = 0
student_count = 0

for name, grade in student_grades.items():
    print(f"{name}: {grade}")
    total_grade += grade
    student_count += 1

average = total_grade / student_count
print(f"میانگین نمرات: {average:.2f}")""",
                "concepts": [
                    "دیکشنری",
                    "حلقه for",
                    "متد items",
                    "کلید و مقدار",
                    "محاسبه میانگین",
                    "قالب‌بندی اعداد"
                ],
                "hints": [
                    "دیکشنری جفت کلید-مقدار ذخیره می‌کند",
                    "items() کلید و مقدار را برمی‌گرداند",
                    ":.2f برای نمایش 2 رقم اعشار استفاده می‌شود"
                ],
                "questions": [
                    {
                        "question": "میانگین نمرات چیست؟",
                        "type": "multiple_choice",
                        "options": ["85.5", "87.5", "90.0", "92.5"],
                        "answer": "87.5"
                    },
                    {
                        "question": "متد items() چه کاری انجام می‌دهد؟",
                        "type": "multiple_choice",
                        "options": ["فقط کلیدها را برمی‌گرداند", "فقط مقدارها را برمی‌گرداند", "کلید و مقدار را برمی‌گرداند", "طول دیکشنری را برمی‌گرداند"],
                        "answer": "کلید و مقدار را برمی‌گرداند"
                    },
                    {
                        "question": "تعداد دانش‌آموزان چیست؟",
                        "type": "text",
                        "answer": "4"
                    }
                ]
            },
            {
                "id": 7,
                "title": "تحلیل تابع بازگشتی",
                "difficulty": "پیشرفته",
                "description": "در این تمرین، مفهوم بازگشت (recursion) را بررسی می‌کنیم.",
                "code": """def factorial(n):
    if n == 0 or n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

print(f"فاکتوریل 5: {factorial(5)}")
print(f"فیبوناچی 6: {fibonacci(6)}")""",
                "concepts": [
                    "بازگشت (recursion)",
                    "شرط پایان",
                    "فاکتوریل",
                    "فیبوناچی",
                    "تابع بازگشتی"
                ],
                "hints": [
                    "تابع بازگشتی خودش را فراخوانی می‌کند",
                    "شرط پایان برای جلوگیری از بی‌نهایت لازم است",
                    "فاکتوریل n برابر n! = n × (n-1)! است"
                ],
                "questions": [
                    {
                        "question": "فاکتوریل 5 چیست؟",
                        "type": "multiple_choice",
                        "options": ["24", "60", "120", "720"],
                        "answer": "120"
                    },
                    {
                        "question": "فیبوناچی 6 چیست؟",
                        "type": "multiple_choice",
                        "options": ["5", "8", "13", "21"],
                        "answer": "8"
                    },
                    {
                        "question": "چرا شرط پایان در تابع بازگشتی مهم است؟",
                        "type": "text",
                        "answer": "برای جلوگیری از بی‌نهایت شدن فراخوانی‌ها"
                    }
                ]
            },
            {
                "id": 8,
                "title": "کار با فایل",
                "difficulty": "متوسط",
                "description": "در این تمرین، نحوه کار با فایل‌ها را یاد می‌گیریم.",
                "code": """def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return "فایل یافت نشد"
    except Exception as e:
        return f"خطا: {e}"

def write_file(filename, content):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
            return "فایل با موفقیت ذخیره شد"
    except Exception as e:
        return f"خطا: {e}"

content = "سلام دنیا!"
result = write_file("test.txt", content)
print(result)""",
                "concepts": [
                    "کار با فایل",
                    "with statement",
                    "encoding",
                    "FileNotFoundError",
                    "خواندن فایل",
                    "نوشتن فایل"
                ],
                "hints": [
                    "with statement فایل را خودکار می‌بندد",
                    "encoding='utf-8' برای متن فارسی ضروری است",
                    "'r' برای خواندن و 'w' برای نوشتن استفاده می‌شود"
                ],
                "questions": [
                    {
                        "question": "با چه دستوری فایل باز می‌شود؟",
                        "type": "multiple_choice",
                        "options": ["open()", "read()", "write()", "file()"],
                        "answer": "open()"
                    },
                    {
                        "question": "مزیت استفاده از with statement چیست؟",
                        "type": "text",
                        "answer": "فایل را خودکار می‌بندد"
                    },
                    {
                        "question": "encoding='utf-8' چرا مهم است؟",
                        "type": "text",
                        "answer": "برای پشتیبانی از متن فارسی"
                    }
                ]
            }
        ]
    
    def get_exercise_by_id(self, exercise_id: int) -> Optional[Dict[str, Any]]:
        """دریافت تمرین براساس شناسه"""
        for exercise in self.exercises:
            if exercise.get('id') == exercise_id:
                return exercise
        return None
    
    def get_exercises_by_difficulty(self, difficulty: str) -> List[Dict[str, Any]]:
        """دریافت تمرین‌ها براساس سطح دشواری"""
        return [ex for ex in self.exercises if ex.get('difficulty') == difficulty]
    
    def get_random_exercise(self, difficulty: str = None) -> Optional[Dict[str, Any]]:
        """دریافت تمرین تصادفی"""
        available_exercises = self.exercises
        
        if difficulty:
            available_exercises = self.get_exercises_by_difficulty(difficulty)
        
        if not available_exercises:
            return None
        
        return random.choice(available_exercises)
    
    def add_exercise(self, exercise: Dict[str, Any]) -> bool:
        """اضافه کردن تمرین جدید"""
        try:
            # تعیین شناسه جدید
            max_id = max([ex.get('id', 0) for ex in self.exercises], default=0)
            exercise['id'] = max_id + 1
            
            # اعتبارسنجی تمرین
            if not self._validate_exercise(exercise):
                return False
            
            self.exercises.append(exercise)
            return self.save_exercises()
        except Exception as e:
            print(f"خطا در اضافه کردن تمرین: {e}")
            return False
    
    def update_exercise(self, exercise_id: int, updated_exercise: Dict[str, Any]) -> bool:
        """به‌روزرسانی تمرین"""
        try:
            for i, exercise in enumerate(self.exercises):
                if exercise.get('id') == exercise_id:
                    updated_exercise['id'] = exercise_id
                    if self._validate_exercise(updated_exercise):
                        self.exercises[i] = updated_exercise
                        return self.save_exercises()
            return False
        except Exception as e:
            print(f"خطا در به‌روزرسانی تمرین: {e}")
            return False
    
    def delete_exercise(self, exercise_id: int) -> bool:
        """حذف تمرین"""
        try:
            self.exercises = [ex for ex in self.exercises if ex.get('id') != exercise_id]
            return self.save_exercises()
        except Exception as e:
            print(f"خطا در حذف تمرین: {e}")
            return False
    
    def _validate_exercise(self, exercise: Dict[str, Any]) -> bool:
        """اعتبارسنجی تمرین"""
        required_fields = ['title', 'difficulty', 'description', 'code', 'questions']
        
        for field in required_fields:
            if field not in exercise:
                print(f"فیلد {field} موجود نیست")
                return False
        
        # بررسی سطح دشواری
        valid_difficulties = ['مبتدی', 'متوسط', 'پیشرفته']
        if exercise['difficulty'] not in valid_difficulties:
            print(f"سطح دشواری نامعتبر: {exercise['difficulty']}")
            return False
        
        # بررسی سوالات
        if not isinstance(exercise['questions'], list) or len(exercise['questions']) == 0:
            print("سوالات نامعتبر")
            return False
        
        for question in exercise['questions']:
            if not self._validate_question(question):
                return False
        
        return True
    
    def _validate_question(self, question: Dict[str, Any]) -> bool:
        """اعتبارسنجی سوال"""
        required_fields = ['question', 'type', 'answer']
        
        for field in required_fields:
            if field not in question:
                print(f"فیلد {field} در سوال موجود نیست")
                return False
        
        valid_types = ['multiple_choice', 'text', 'code']
        if question['type'] not in valid_types:
            print(f"نوع سوال نامعتبر: {question['type']}")
            return False
        
        # بررسی گزینه‌ها برای سوال چند گزینه‌ای
        if question['type'] == 'multiple_choice':
            if 'options' not in question or not isinstance(question['options'], list):
                print("گزینه‌های سوال چند گزینه‌ای نامعتبر")
                return False
            
            if question['answer'] not in question['options']:
                print("پاسخ صحیح در گزینه‌ها موجود نیست")
                return False
        
        return True
    
    def get_exercise_statistics(self) -> Dict[str, Any]:
        """دریافت آمار تمرین‌ها"""
        total = len(self.exercises)
        
        difficulty_counts = {}
        for exercise in self.exercises:
            difficulty = exercise.get('difficulty', 'نامشخص')
            difficulty_counts[difficulty] = difficulty_counts.get(difficulty, 0) + 1
        
        concept_counts = {}
        for exercise in self.exercises:
            concepts = exercise.get('concepts', [])
            for concept in concepts:
                concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        return {
            'total': total,
            'by_difficulty': difficulty_counts,
            'by_concept': concept_counts
        }
    
    def search_exercises(self, query: str) -> List[Dict[str, Any]]:
        """جستجو در تمرین‌ها"""
        results = []
        query_lower = query.lower()
        
        for exercise in self.exercises:
            # جستجو در عنوان
            if query_lower in exercise.get('title', '').lower():
                results.append(exercise)
                continue
            
            # جستجو در توضیحات
            if query_lower in exercise.get('description', '').lower():
                results.append(exercise)
                continue
            
            # جستجو در کد
            if query_lower in exercise.get('code', '').lower():
                results.append(exercise)
                continue
            
            # جستجو در مفاهیم
            concepts = exercise.get('concepts', [])
            if any(query_lower in concept.lower() for concept in concepts):
                results.append(exercise)
                continue
        
        return results
    
    def get_next_exercise(self) -> Optional[Dict[str, Any]]:
        """دریافت تمرین بعدی"""
        if not self.exercises:
            return None
        
        if self.current_exercise_index >= len(self.exercises):
            self.current_exercise_index = 0
        
        exercise = self.exercises[self.current_exercise_index]
        self.current_exercise_index += 1
        
        return exercise
    
    def get_previous_exercise(self) -> Optional[Dict[str, Any]]:
        """دریافت تمرین قبلی"""
        if not self.exercises:
            return None
        
        if self.current_exercise_index <= 0:
            self.current_exercise_index = len(self.exercises) - 1
        else:
            self.current_exercise_index -= 1
        
        return self.exercises[self.current_exercise_index]
    
    def reset_exercise_index(self):
        """بازنشانی شاخص تمرین"""
        self.current_exercise_index = 0
    
    def shuffle_exercises(self):
        """مخلوط کردن تمرین‌ها"""
        random.shuffle(self.exercises)
    
    def sort_exercises(self, key: str = 'difficulty', reverse: bool = False):
        """مرتب‌سازی تمرین‌ها"""
        difficulty_order = {'مبتدی': 1, 'متوسط': 2, 'پیشرفته': 3}
        
        if key == 'difficulty':
            self.exercises.sort(key=lambda x: difficulty_order.get(x.get('difficulty', 'متوسط'), 2), reverse=reverse)
        elif key == 'title':
            self.exercises.sort(key=lambda x: x.get('title', ''), reverse=reverse)
        elif key == 'id':
            self.exercises.sort(key=lambda x: x.get('id', 0), reverse=reverse)
    
    def export_exercises(self, filename: str) -> bool:
        """خروجی گرفتن از تمرین‌ها"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.exercises, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"خطا در خروجی گرفتن: {e}")
            return False
    
    def import_exercises(self, filename: str) -> bool:
        """وارد کردن تمرین‌ها از فایل"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                imported_exercises = json.load(f)
            
            # اعتبارسنجی تمرین‌های وارد شده
            valid_exercises = []
            for exercise in imported_exercises:
                if self._validate_exercise(exercise):
                    valid_exercises.append(exercise)
            
            if valid_exercises:
                self.exercises.extend(valid_exercises)
                return self.save_exercises()
            
            return False
        except Exception as e:
            print(f"خطا در وارد کردن: {e}")
            return False
    
    def backup_exercises(self, backup_filename: str = None) -> bool:
        """پشتیبان‌گیری از تمرین‌ها"""
        if not backup_filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"exercises_backup_{timestamp}.json"
        
        return self.export_exercises(backup_filename)
    
    def get_difficulty_progression(self) -> List[str]:
        """دریافت ترتیب پیشرفت سطح دشواری"""
        return ['مبتدی', 'متوسط', 'پیشرفته']
    
    def get_recommended_next_exercise(self, user_progress: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """پیشنهاد تمرین بعدی براساس پیشرفت کاربر"""
        completed_exercises = user_progress.get('completed_exercises', [])
        
        if not completed_exercises:
            # اگر هیچ تمرینی حل نشده، تمرین مبتدی پیشنهاد بده
            beginner_exercises = self.get_exercises_by_difficulty('مبتدی')
            return beginner_exercises[0] if beginner_exercises else None
        
        # محاسبه میانگین امتیاز
        avg_score = sum(ex.get('score', 0) for ex in completed_exercises) / len(completed_exercises)
        
        # تعیین سطح پیشنهادی
        completed_titles = [ex.get('title', '') for ex in completed_exercises]
        
        if avg_score >= 80:
            # اگر امتیاز خوب است، سطح بالاتر پیشنهاد بده
            for difficulty in ['متوسط', 'پیشرفته']:
                available = [ex for ex in self.get_exercises_by_difficulty(difficulty) 
                           if ex.get('title') not in completed_titles]
                if available:
                    return available[0]
        
        # در غیر این صورت، تمرین‌های همان سطح پیشنهاد بده
        last_difficulty = completed_exercises[-1].get('difficulty', 'مبتدی')
        available = [ex for ex in self.get_exercises_by_difficulty(last_difficulty) 
                    if ex.get('title') not in completed_titles]
        
        return available[0] if available else None
