import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine, text
from typing import Dict, List, Any, Optional
from datetime import datetime

class DatabaseManager:
    """مدیریت پایگاه داده برای پلتفرم آموزش معکوس"""
    
    def __init__(self):
        self.database_url = os.getenv('DATABASE_URL')
        self.engine = create_engine(self.database_url)
        self.init_database()
    
    def init_database(self):
        """ایجاد جداول پایگاه داده"""
        with self.engine.connect() as conn:
            # جدول کاربران
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    preferences JSONB DEFAULT '{}'::jsonb
                )
            """))
            
            # جدول تمرین‌ها
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS exercises (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    difficulty VARCHAR(20) NOT NULL,
                    description TEXT,
                    code TEXT NOT NULL,
                    concepts JSONB DEFAULT '[]'::jsonb,
                    hints JSONB DEFAULT '[]'::jsonb,
                    questions JSONB DEFAULT '[]'::jsonb,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # جدول پیشرفت کاربران
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS user_progress (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    exercise_id INTEGER REFERENCES exercises(id) ON DELETE CASCADE,
                    completed BOOLEAN DEFAULT FALSE,
                    score FLOAT DEFAULT 0.0,
                    attempts INTEGER DEFAULT 0,
                    completed_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, exercise_id)
                )
            """))
            
            # جدول تحلیل کد
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS code_analysis (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    code TEXT NOT NULL,
                    analysis_result JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # جدول آمار
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS statistics (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    total_exercises_completed INTEGER DEFAULT 0,
                    average_score FLOAT DEFAULT 0.0,
                    time_spent INTEGER DEFAULT 0,
                    streak INTEGER DEFAULT 0,
                    achievements JSONB DEFAULT '[]'::jsonb,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            # جدول جلسات
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    session_data JSONB DEFAULT '{}'::jsonb,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """))
            
            conn.commit()
    
    def get_or_create_user(self, username: str = "default_user", email: str = None) -> int:
        """دریافت یا ایجاد کاربر"""
        with self.engine.connect() as conn:
            # بررسی وجود کاربر
            result = conn.execute(text("""
                SELECT id FROM users WHERE username = :username
            """), {"username": username}).fetchone()
            
            if result:
                return result[0]
            
            # ایجاد کاربر جدید
            result = conn.execute(text("""
                INSERT INTO users (username, email) 
                VALUES (:username, :email) 
                RETURNING id
            """), {"username": username, "email": email}).fetchone()
            
            conn.commit()
            return result[0]
    
    def save_user_progress(self, user_id: int, exercise_id: int, completed: bool, score: float, attempts: int = 1):
        """ذخیره پیشرفت کاربر"""
        with self.engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO user_progress (user_id, exercise_id, completed, score, attempts, completed_at)
                VALUES (:user_id, :exercise_id, :completed, :score, :attempts, :completed_at)
                ON CONFLICT (user_id, exercise_id) 
                DO UPDATE SET 
                    completed = :completed,
                    score = GREATEST(user_progress.score, :score),
                    attempts = user_progress.attempts + 1,
                    completed_at = CASE WHEN :completed THEN :completed_at ELSE user_progress.completed_at END
            """), {
                "user_id": user_id,
                "exercise_id": exercise_id,
                "completed": completed,
                "score": score,
                "attempts": attempts,
                "completed_at": datetime.now() if completed else None
            })
            conn.commit()
    
    def get_user_progress(self, user_id: int) -> List[Dict]:
        """دریافت پیشرفت کاربر"""
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT up.*, e.title, e.difficulty
                FROM user_progress up
                JOIN exercises e ON up.exercise_id = e.id
                WHERE up.user_id = :user_id
                ORDER BY up.completed_at DESC
            """), {"user_id": user_id}).fetchall()
            
            return [dict(row._mapping) for row in result]
    
    def save_code_analysis(self, user_id: int, code: str, analysis_result: dict):
        """ذخیره تحلیل کد"""
        with self.engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO code_analysis (user_id, code, analysis_result)
                VALUES (:user_id, :code, :analysis_result)
            """), {
                "user_id": user_id,
                "code": code,
                "analysis_result": json.dumps(analysis_result, ensure_ascii=False)
            })
            conn.commit()
    
    def get_exercises(self, difficulty: str = None) -> List[Dict]:
        """دریافت تمرین‌ها"""
        with self.engine.connect() as conn:
            if difficulty:
                result = conn.execute(text("""
                    SELECT * FROM exercises 
                    WHERE difficulty = :difficulty
                    ORDER BY id
                """), {"difficulty": difficulty}).fetchall()
            else:
                result = conn.execute(text("""
                    SELECT * FROM exercises 
                    ORDER BY id
                """)).fetchall()
            
            exercises = []
            for row in result:
                exercise = dict(row._mapping)
                # تبدیل JSONB به Python objects
                exercise['concepts'] = json.loads(exercise['concepts']) if exercise['concepts'] else []
                exercise['hints'] = json.loads(exercise['hints']) if exercise['hints'] else []
                exercise['questions'] = json.loads(exercise['questions']) if exercise['questions'] else []
                exercises.append(exercise)
            
            return exercises
    
    def add_exercise(self, title: str, difficulty: str, description: str, code: str, 
                    concepts: List[str], hints: List[str], questions: List[Dict]):
        """اضافه کردن تمرین جدید"""
        with self.engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO exercises (title, difficulty, description, code, concepts, hints, questions)
                VALUES (:title, :difficulty, :description, :code, :concepts, :hints, :questions)
            """), {
                "title": title,
                "difficulty": difficulty,
                "description": description,
                "code": code,
                "concepts": json.dumps(concepts, ensure_ascii=False),
                "hints": json.dumps(hints, ensure_ascii=False),
                "questions": json.dumps(questions, ensure_ascii=False)
            })
            conn.commit()
    
    def update_user_statistics(self, user_id: int):
        """به‌روزرسانی آمار کاربر"""
        with self.engine.connect() as conn:
            # محاسبه آمار
            stats = conn.execute(text("""
                SELECT 
                    COUNT(*) as total_completed,
                    AVG(score) as avg_score,
                    MAX(completed_at) as last_completed
                FROM user_progress
                WHERE user_id = :user_id AND completed = TRUE
            """), {"user_id": user_id}).fetchone()
            
            total_completed = stats[0] or 0
            avg_score = float(stats[1]) if stats[1] else 0.0
            
            # محاسبه streak
            streak = self._calculate_streak(user_id)
            
            # به‌روزرسانی جدول آمار
            conn.execute(text("""
                INSERT INTO statistics (user_id, total_exercises_completed, average_score, streak)
                VALUES (:user_id, :total, :avg, :streak)
                ON CONFLICT (user_id) 
                DO UPDATE SET 
                    total_exercises_completed = EXCLUDED.total_exercises_completed,
                    average_score = EXCLUDED.average_score,
                    streak = EXCLUDED.streak,
                    updated_at = CURRENT_TIMESTAMP
            """), {
                "user_id": user_id,
                "total": total_completed,
                "avg": avg_score,
                "streak": streak
            })
            conn.commit()
    
    def _calculate_streak(self, user_id: int) -> int:
        """محاسبه streak کاربر"""
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT DATE(completed_at) as completion_date
                FROM user_progress
                WHERE user_id = :user_id AND completed = TRUE
                ORDER BY completed_at DESC
                LIMIT 30
            """), {"user_id": user_id}).fetchall()
            
            if not result:
                return 0
            
            streak = 0
            current_date = datetime.now().date()
            
            for row in result:
                completion_date = row[0]
                if completion_date == current_date:
                    streak += 1
                    current_date = current_date.replace(day=current_date.day - 1)
                else:
                    break
            
            return streak
    
    def get_user_statistics(self, user_id: int) -> Dict:
        """دریافت آمار کاربر"""
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT * FROM statistics WHERE user_id = :user_id
            """), {"user_id": user_id}).fetchone()
            
            if result:
                stats = dict(result._mapping)
                stats['achievements'] = json.loads(stats['achievements']) if stats['achievements'] else []
                return stats
            
            return {
                'total_exercises_completed': 0,
                'average_score': 0.0,
                'streak': 0,
                'achievements': []
            }
    
    def save_session_data(self, user_id: int, session_data: dict):
        """ذخیره داده‌های جلسه"""
        with self.engine.connect() as conn:
            conn.execute(text("""
                INSERT INTO sessions (user_id, session_data)
                VALUES (:user_id, :session_data)
                ON CONFLICT (user_id) 
                DO UPDATE SET 
                    session_data = :session_data,
                    updated_at = CURRENT_TIMESTAMP
            """), {
                "user_id": user_id,
                "session_data": json.dumps(session_data, ensure_ascii=False)
            })
            conn.commit()
    
    def get_session_data(self, user_id: int) -> dict:
        """دریافت داده‌های جلسه"""
        with self.engine.connect() as conn:
            result = conn.execute(text("""
                SELECT session_data FROM sessions WHERE user_id = :user_id
            """), {"user_id": user_id}).fetchone()
            
            if result:
                return json.loads(result[0])
            
            return {}
    
    def populate_default_exercises(self):
        """پر کردن تمرین‌های پیش‌فرض"""
        # بررسی وجود تمرین‌ها
        with self.engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM exercises")).fetchone()[0]
            
            if count > 0:
                return  # تمرین‌ها از قبل وجود دارند
        
        # خواندن تمرین‌ها از فایل JSON
        try:
            with open('data/exercises.json', 'r', encoding='utf-8') as f:
                exercises = json.load(f)
            
            for exercise in exercises:
                self.add_exercise(
                    title=exercise['title'],
                    difficulty=exercise['difficulty'],
                    description=exercise['description'],
                    code=exercise['code'],
                    concepts=exercise.get('concepts', []),
                    hints=exercise.get('hints', []),
                    questions=exercise.get('questions', [])
                )
        except FileNotFoundError:
            print("فایل exercises.json یافت نشد")