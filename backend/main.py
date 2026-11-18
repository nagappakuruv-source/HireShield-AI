
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query, Path
from pydantic import BaseModel
from typing import Literal
from backend.ml_engine.load_model import load_model
from backend.verification.company_verifier import generate_company_report
from backend.risk_engine.risk_assessor import calculate_risk_score
from backend.llm_engine.llm_explainer import generate_risk_explanation
from backend.document_processing.pdf_extractor import extract_text_from_pdf_bytes
from backend.database.save_analysis import save_analysis
from backend.database.delete_analysis import delete_analysis
from backend.database.search_analysis import (
    search_analyses,
    count_search_results
)
from fastapi.middleware.cors import CORSMiddleware
from backend.database.history_service import (
    get_analysis_history,
    get_analysis_by_id,
    get_total_analysis_count
)
from backend.preprocessing.company_extractor import (
    extract_company_name,
    compare_company_names
)

app = FastAPI(
    title="HireShield AI",
    description="AI-powered Job Fraud Detection and Company Verification",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
model = load_model()


class JobRequest(BaseModel):
    job_title: str
    company_name: str
    job_description: str
    company_website: str | None = None

    company_profile: str | None = None
    requirements: str | None = None
    benefits: str | None = None
    employment_type: str | None = None
    required_experience: str | None = None
    required_education: str | None = None
    industry: str | None = None
    function: str | None = None
@app.get("/")
def home():
    return {
        "message": "Welcome to HireShield AI",
        "status": "Application is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "project": "HireShield AI"
    }



@app.get("/history")
def get_history(
   page: int = Query(default=1, ge=1),
limit: int = Query(default=10, ge=1, le=100)
):
 
    offset = (page - 1) * limit

    history = get_analysis_history(
        limit=limit,
        offset=offset
    )

    total_records = get_total_analysis_count()

    total_pages = (total_records + limit - 1) // limit

    return {
        "message": "Analysis history retrieved successfully",
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "history": history
    }




@app.get("/history/search")
def search_history(
    keyword: str | None = Query(default=None, min_length=1, max_length=100),
    risk_level: Literal["Low Risk", "Medium Risk", "High Risk"] | None = None,
   page: int = Query(default=1, ge=1),
limit: int = Query(default=10, ge=1, le=100)
):
    

    offset = (page - 1) * limit

    history = search_analyses(
        keyword=keyword,
        risk_level=risk_level,
        limit=limit,
        offset=offset
    )

    total_records = count_search_results(
        keyword=keyword,
        risk_level=risk_level
    )

    total_pages = (total_records + limit - 1) // limit

    return {
        "message": "Search completed successfully",
        "page": page,
        "limit": limit,
        "total_records": total_records,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_previous": page > 1,
        "history": history
    }


@app.get("/history/{analysis_id}")
def get_history_by_id(
    analysis_id: int = Path(..., ge=1)
):

    analysis = get_analysis_by_id(analysis_id)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis with ID {analysis_id} not found"
        )

    return {
        "message": "Analysis retrieved successfully",
        "analysis": analysis
    }
@app.delete("/history/{analysis_id}")
def delete_history_by_id(
    analysis_id: int = Path(..., ge=1)
):
    deleted = delete_analysis(analysis_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis with ID {analysis_id} not found"
        )

    return {
        "message": "Analysis deleted successfully",
        "deleted_analysis_id": analysis_id
    }


@app.post("/analyze")
def analyze_job(job: JobRequest):
    prediction_text=" ".join([
    job.job_title or "",
    job.job_description or "",
    job.company_profile or "",
    job.requirements or "",
    job.benefits or "",
    job.employment_type or "",
    job.required_experience or "",
    job.required_education or "",
    job.industry or "",
    job.function or ""
    ])
    prediction = model.predict([prediction_text])[0]

    result = "Fraudulent Job" if prediction == 1 else "Genuine Job"

    company_verification = None

    if job.company_website:
        company_verification = generate_company_report(
            job.company_name,
            job.company_website
        )

    risk_assessment = calculate_risk_score(
    int(prediction),
    company_verification or {},
    job_description=job.job_description
)
    # Save analysis to database
    analysis_id = save_analysis(
        job_title=job.job_title,
        company_name=job.company_name,
        job_description=job.job_description,
        prediction=int(prediction),
        result=result,
        risk_score=risk_assessment["risk_score"],
        risk_level=risk_assessment["risk_level"]
    )
    ai_explanation = generate_risk_explanation(
        job_title=job.job_title,
        company_name=job.company_name,
        job_description=job.job_description,
        prediction=int(prediction),
        company_verification=company_verification or {},
        risk_assessment=risk_assessment
    )

    return {
        "message": "Job analysis completed",
         "analysis_id": analysis_id,
        "job_title": job.job_title,
        "company_name": job.company_name,
        "prediction": int(prediction),
        "result": result,
        "company_verification": company_verification,
        "risk_assessment": risk_assessment,
        "ai_explanation": ai_explanation
    }


@app.post("/analyze-pdf")
async def analyze_pdf(
    file: UploadFile = File(...),
    job_title: str = Form(...),
    company_name: str = Form(...),
    company_website: str | None = Form(None),
    company_profile: str | None = Form(None),
    requirements: str | None = Form(None),
    benefits: str | None = Form(None),
    employment_type: str | None = Form(None),
    required_experience: str | None = Form(None),
    required_education: str | None = Form(None),
    industry: str | None = Form(None),
    function: str | None = Form(None)
): 

    # Check PDF filename
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file."
        )

    # Read uploaded PDF
    pdf_bytes = await file.read()

    # Check file size (10 MB maximum)
    if len(pdf_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="PDF file is too large. Maximum size is 10 MB."
        )

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty."
        )

    # Extract text from PDF
    job_description = extract_text_from_pdf_bytes(pdf_bytes)

    if not job_description:
        raise HTTPException(
            status_code=422,
            detail="Could not extract text. This PDF may be scanned or empty."
        )



    
    # Extract company name from PDF
    pdf_company_name = extract_company_name(job_description)

    # Compare user-entered company with PDF company
    company_consistency = compare_company_names(
        company_name,
        pdf_company_name
    )

    print("Company Consistency:", company_consistency)
    # ML prediction
    prediction_text= " ".join([
    job_title or "",
    job_description or "",
    company_profile or "",
    requirements or "",
    benefits or "",
    employment_type or "",
    required_experience or "",
    required_education or "",
    industry or "",
    function or ""
])
    prediction=int(model.predict([prediction_text])[0])
    result = "Fraudulent Job" if prediction == 1 else "Genuine Job"

    # Company verification
    company_verification = None

    if company_website:
        company_verification = generate_company_report(
            company_name,
            company_website
        )

      # Risk assessment
    risk_assessment = calculate_risk_score(
        prediction,
        company_verification or {},
        company_consistency,
        job_description=job_description
    )

        # Save PDF analysis to database
    analysis_id = save_analysis(
        job_title=job_title,
        company_name=company_name,
        job_description=job_description,
        prediction=prediction,
        result=result,
        risk_score=risk_assessment["risk_score"],
        risk_level=risk_assessment["risk_level"]
    )

    # Gemini explanation
    ai_explanation = generate_risk_explanation(
        job_title=job_title,
        company_name=company_name,
        job_description=job_description,
        prediction=prediction,
        company_verification=company_verification or {},
        risk_assessment=risk_assessment
    )

    return {
        "message": "PDF analysis completed",
         "analysis_id": analysis_id,
        "filename": file.filename,
        "job_title": job_title,
        "company_name": company_name,
        "extracted_text": job_description,
        "prediction": prediction,
        "result": result,
        "company_verification": company_verification,
        "risk_assessment": risk_assessment,
        "ai_explanation": ai_explanation
    }
