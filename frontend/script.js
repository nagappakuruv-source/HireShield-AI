const API_URL = "http://127.0.0.1:8000/analyze";
const jobForm = document.getElementById("jobForm");
const analyzeBtn = document.getElementById("analyzeBtn");

// Create the result section dynamically
const resultSection = document.createElement("section");
resultSection.id = "analysisResult";
resultSection.hidden = true;
jobForm.insertAdjacentElement("afterend", resultSection);

function addResultText(parent, label, value) {
    const paragraph = document.createElement("p");
    const strong = document.createElement("strong");

    strong.textContent = label + ": ";
    paragraph.appendChild(strong);
    paragraph.appendChild(
        document.createTextNode(value ?? "Not available")
    );

    parent.appendChild(paragraph);
}

jobForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const jobData = {
        job_title: document.getElementById("job_title").value.trim(),
        company_name: document.getElementById("company_name").value.trim(),
        job_description: document.getElementById("job_description").value.trim(),
        company_website: document.getElementById("company_website").value.trim() || null,
        company_profile: document.getElementById("company_profile").value.trim() || null,
        requirements: document.getElementById("requirements").value.trim() || null,
        benefits: document.getElementById("benefits").value.trim() || null,
        employment_type: document.getElementById("employment_type").value.trim() || null,
        required_experience: document.getElementById("required_experience").value.trim() || null,
        required_education: document.getElementById("required_education").value.trim() || null,
        industry: document.getElementById("industry").value.trim() || null,
        function: document.getElementById("function").value.trim() || null
    };

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";
    resultSection.hidden = false;
    resultSection.replaceChildren();

    const loadingMessage = document.createElement("p");
    loadingMessage.textContent = "Analyzing the job posting. Please wait...";
    resultSection.appendChild(loadingMessage);

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jobData)
        });

       const data = await response.json();

console.log("FULL MANUAL ANALYSIS RESPONSE:", data);
        if (!response.ok) {
            throw new Error(data.detail || "Unable to analyze this job.");
        }

        resultSection.replaceChildren();

        const heading = document.createElement("h2");
        heading.textContent = "Analysis Results";
        resultSection.appendChild(heading);

       const prediction = Number(data.prediction);
const risk = data.risk_assessment || {};

const jobResult = document.createElement("h3");

const riskLevel = risk.risk_level || "Unknown";

jobResult.textContent =
    riskLevel === "High Risk"
        ? "HIGH RISK — Do Not Proceed"
        : riskLevel === "Medium Risk"
        ? "MEDIUM RISK — Proceed With Caution"
        : riskLevel === "Low Risk"
        ? "LOW RISK — No Major Warning Signs Detected"
        : "RISK ASSESSMENT UNAVAILABLE";

const recommendation = document.createElement("p");
recommendation.className = "risk-recommendation";

recommendation.textContent =
    riskLevel === "High Risk"
        ? "Do not pay money or proceed with this job until the employer and job offer are independently verified."
        : riskLevel === "Medium Risk"
        ? "Verify the company, job details, and payment requirements carefully before proceeding."
        : riskLevel === "Low Risk"
        ? "No major warning signs were detected. Still verify the employer before accepting the offer."
        : "We could not determine the overall risk. Please review the details carefully.";

resultSection.appendChild(jobResult);
resultSection.appendChild(recommendation);

resultSection.appendChild(jobResult);

const mlPrediction = document.createElement("p");
mlPrediction.textContent =
    `ML Model Prediction: ${data.result || (prediction === 1 ? "Fraudulent Job" : "Genuine Job")}`;

resultSection.appendChild(mlPrediction);
       addResultText(resultSection, "Risk Score", `${risk.risk_score ?? 0}/100`);
        addResultText(resultSection, "Risk Level", risk.risk_level ?? "Not available");
        addResultText(resultSection, "Analysis ID", data.analysis_id ?? "Not available");

        const reasonsHeading = document.createElement("h3");
        reasonsHeading.textContent = "Risk Indicators";
        resultSection.appendChild(reasonsHeading);

        const reasonsList = document.createElement("ul");

        if (Array.isArray(risk.reasons) && risk.reasons.length > 0) {
            risk.reasons.forEach((reason) => {
                const item = document.createElement("li");
                item.textContent = reason;
                reasonsList.appendChild(item);
            });
        } else {
            const item = document.createElement("li");
            item.textContent = "No risk indicators detected.";
            reasonsList.appendChild(item);
        }

        resultSection.appendChild(reasonsList);

        const explanationHeading = document.createElement("h3");
        explanationHeading.textContent = "AI Explanation";
        resultSection.appendChild(explanationHeading);

        const explanation = document.createElement("div");
explanation.className = "ai-explanation";

const explanationText =
    data.ai_explanation || "AI explanation is not available.";




const normalizedExplanation = String(explanationText)
      .replace(/\\(?=#{1,6}\s)/g, "")
    .replace(/\\([*_`])/g, "$1")
    .replace(/\\([.!?])/g, "$1");
    
const lines = normalizedExplanation
    .replace(/([^\n])\s+(?=#{1,6}\s)/g, "$1\n")
    .replace(/([^\n])\s+(?=\d+[.)]\s)/g, "$1\n")
    .split(/\r?\n/);

let currentList = null;
let currentListType = null;

function closeCurrentList() {
    currentList = null;
    currentListType = null;
}

lines.forEach((line) => {
    const text = line.trim();

    if (!text) {
        closeCurrentList();
        return;
    }

    const cleanText = (value) =>
        value
            .replace(/\*\*/g, "")
            .replace(/\*/g, "")
            .replace(/`/g, "")
            .trim();

    const headingMatch = text.match(/^#{1,6}\s+(.+)$/);
    const numberedMatch = text.match(/^\d+[.)]\s+(.+)$/);
    const bulletMatch = text.match(/^[-*]\s+(.+)$/);

    if (headingMatch) {
        closeCurrentList();

        const heading = document.createElement("h4");
        heading.textContent = cleanText(headingMatch[1]);
        explanation.appendChild(heading);

    } else if (numberedMatch || bulletMatch) {
        const listType = numberedMatch ? "ol" : "ul";

        if (currentListType !== listType) {
            closeCurrentList();

            currentList = document.createElement(listType);
            explanation.appendChild(currentList);
            currentListType = listType;
        }

        const item = document.createElement("li");

        item.textContent = cleanText(
            numberedMatch ? numberedMatch[1] : bulletMatch[1]
        );

        currentList.appendChild(item);

    } else {
        closeCurrentList();

        const paragraph = document.createElement("p");
        paragraph.textContent = cleanText(text);

        explanation.appendChild(paragraph);
    }
});

resultSection.appendChild(explanation);

resultSection.scrollIntoView({
    behavior: "smooth",
    block: "start"
});

} catch (error) {
    resultSection.textContent = "Error: " + error.message;

} finally {
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = "Analyze Job";
}
});


const pdfForm = document.getElementById("pdfForm");
const pdfAnalyzeBtn = document.getElementById("pdfAnalyzeBtn");

const pdfResultSection = document.createElement("section");
pdfResultSection.id = "pdfAnalysisResult";
pdfResultSection.hidden = true;
pdfForm.insertAdjacentElement("afterend", pdfResultSection);

pdfForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const pdfFile = document.getElementById("jobPdf").files[0];

    if (!pdfFile) {
        alert("Please select a PDF file.");
        return;
    }

    const formData = new FormData();

    formData.append("file", pdfFile);
    formData.append(
        "job_title",
        document.getElementById("pdf_job_title").value.trim()
    );
    formData.append(
        "company_name",
        document.getElementById("pdf_company_name").value.trim()
    );

    pdfAnalyzeBtn.disabled = true;
    pdfAnalyzeBtn.textContent = "Analyzing PDF...";

    pdfResultSection.hidden = false;
    pdfResultSection.textContent = "Extracting and analyzing your PDF...";

    try {
        const response = await fetch(
           "http://127.0.0.1:8000/analyze-pdf",
            {
                method: "POST",
                body: formData
            }
        );

       const data = await response.json();

console.log("FULL MANUAL ANALYSIS RESPONSE:", data);
console.log("RAW AI EXPLANATION:", JSON.stringify(data.ai_explanation));

        if (!response.ok) {
            throw new Error(data.detail || "PDF analysis failed.");
        }

      pdfResultSection.replaceChildren();

const risk = data.risk_assessment || {};

const container = document.createElement("div");
container.className = "pdf-result-card";

const heading = document.createElement("h2");
heading.textContent = "Security Analysis Report";

const subtitle = document.createElement("p");
subtitle.textContent = "Your job posting analysis is complete.";

const result = document.createElement("h3");

const riskLevel = risk.risk_level || "Unknown";

result.textContent =
    riskLevel === "High Risk"
        ? "HIGH RISK — Do Not Proceed"
        : riskLevel === "Medium Risk"
        ? "MEDIUM RISK — Proceed With Caution"
        : riskLevel === "Low Risk"
        ? "LOW RISK — No Major Warning Signs Detected"
        : "RISK ASSESSMENT UNAVAILABLE";

const recommendation = document.createElement("p");
recommendation.className = "risk-recommendation";

recommendation.textContent =
    riskLevel === "High Risk"
        ? "Do not pay money or proceed with this job until the employer and job offer are independently verified."
        : riskLevel === "Medium Risk"
        ? "Verify the company, job details, and payment requirements carefully before proceeding."
        : riskLevel === "Low Risk"
        ? "No major warning signs were detected. Still verify the employer before accepting the offer."
        : "We could not determine the overall risk. Please review the details carefully.";
const mlPrediction = document.createElement("p");
mlPrediction.textContent =
    `ML Model Prediction: ${data.result || "Not available"}`;
const score = document.createElement("p");
score.textContent = `Risk Score: ${risk.risk_score ?? 0}/100`;

const level = document.createElement("p");
level.textContent = `Risk Level: ${risk.risk_level ?? "Not available"}`;

const analysisId = document.createElement("p");
analysisId.textContent = `Analysis ID: ${data.analysis_id ?? "Not available"}`;

const indicatorsHeading = document.createElement("h3");
indicatorsHeading.textContent = "Risk Indicators";

const indicators = document.createElement("ul");

if (Array.isArray(risk.reasons) && risk.reasons.length > 0) {
    risk.reasons.forEach((reason) => {
        const item = document.createElement("li");
        item.textContent = reason;
        indicators.appendChild(item);
    });
} else {
    const item = document.createElement("li");
    item.textContent = "No risk indicators detected.";
    indicators.appendChild(item);
}

const verificationHeading = document.createElement("h3");
verificationHeading.textContent = "Company Verification";

const verification = document.createElement("p");
const companyData = data.company_verification;

if (companyData) {
    verification.textContent = JSON.stringify(companyData, null, 2);
} else {
    verification.textContent =
        "Company verification information was not provided.";
}

const explanationHeading = document.createElement("h3");
explanationHeading.textContent = "AI Explanation";

const explanation = document.createElement("div");
explanation.className = "ai-explanation";

const explanationText =
    data.ai_explanation || "AI explanation is not available.";

const normalizedExplanation = String(explanationText)
    .replace(/\\(?=#{1,6}\s)/g, "")
    .replace(/\\([*`_])/g, "$1")
    .replace(/\\([.!?])/g, "$1");
const lines = normalizedExplanation
    .replace(/([^\n])\s+(?=#{1,6}\s)/g, "$1\n")
    .replace(/([^\n])\s+(?=\d+\.\s)/g, "$1\n")
    .split(/\r?\n/);
let currentList = null;
let currentListType = null;

function closeCurrentList() {
    currentList = null;
    currentListType = null;
}


lines.forEach((line) => {
    const text = line.trim();

    if (!text) {
        closeCurrentList();
        return;
    }

    const cleanText = (value) =>
        value
            .replace(/\*\*/g, "")
            .replace(/\*/g, "")
            .replace(/`/g, "")
            .trim();

    const headingMatch = text.match(/^#{1,6}\s+(.+)$/);
  const boldNumberedHeadingMatch =
    text.match(/^\*\*\s*(\d+[.)]\s+.+?)\s*\*\*$/);
    const numberedMatch = text.match(/^\d+[.)]\s+(.+)$/);
    const bulletMatch = text.match(/^[-*]\s+(.+)$/);

    if (headingMatch || boldNumberedHeadingMatch) {
        closeCurrentList();

        const heading = document.createElement("h4");
        heading.textContent = cleanText(
            headingMatch ? headingMatch[1] : boldNumberedHeadingMatch[1]
        );

        explanation.appendChild(heading);

    } else if (numberedMatch || bulletMatch) {
        const listType = numberedMatch ? "ol" : "ul";

        if (currentListType !== listType) {
            closeCurrentList();

            currentList = document.createElement(listType);
            explanation.appendChild(currentList);
            currentListType = listType;
        }

        const item = document.createElement("li");

        item.textContent = cleanText(
            numberedMatch ? numberedMatch[1] : bulletMatch[1]
        );

        currentList.appendChild(item);

    } else {
        closeCurrentList();

        const paragraph = document.createElement("p");
        paragraph.textContent = cleanText(text);

        explanation.appendChild(paragraph);
    }
});


container.append(
    heading,
    subtitle,
    result,
    recommendation,
    score,
    level,
    analysisId,
    indicatorsHeading,
    indicators,
    verificationHeading,
    verification,
    explanationHeading,
    explanation
);

pdfResultSection.appendChild(container);

pdfResultSection.scrollIntoView({
    behavior: "smooth",
    block: "start"
});

    } catch (error) {
        pdfResultSection.textContent = "Error: " + error.message;

    } finally {
        pdfAnalyzeBtn.disabled = false;
        pdfAnalyzeBtn.textContent = "Analyze PDF";
    }
});

// Load Analysis History with Pagination
const loadHistoryBtn = document.getElementById("loadHistoryBtn");
const historyList = document.getElementById("historyList");

let currentHistoryPage = 1;
let totalHistoryPages = 1;

async function loadHistory(page = 1) {
    currentHistoryPage = page;
    historyList.textContent = "Loading analysis history...";

    try {
        const response = await fetch(
            `http://127.0.0.1:8000/history?page=${page}&limit=10`
        );

        const data = await response.json();
        console.log("FULL MANUAL ANALYSIS RESPONSE:", data);

        if (!response.ok) {
            throw new Error(data.detail || "Unable to load history");
        }

        historyList.innerHTML = "";
        totalHistoryPages = data.total_pages || 1;

        const summary = document.createElement("p");
        summary.textContent =
            `${data.total_records} analyses found`;
        historyList.appendChild(summary);

        if (!data.history || data.history.length === 0) {
            historyList.textContent = "No analysis history found.";
            return;
        }

        data.history.forEach((item) => {
            const card = document.createElement("div");
            card.className = "history-card";

            const title = document.createElement("h3");
            title.textContent = item.job_title || "Untitled Job";

            const company = document.createElement("p");
            company.textContent =
                `Company: ${item.company_name || "Unknown"}`;

            const risk = document.createElement("p");
            risk.textContent =
                `Risk: ${item.risk_level} (${item.risk_score}/100)`;

            const prediction = document.createElement("p");
            prediction.textContent =
                `ML Prediction: ${item.result}`;

            const date = document.createElement("p");
            date.textContent = `Analyzed: ${item.created_at}`;

            // View Full Report
            const viewBtn = document.createElement("button");
            viewBtn.textContent = "View Full Report";
            viewBtn.type = "button";

            const reportDetails = document.createElement("div");
            reportDetails.className = "full-report-details";
            reportDetails.hidden = true;

            viewBtn.addEventListener("click", async () => {
                if (!reportDetails.hidden) {
                    reportDetails.hidden = true;
                    viewBtn.textContent = "View Full Report";
                    return;
                }

                if (reportDetails.dataset.loaded !== "true") {
                    viewBtn.textContent = "Loading...";

                    try {
                        const reportResponse = await fetch(
                            `http://127.0.0.1:8000/history/${item.id}`
                        );

                        const reportData = await reportResponse.json();

                        if (!reportResponse.ok) {
                            throw new Error(
                                reportData.detail || "Unable to load report"
                            );
                        }

                        const report =
                            reportData.analysis ||
                            reportData.record ||
                            reportData;

                        Object.entries(report).forEach(([key, value]) => {
                            if (key === "message" || value === null) return;

                            const row = document.createElement("p");

                            const label = document.createElement("strong");
                            label.textContent =
                                key.replace(/_/g, " ") + ": ";

                            const content = document.createElement("span");
                            content.textContent =
                                typeof value === "object"
                                    ? JSON.stringify(value, null, 2)
                                    : String(value);

                            row.append(label, content);
                            reportDetails.appendChild(row);
                        });

                        reportDetails.dataset.loaded = "true";

                    } catch (error) {
                        reportDetails.textContent = error.message;
                    }
                }

                reportDetails.hidden = false;
                viewBtn.textContent = "Hide Full Report";
            });

            // Delete Report
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete Report";
            deleteBtn.type = "button";

            deleteBtn.addEventListener("click", async () => {
                if (!confirm("Are you sure you want to delete this report?")) {
                    return;
                }

                try {
                    const deleteResponse = await fetch(
                        `http://127.0.0.1:8000/history/${item.id}`,
                        { method: "DELETE" }
                    );

                    if (!deleteResponse.ok) {
                        throw new Error("Could not delete report");
                    }

                    await loadHistory(currentHistoryPage);

                } catch (error) {
                    alert(error.message);
                }
            });

            card.append(
                title,
                company,
                risk,
                prediction,
                date,
                viewBtn,
                reportDetails,
                deleteBtn
            );

            historyList.appendChild(card);
        });

        // Pagination controls
        let pagination = document.getElementById("historyPagination");

        if (!pagination) {
            pagination = document.createElement("div");
            pagination.id = "historyPagination";
            historyList.after(pagination);
        }

        pagination.innerHTML = "";

        const previousBtn = document.createElement("button");
        previousBtn.textContent = "Previous";
        previousBtn.disabled = page <= 1;
        previousBtn.addEventListener("click", () => {
            loadHistory(currentHistoryPage - 1);
        });

        const pageInfo = document.createElement("span");
        pageInfo.textContent =
            `Page ${page} of ${totalHistoryPages}`;

        const nextBtn = document.createElement("button");
        nextBtn.textContent = "Next";
        nextBtn.disabled = page >= totalHistoryPages;
        nextBtn.addEventListener("click", () => {
            loadHistory(currentHistoryPage + 1);
        });

        pagination.append(previousBtn, pageInfo, nextBtn);

    } catch (error) {
        historyList.textContent = `Error: ${error.message}`;
    }
}

if (loadHistoryBtn && historyList) {
    loadHistoryBtn.addEventListener("click", () => loadHistory(1));
}