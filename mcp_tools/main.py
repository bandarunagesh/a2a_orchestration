from fastapi import FastAPI, UploadFile, File
import pandas as pd
import psycopg2
import os
import subprocess
import tempfile

app = FastAPI()

pg_conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST", "localhost"),
    database=os.getenv("POSTGRES_DB", "unify_plus"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "password")
)

@app.post("/sql_sandbox")
async def sql_sandbox(query: str, schema: dict):
    # Use schema to validate, but for now, execute
    cursor = pg_conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return {"results": results}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()

@app.post("/excel_reader")
async def excel_reader(file: UploadFile = File(...)):
    df = pd.read_excel(file.file)
    return df.to_dict()

@app.post("/excel_merger")
async def excel_merger(files: list[UploadFile] = File(...)):
    dfs = [pd.read_excel(f.file) for f in files]
    merged = pd.concat(dfs)
    return merged.to_dict()

@app.post("/python_sandbox")
async def python_sandbox(code: str):
    # Execute code safely? For demo, use exec, but dangerous
    try:
        exec(code)
        return {"status": "executed"}
    except Exception as e:
        return {"error": str(e)}

@app.post("/meltano")
async def meltano(command: str):
    # Run meltano command
    result = subprocess.run(["meltano", command], capture_output=True, text=True)
    return {"output": result.stdout, "error": result.stderr}

@app.post("/file_converter")
async def file_converter(to_format: str = "json", file: UploadFile = File(...)):
    # Simple conversion, e.g., csv to json
    if to_format == "json":
        df = pd.read_csv(file.file)
        return df.to_dict()
    return {"error": "Unsupported format"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)