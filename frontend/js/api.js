/**
 * api.js — All fetch API calls to FastAPI backend.
 * Exports: checkHealth(), analyzeEmail(emailText)
 */

const API_BASE = window.location.origin;

/**
 * GET /health — backend health check
 * @returns {Promise<{
 *   status: string,
 *   service: string,
 *   model: string,
 *   classifier: string,
 *   langsmith_tracing: boolean,
 *   langsmith_project: string
 * }>}
 */
export async function checkHealth() {
    const res = await fetch(`${API_BASE}/health`);

    if (!res.ok) {
        throw new Error(`Health check failed: HTTP ${res.status}`);
    }

    return res.json();
}

/**
 * POST /analyze — run LangGraph email workflow
 * @param {string} emailText
 * @returns {Promise<{
 *   category: string,
 *   confidence: number,
 *   reply: string
 * }>}
 */
export async function analyzeEmail(emailText) {
    const res = await fetch(`${API_BASE}/analyze`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: emailText,
        }),
    });

    if (!res.ok) {
        const body = await res.json().catch(() => ({}));

        throw new Error(
            body.detail ?? `Server error: HTTP ${res.status}`
        );
    }

    return res.json();
}