from fastapi import FastAPI

app = FastAPI(
    title="C216 - Sistemas Distribuídos",
    description="API de exemplo para a Prática 1",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "disciplina": "C216 - Sistemas Distribuídos",
        "pratica": "Prática 1",
        "mensagem": "Ambiente configurado com sucesso com Poetry e FastAPI!"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
