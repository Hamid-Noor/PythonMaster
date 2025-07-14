import ast
import graphviz
from typing import Optional, Dict, List

class FlowchartGenerator:
    """کلاس تولید نمودار جریان از کد پایتون"""
    
    def __init__(self):
        self.graph = None
        self.node_counter = 0
        self.nodes = []
        self.edges = []
    
    def generate_flowchart(self, code: str) -> Optional[str]:
        """تولید نمودار جریان از کد"""
        try:
            tree = ast.parse(code)
            self._reset_graph()
            
            # تولید نمودار
            self._process_ast(tree)
            
            if self.graph:
                return self.graph.source
            return None
            
        except Exception as e:
            return None
    
    def _reset_graph(self):
        """بازنشانی گراف"""
        self.graph = graphviz.Digraph(comment='Python Code Flowchart')
        self.graph.attr(rankdir='TB')
        self.graph.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
        self.node_counter = 0
        self.nodes = []
        self.edges = []
    
    def _get_next_node_id(self) -> str:
        """دریافت شناسه نود بعدی"""
        self.node_counter += 1
        return f"node_{self.node_counter}"
    
    def _process_ast(self, tree):
        """پردازش درخت AST"""
        # شروع
        start_node = self._get_next_node_id()
        self.graph.node(start_node, 'شروع', shape='ellipse', fillcolor='lightgreen')
        
        # پردازش بدنه اصلی
        last_node = start_node
        for stmt in tree.body:
            last_node = self._process_statement(stmt, last_node)
        
        # پایان
        end_node = self._get_next_node_id()
        self.graph.node(end_node, 'پایان', shape='ellipse', fillcolor='lightcoral')
        if last_node:
            self.graph.edge(last_node, end_node)
    
    def _process_statement(self, stmt, prev_node: str) -> str:
        """پردازش یک دستور"""
        if isinstance(stmt, ast.Assign):
            return self._process_assignment(stmt, prev_node)
        elif isinstance(stmt, ast.If):
            return self._process_if(stmt, prev_node)
        elif isinstance(stmt, ast.For):
            return self._process_for(stmt, prev_node)
        elif isinstance(stmt, ast.While):
            return self._process_while(stmt, prev_node)
        elif isinstance(stmt, ast.FunctionDef):
            return self._process_function(stmt, prev_node)
        elif isinstance(stmt, ast.Return):
            return self._process_return(stmt, prev_node)
        elif isinstance(stmt, ast.Expr):
            return self._process_expression(stmt, prev_node)
        else:
            # دستور عمومی
            return self._process_generic_statement(stmt, prev_node)
    
    def _process_assignment(self, stmt, prev_node: str) -> str:
        """پردازش انتساب"""
        node_id = self._get_next_node_id()
        
        # استخراج نام متغیر
        if isinstance(stmt.targets[0], ast.Name):
            var_name = stmt.targets[0].id
            value = self._get_value_representation(stmt.value)
            label = f"{var_name} = {value}"
        else:
            label = "انتساب متغیر"
        
        self.graph.node(node_id, label)
        if prev_node:
            self.graph.edge(prev_node, node_id)
        
        return node_id
    
    def _process_if(self, stmt, prev_node: str) -> str:
        """پردازش دستور if"""
        # نود تصمیم
        decision_node = self._get_next_node_id()
        condition = self._get_condition_representation(stmt.test)
        self.graph.node(decision_node, f"اگر {condition}؟", shape='diamond', fillcolor='lightyellow')
        
        if prev_node:
            self.graph.edge(prev_node, decision_node)
        
        # پردازش بدنه if
        if_body_node = decision_node
        for s in stmt.body:
            if_body_node = self._process_statement(s, if_body_node)
        
        # پردازش else (اگر وجود دارد)
        else_body_node = decision_node
        if stmt.orelse:
            for s in stmt.orelse:
                else_body_node = self._process_statement(s, else_body_node)
        
        # نود ادغام
        merge_node = self._get_next_node_id()
        self.graph.node(merge_node, "ادغام", shape='circle', fillcolor='lightgray')
        
        # اتصال نودها
        self.graph.edge(decision_node, if_body_node if if_body_node != decision_node else merge_node, label='بله')
        if if_body_node != decision_node:
            self.graph.edge(if_body_node, merge_node)
        
        if stmt.orelse:
            self.graph.edge(decision_node, else_body_node if else_body_node != decision_node else merge_node, label='خیر')
            if else_body_node != decision_node:
                self.graph.edge(else_body_node, merge_node)
        else:
            self.graph.edge(decision_node, merge_node, label='خیر')
        
        return merge_node
    
    def _process_for(self, stmt, prev_node: str) -> str:
        """پردازش حلقه for"""
        # نود شروع حلقه
        loop_start = self._get_next_node_id()
        target = self._get_node_name(stmt.target)
        iter_obj = self._get_node_name(stmt.iter)
        self.graph.node(loop_start, f"برای {target} در {iter_obj}", shape='hexagon', fillcolor='lightcyan')
        
        if prev_node:
            self.graph.edge(prev_node, loop_start)
        
        # پردازش بدنه حلقه
        body_node = loop_start
        for s in stmt.body:
            body_node = self._process_statement(s, body_node)
        
        # برگشت به شروع حلقه
        if body_node != loop_start:
            self.graph.edge(body_node, loop_start, label='تکرار')
        
        # نود پایان حلقه
        loop_end = self._get_next_node_id()
        self.graph.node(loop_end, "پایان حلقه", shape='circle', fillcolor='lightgray')
        self.graph.edge(loop_start, loop_end, label='پایان')
        
        return loop_end
    
    def _process_while(self, stmt, prev_node: str) -> str:
        """پردازش حلقه while"""
        # نود شرط
        condition_node = self._get_next_node_id()
        condition = self._get_condition_representation(stmt.test)
        self.graph.node(condition_node, f"تا زمانی که {condition}", shape='diamond', fillcolor='lightyellow')
        
        if prev_node:
            self.graph.edge(prev_node, condition_node)
        
        # پردازش بدنه حلقه
        body_node = condition_node
        for s in stmt.body:
            body_node = self._process_statement(s, body_node)
        
        # برگشت به شرط
        if body_node != condition_node:
            self.graph.edge(body_node, condition_node, label='تکرار')
        
        # نود پایان
        end_node = self._get_next_node_id()
        self.graph.node(end_node, "پایان حلقه", shape='circle', fillcolor='lightgray')
        self.graph.edge(condition_node, end_node, label='خیر')
        
        return end_node
    
    def _process_function(self, stmt, prev_node: str) -> str:
        """پردازش تعریف تابع"""
        node_id = self._get_next_node_id()
        args = [arg.arg for arg in stmt.args.args]
        args_str = ', '.join(args) if args else 'بدون پارامتر'
        label = f"تابع {stmt.name}({args_str})"
        
        self.graph.node(node_id, label, shape='box', fillcolor='lightgreen')
        if prev_node:
            self.graph.edge(prev_node, node_id)
        
        return node_id
    
    def _process_return(self, stmt, prev_node: str) -> str:
        """پردازش دستور return"""
        node_id = self._get_next_node_id()
        if stmt.value:
            value = self._get_value_representation(stmt.value)
            label = f"برگردان {value}"
        else:
            label = "برگردان"
        
        self.graph.node(node_id, label, shape='box', fillcolor='lightcoral')
        if prev_node:
            self.graph.edge(prev_node, node_id)
        
        return node_id
    
    def _process_expression(self, stmt, prev_node: str) -> str:
        """پردازش عبارت"""
        node_id = self._get_next_node_id()
        
        if isinstance(stmt.value, ast.Call):
            func_name = self._get_node_name(stmt.value.func)
            label = f"فراخوانی {func_name}"
        else:
            label = "عبارت"
        
        self.graph.node(node_id, label)
        if prev_node:
            self.graph.edge(prev_node, node_id)
        
        return node_id
    
    def _process_generic_statement(self, stmt, prev_node: str) -> str:
        """پردازش دستور عمومی"""
        node_id = self._get_next_node_id()
        label = f"دستور {type(stmt).__name__}"
        
        self.graph.node(node_id, label)
        if prev_node:
            self.graph.edge(prev_node, node_id)
        
        return node_id
    
    def _get_node_name(self, node):
        """استخراج نام نود"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_node_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Constant):
            return str(node.value)
        elif isinstance(node, ast.Call):
            return self._get_node_name(node.func)
        return "نامشخص"
    
    def _get_value_representation(self, value):
        """نمایش مقدار"""
        if isinstance(value, ast.Constant):
            return str(value.value)
        elif isinstance(value, ast.Name):
            return value.id
        elif isinstance(value, ast.BinOp):
            left = self._get_value_representation(value.left)
            right = self._get_value_representation(value.right)
            op = self._get_operator_symbol(value.op)
            return f"{left} {op} {right}"
        elif isinstance(value, ast.Call):
            return self._get_node_name(value.func) + "()"
        return "مقدار"
    
    def _get_condition_representation(self, condition):
        """نمایش شرط"""
        if isinstance(condition, ast.Compare):
            left = self._get_value_representation(condition.left)
            if condition.ops and condition.comparators:
                op = self._get_comparison_symbol(condition.ops[0])
                right = self._get_value_representation(condition.comparators[0])
                return f"{left} {op} {right}"
        elif isinstance(condition, ast.BoolOp):
            values = [self._get_value_representation(v) for v in condition.values]
            op = "و" if isinstance(condition.op, ast.And) else "یا"
            return f" {op} ".join(values)
        elif isinstance(condition, ast.Name):
            return condition.id
        return "شرط"
    
    def _get_operator_symbol(self, op):
        """تبدیل عملگر به نماد"""
        if isinstance(op, ast.Add):
            return "+"
        elif isinstance(op, ast.Sub):
            return "-"
        elif isinstance(op, ast.Mult):
            return "*"
        elif isinstance(op, ast.Div):
            return "/"
        elif isinstance(op, ast.Mod):
            return "%"
        return "عملگر"
    
    def _get_comparison_symbol(self, op):
        """تبدیل عملگر مقایسه به نماد"""
        if isinstance(op, ast.Eq):
            return "=="
        elif isinstance(op, ast.NotEq):
            return "!="
        elif isinstance(op, ast.Lt):
            return "<"
        elif isinstance(op, ast.LtE):
            return "<="
        elif isinstance(op, ast.Gt):
            return ">"
        elif isinstance(op, ast.GtE):
            return ">="
        return "مقایسه"
