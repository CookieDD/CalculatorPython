from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import ast
import operator as _op
import uvicorn


class CalcRequest(BaseModel):
	expr: str | None = None
	op: str | None = None
	a: float | None = None
	b: float | None = None


app = FastAPI(title="Calculator API")
# serve static assets under /static so API routes are not shadowed
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index():
	return FileResponse("static/index.html")


def _safe_eval(expr: str):
	node = ast.parse(expr, mode="eval")

	allowed_binops = {
		ast.Add: _op.add,
		ast.Sub: _op.sub,
		ast.Mult: _op.mul,
		ast.Div: _op.truediv,
		ast.Pow: _op.pow,
		ast.Mod: _op.mod,
	}

	allowed_unary = {ast.UAdd: lambda x: x, ast.USub: _op.neg}

	def _eval(n):
		if isinstance(n, ast.Expression):
			return _eval(n.body)
		if isinstance(n, ast.Constant):
			return n.value
		if isinstance(n, ast.Num):
			return n.n
		if isinstance(n, ast.BinOp):
			left = _eval(n.left)
			right = _eval(n.right)
			fn = allowed_binops.get(type(n.op))
			if fn is None:
				raise ValueError("Operator not allowed")
			return fn(left, right)
		if isinstance(n, ast.UnaryOp):
			fn = allowed_unary.get(type(n.op))
			if fn is None:
				raise ValueError("Unary operator not allowed")
			return fn(_eval(n.operand))
		raise ValueError("Unsupported expression")

	return _eval(node)


@app.post("/api/calc")
async def calc(req: CalcRequest):
	try:
		if req.expr:
			result = _safe_eval(req.expr)
		elif req.op and req.a is not None and req.b is not None:
			ops = {
				"add": _op.add,
				"sub": _op.sub,
				"mul": _op.mul,
				"div": _op.truediv,
				"pow": _op.pow,
				"mod": _op.mod,
			}
			fn = ops.get(req.op)
			if not fn:
				raise HTTPException(status_code=400, detail="Unknown op")
			result = fn(req.a, req.b)
		else:
			raise HTTPException(status_code=400, detail="Invalid request payload")

		return {"result": result}
	except Exception as e:
		raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
	uvicorn.run("Calculator:app", host="0.0.0.0", port=8000, reload=False)