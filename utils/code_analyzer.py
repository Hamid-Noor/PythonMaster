import ast
import re
from typing import Dict, List, Any

class CodeAnalyzer:
    """کلاس تحلیل کد پایتون"""
    
    def __init__(self):
        self.variables = set()
        self.functions = []
        self.classes = []
        self.imports = []
        self.loops = []
        self.conditions = []
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """تحلیل کامل کد پایتون"""
        try:
            tree = ast.parse(code)
            self._reset_analysis()
            
            # تحلیل درخت AST
            self._analyze_ast(tree)
            
            return {
                'variables': list(self.variables),
                'functions': self.functions,
                'classes': self.classes,
                'imports': self.imports,
                'loops': self.loops,
                'conditions': self.conditions,
                'complexity': self._calculate_complexity()
            }
        except SyntaxError as e:
            return {'error': f'خطای نحوی: {e}'}
        except Exception as e:
            return {'error': f'خطا در تحلیل: {e}'}
    
    def _reset_analysis(self):
        """بازنشانی متغیرهای تحلیل"""
        self.variables = set()
        self.functions = []
        self.classes = []
        self.imports = []
        self.loops = []
        self.conditions = []
    
    def _analyze_ast(self, node, parent_type=None):
        """تحلیل بازگشتی درخت AST"""
        for child in ast.walk(node):
            # تحلیل متغیرها
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Store):
                self.variables.add(child.id)
            
            # تحلیل توابع
            elif isinstance(child, ast.FunctionDef):
                func_info = {
                    'name': child.name,
                    'line': child.lineno,
                    'args': [arg.arg for arg in child.args.args],
                    'docstring': ast.get_docstring(child),
                    'decorators': [self._get_decorator_name(d) for d in child.decorator_list]
                }
                self.functions.append(func_info)
            
            # تحلیل کلاس‌ها
            elif isinstance(child, ast.ClassDef):
                methods = [
                    node.name for node in child.body 
                    if isinstance(node, ast.FunctionDef)
                ]
                class_info = {
                    'name': child.name,
                    'line': child.lineno,
                    'methods': methods,
                    'bases': [self._get_base_name(base) for base in child.bases],
                    'docstring': ast.get_docstring(child)
                }
                self.classes.append(class_info)
            
            # تحلیل imports
            elif isinstance(child, ast.Import):
                for alias in child.names:
                    self.imports.append(alias.name)
            
            elif isinstance(child, ast.ImportFrom):
                module = child.module or ''
                for alias in child.names:
                    self.imports.append(f"{module}.{alias.name}")
            
            # تحلیل حلقه‌ها
            elif isinstance(child, ast.For):
                loop_info = {
                    'type': 'for',
                    'line': child.lineno,
                    'target': self._get_node_name(child.target),
                    'iter': self._get_node_name(child.iter)
                }
                self.loops.append(loop_info)
            
            elif isinstance(child, ast.While):
                loop_info = {
                    'type': 'while',
                    'line': child.lineno,
                    'condition': self._get_node_name(child.test)
                }
                self.loops.append(loop_info)
            
            # تحلیل شرطی‌ها
            elif isinstance(child, ast.If):
                condition_info = {
                    'type': 'if',
                    'line': child.lineno,
                    'condition': self._get_node_name(child.test)
                }
                self.conditions.append(condition_info)
    
    def _get_decorator_name(self, decorator):
        """استخراج نام decorator"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{decorator.value.id}.{decorator.attr}"
        return str(decorator)
    
    def _get_base_name(self, base):
        """استخراج نام کلاس پایه"""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return f"{base.value.id}.{base.attr}"
        return str(base)
    
    def _get_node_name(self, node):
        """استخراج نام از نود AST"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{node.value.id}.{node.attr}"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Call):
            return self._get_node_name(node.func)
        return str(type(node).__name__)
    
    def _calculate_complexity(self):
        """محاسبه پیچیدگی کد"""
        complexity = 1  # پیچیدگی پایه
        complexity += len(self.loops) * 2  # حلقه‌ها
        complexity += len(self.conditions)  # شرطی‌ها
        complexity += len(self.functions)  # توابع
        return complexity
    
    def generate_explanations(self, code: str) -> List[Dict[str, str]]:
        """تولید توضیحات خودکار برای کد"""
        explanations = []
        
        try:
            tree = ast.parse(code)
            
            # توضیح کلی
            explanations.append({
                'title': 'توضیح کلی کد',
                'content': self._generate_general_explanation(code, tree)
            })
            
            # توضیح متغیرها
            if self.variables:
                explanations.append({
                    'title': 'متغیرها و داده‌ها',
                    'content': self._generate_variables_explanation()
                })
            
            # توضیح توابع
            if self.functions:
                explanations.append({
                    'title': 'توابع و عملکردها',
                    'content': self._generate_functions_explanation()
                })
            
            # توضیح ساختار کنترل
            if self.loops or self.conditions:
                explanations.append({
                    'title': 'ساختار کنترل جریان',
                    'content': self._generate_control_flow_explanation()
                })
            
        except Exception as e:
            explanations.append({
                'title': 'خطا در تولید توضیحات',
                'content': f'خطا: {e}'
            })
        
        return explanations
    
    def _generate_general_explanation(self, code: str, tree) -> str:
        """تولید توضیح کلی کد"""
        lines = len(code.splitlines())
        nodes = len(list(ast.walk(tree)))
        
        explanation = f"""
        این کد شامل {lines} خط کد است و {nodes} عنصر مختلف دارد.
        
        **ساختار کلی:**
        - تعداد متغیرها: {len(self.variables)}
        - تعداد توابع: {len(self.functions)}
        - تعداد کلاس‌ها: {len(self.classes)}
        - تعداد حلقه‌ها: {len(self.loops)}
        - تعداد شرطی‌ها: {len(self.conditions)}
        
        **پیچیدگی کد:** {self._calculate_complexity()}
        """
        
        return explanation
    
    def _generate_variables_explanation(self) -> str:
        """تولید توضیح متغیرها"""
        explanation = "**متغیرهای استفاده شده در کد:**\n\n"
        
        for var in sorted(self.variables):
            explanation += f"- `{var}`: متغیری که برای ذخیره داده استفاده می‌شود\n"
        
        explanation += "\n**نکات مهم:**\n"
        explanation += "- متغیرها باید نام‌های معنادار داشته باشند\n"
        explanation += "- نوع داده متغیرها در پایتون خودکار تشخیص داده می‌شود\n"
        
        return explanation
    
    def _generate_functions_explanation(self) -> str:
        """تولید توضیح توابع"""
        explanation = "**توابع موجود در کد:**\n\n"
        
        for func in self.functions:
            explanation += f"### تابع `{func['name']}`:\n"
            explanation += f"- خط {func['line']}\n"
            
            if func['args']:
                explanation += f"- پارامترها: {', '.join(func['args'])}\n"
            else:
                explanation += "- بدون پارامتر\n"
            
            if func['docstring']:
                explanation += f"- توضیحات: {func['docstring']}\n"
            
            explanation += "\n"
        
        return explanation
    
    def _generate_control_flow_explanation(self) -> str:
        """تولید توضیح ساختار کنترل"""
        explanation = "**ساختار کنترل جریان:**\n\n"
        
        if self.loops:
            explanation += "**حلقه‌ها:**\n"
            for loop in self.loops:
                if loop['type'] == 'for':
                    explanation += f"- حلقه for در خط {loop['line']}: تکرار روی {loop['iter']}\n"
                elif loop['type'] == 'while':
                    explanation += f"- حلقه while در خط {loop['line']}: تا زمانی که {loop['condition']} صادق باشد\n"
            explanation += "\n"
        
        if self.conditions:
            explanation += "**شرطی‌ها:**\n"
            for condition in self.conditions:
                explanation += f"- شرط if در خط {condition['line']}: بررسی {condition['condition']}\n"
            explanation += "\n"
        
        return explanation
    
    def generate_questions(self, code: str) -> List[Dict[str, str]]:
        """تولید سوالات خودکار برای کد"""
        questions = []
        
        # سوال در مورد متغیرها
        if self.variables:
            var_list = list(self.variables)
            questions.append({
                'question': f"متغیر `{var_list[0]}` چه کاری انجام می‌دهد؟",
                'answer': f"متغیر `{var_list[0]}` برای ذخیره داده استفاده می‌شود",
                'hint': "متغیرها مقادیر را در حافظه نگهداری می‌کنند"
            })
        
        # سوال در مورد توابع
        if self.functions:
            func = self.functions[0]
            questions.append({
                'question': f"تابع `{func['name']}` چه کاری انجام می‌دهد؟",
                'answer': f"تابع `{func['name']}` یک عملکرد خاص را انجام می‌دهد",
                'hint': "توابع کد را سازماندهی می‌کنند و قابل استفاده مجدد هستند"
            })
        
        # سوال در مورد حلقه‌ها
        if self.loops:
            loop = self.loops[0]
            questions.append({
                'question': f"حلقه {loop['type']} چگونه کار می‌کند؟",
                'answer': f"حلقه {loop['type']} کد را تکرار می‌کند",
                'hint': "حلقه‌ها برای تکرار عملیات استفاده می‌شوند"
            })
        
        # سوال کلی
        questions.append({
            'question': "خروجی این کد چیست؟",
            'answer': "کد را اجرا کنید تا خروجی را ببینید",
            'hint': "کد را مرحله به مرحله دنبال کنید"
        })
        
        return questions
