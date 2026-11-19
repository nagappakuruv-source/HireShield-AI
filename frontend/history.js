
const API_BASE_URL = "https://hireshield-ai-j55j.onrender.com";

const loadHistoryBtn = document.getElementById("loadHistoryBtn");
const historyList = document.getElementById("historyList");

let currentHistoryPage = 1;
let totalHistoryPages = 1;

async function loadHistory(page = 1) {
    currentHistoryPage = page;
    historyList.textContent = "Loading analysis history...";

    try {
        const response = await fetch(
            `${API_BASE_URL}/history?page=${page}&limit=10`
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Unable to load history.");
        }

        historyList.replaceChildren();
        totalHistoryPages = data.total_pages || 1;

        const summary = document.createElement("p");
        summary.textContent = `${data.total_records} analyses found`;
        historyList.appendChild(summary);

        if (!data.history || data.history.length === 0) {
            historyList.appendChild(
                Object.assign(document.createElement("p"), {
                    textContent: "No analysis history found."
                })
            );

            updatePagination(page);
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
            viewBtn.type = "button";
            viewBtn.textContent = "View Full Report";

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
                            `${API_BASE_URL}/history/${item.id}`
                        );

                        const reportData = await reportResponse.json();

                        if (!reportResponse.ok) {
                            throw new Error(
                                reportData.detail || "Unable to load report."
                            );
                        }

                        const report =
                            reportData.analysis ||
                            reportData.record ||
                            reportData;

                      // 1. Overall Risk Verdict
const riskLevel = report.risk_level || item.risk_level || "Unknown";
const riskScore = report.risk_score ?? item.risk_score ?? 0;

const verdict = document.createElement("h3");

verdict.textContent =
    riskLevel === "High Risk"
        ? "HIGH RISK — Do Not Proceed"
        : riskLevel === "Medium Risk"
        ? "MEDIUM RISK — Proceed With Caution"
        : riskLevel === "Low Risk"
        ? "LOW RISK — No Major Warning Signs Detected"
        : "RISK ASSESSMENT UNAVAILABLE";

reportDetails.appendChild(verdict);

// 2. Recommendation
const recommendation = document.createElement("p");

recommendation.className = "risk-recommendation";

recommendation.textContent =
    riskLevel === "High Risk"
        ? "Do not pay money or proceed with this job until the employer and job offer are independently verified."
        : riskLevel === "Medium Risk"
        ? "Verify the company, job details, and payment requirements carefully before proceeding."
        : riskLevel === "Low Risk"
        ? "No major warning signs were detected. Still verify the employer before accepting the offer."
        : "Please review the job details carefully.";

reportDetails.appendChild(recommendation);

// 3. Risk Score
const score = document.createElement("p");
score.textContent = `Risk Score: ${riskScore}/100`;
reportDetails.appendChild(score);

// 4. ML Model Classification (Secondary Information)
const prediction = document.createElement("p");
prediction.textContent =
    `ML Model Classification: ${report.result || item.result || "Not available"}`;

reportDetails.appendChild(prediction);

// 5. Display remaining report information
Object.entries(report).forEach(([key, value]) => {
    if (
        ["message", "risk_level", "risk_score", "result", "prediction"].includes(key) ||
        value === null
    ) {
        return;
    }

    const row = document.createElement("p");

    const label = document.createElement("strong");
    label.textContent = key.replace(/_/g, " ") + ": ";

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
            deleteBtn.type = "button";
            deleteBtn.textContent = "Delete Report";

            deleteBtn.addEventListener("click", async () => {
                if (!confirm("Are you sure you want to delete this report?")) {
                    return;
                }

                try {
                    const deleteResponse = await fetch(
                        `${API_BASE_URL}/history/${item.id}`,
                        { method: "DELETE" }
                    );

                    if (!deleteResponse.ok) {
                        const errorData = await deleteResponse.json();
                        throw new Error(
                            errorData.detail || "Could not delete report."
                        );
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

        updatePagination(page);

    } catch (error) {
        historyList.textContent = `Error: ${error.message}`;
    }
}

function updatePagination(page) {
    let pagination = document.getElementById("historyPagination");

    if (!pagination) {
        pagination = document.createElement("div");
        pagination.id = "historyPagination";
        historyList.after(pagination);
    }

    pagination.replaceChildren();

    const previousBtn = document.createElement("button");
    previousBtn.textContent = "Previous";
    previousBtn.disabled = page <= 1;

    previousBtn.addEventListener("click", () => {
        loadHistory(currentHistoryPage - 1);
    });

    const pageInfo = document.createElement("span");
    pageInfo.textContent = `Page ${page} of ${totalHistoryPages}`;

    const nextBtn = document.createElement("button");
    nextBtn.textContent = "Next";
    nextBtn.disabled = page >= totalHistoryPages;

    nextBtn.addEventListener("click", () => {
        loadHistory(currentHistoryPage + 1);
    });

    pagination.append(previousBtn, pageInfo, nextBtn);
}

loadHistoryBtn.addEventListener("click", () => loadHistory(1));

// Load history automatically when the page opens.
loadHistory(1);
