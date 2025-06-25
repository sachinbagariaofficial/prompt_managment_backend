from fastapi import FastAPI
from models.prompt_generate import prompt_gen
from models.schemas import PromptFineTune
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation failed",
            "errors": jsonable_encoder(exc.errors()),
        },
    )


@app.post("/")
async def gen_ai(payload: PromptFineTune):
    try:

        response = await prompt_gen(payload)
        print("response", payload)
        return {
            "success": True,
            "message": "Request processed successfully",
            "data": response,
        }
    except Exception as e:
        return {"success": False, "message": "Something went wrong", "error": str(e)}
