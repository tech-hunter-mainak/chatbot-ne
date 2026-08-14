import ast
import re
from typing import Optional


class MathService:
    """A very small, safe evaluator for simple arithmetic expressions.

    Supports: +, -, *, /, %, //, ** (power), parentheses and unary +/-.
    Does not allow names, attribute access, function calls, or other Python nodes.
    """

    _OP_MAP = {
        ast.Add: lambda a, b: a + b,
        ast.Sub: lambda a, b: a - b,
        ast.Mult: lambda a, b: a * b,
        ast.Div: lambda a, b: a / b,
        ast.Pow: lambda a, b: a ** b,
        ast.Mod: lambda a, b: a % b,
        ast.FloorDiv: lambda a, b: a // b,
    }

    def try_evaluate(self, text: str) -> Optional[str]:
        # First try to find an explicit math-like expression containing digits/operators
        matches = re.findall(r"[0-9\.\s\+\-\*/%\(\)\^]+", text)
        if matches:
            expr = max(matches, key=len).strip()
            if expr:
                # only treat this as a direct expression if it contains an operator or parentheses
                if re.search(r"[\+\-\*/%\^()]", expr):
                    expr = expr.replace("^", "**")
                    try:
                        value = self._safe_eval(expr)
                    except Exception:
                        value = None
                else:
                    value = None
                if value is not None:
                    if isinstance(value, float) and value.is_integer():
                        return str(int(value))
                    return str(value)

        # Fallback: simple natural-language parsing for patterns like
        # "add two with four", "add 3 with 5", "what is 3 plus 5" etc.
        text_low = text.lower()

        op = None
        if any(k in text_low for k in ("add", "plus", "sum", "total")):
            op = "add"
        elif any(k in text_low for k in ("subtract", "minus", "less")):
            op = "sub"
        elif any(k in text_low for k in ("multiply", "times", "x")):
            op = "mul"
        elif any(k in text_low for k in ("divide", "over", "by")):
            op = "div"

        # extract numeric tokens (digits) and simple number words
        nums: list[float] = []
        for m in re.finditer(r"\d+(?:\.\d+)?", text_low):
            try:
                nums.append(float(m.group(0)))
            except Exception:
                pass

        # small word->number mapping
        WORDS = {
            "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
            "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
            "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18,
            "nineteen": 19, "twenty": 20, "thirty": 30, "forty": 40,
            "fifty": 50, "hundred": 100
        }

        for w, v in WORDS.items():
            if w in text_low:
                # simple approach: append once per occurrence count
                count = text_low.count(w)
                nums.extend([float(v)] * count)

        if op and len(nums) >= 2:
            a, b = nums[0], nums[1]
            try:
                if op == "add":
                    res = a + b
                elif op == "sub":
                    res = a - b
                elif op == "mul":
                    res = a * b
                elif op == "div":
                    res = a / b
                else:
                    return None
            except Exception:
                return None

            if isinstance(res, float) and res.is_integer():
                return str(int(res))
            return str(res)

        return None

    def _safe_eval(self, expr: str):
        node = ast.parse(expr, mode="eval")
        return self._eval(node.body)

    def _eval(self, node):
        if isinstance(node, ast.BinOp):
            left = self._eval(node.left)
            right = self._eval(node.right)
            op_type = type(node.op)
            if op_type in self._OP_MAP:
                return self._OP_MAP[op_type](left, right)
            raise ValueError("unsupported operator")

        if isinstance(node, ast.UnaryOp):
            operand = self._eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            if isinstance(node.op, ast.USub):
                return -operand
            raise ValueError("unsupported unary operator")

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("unsupported constant type")

        if isinstance(node, ast.Num):
            return node.n

        raise ValueError("unsupported expression")


math_service = MathService()
