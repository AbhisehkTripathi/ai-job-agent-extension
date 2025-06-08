from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .agents.resume_matcher import ResumeMatcher
from .services.job_applier import JobApplier
import os
from pathlib import Path

app = FastAPI(title="AI Job Agent API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
resume_matcher = ResumeMatcher()
job_applier = JobApplier()

@app.post("/match-resume")
async def match_resume(job_url: str, resume: UploadFile = File(...)):
    try:
        # Save the uploaded resume temporarily
        resume_path = Path("data/AbhishekTripathi-SDE.pdf")
        # print(resume_path)
        with open(resume_path, "wb") as buffer:
            buffer.write(await resume.read())
        
        # Process the job matching
        result = resume_matcher.match(job_url, str(resume_path))
        
        # Clean up
        os.remove(resume_path)
        
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/apply-job")
async def apply_job(job_url: str, contact_info: dict):
    try:
        result = job_applier.apply(job_url, contact_info)
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)