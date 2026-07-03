/**
 * app.js — Main controller.
 * Imports api.js and ui.js modules.
 * Orchestrates form submission, pipeline animation, and result rendering.
 */

import { checkHealth, analyzeEmail } from './api.js';
import {
    Status, Loading, StepLog, Pipeline, Results,
    initCopyButton, initCharCounter
} from './ui.js';

/* ── Category → reply node name map ─────────────────────── */
const NODE_MAP = {
    Job:       'job_reply',
    Complaint: 'complaint_reply',
    Sales:     'sales_reply',
    Personal:  'personal_reply',
};

/* ── Health check on load ────────────────────────────────── */
async function initHealthCheck() {
    Status.set('warning', 'Connecting…');
    try {
        const data = await checkHealth();
        const traced = data.langsmith_tracing ? '✓ LangSmith' : '✗ LangSmith';
        Status.set('active', `Online · ${data.model} · ${traced}`);
    } catch {
        Status.set('inactive', 'Backend offline');
    }
}

/* ── Pipeline animation sequence ─────────────────────────── */
function animatePipeline(replyNode, onComplete) {
    // Phase 1 — classify_email: running
    Pipeline.setNode('pipe-start', 'done');
    Pipeline.lightArrow(0);
    Pipeline.setNode('pipe-classify', 'running');
    StepLog.add('classify_email', 'running');

    setTimeout(() => {
        // Phase 2 — classify done, reply node: running
        Pipeline.setNode('pipe-classify', 'done');
        Pipeline.lightArrow(1);
        StepLog.add('classify_email', 'success');

        Pipeline.setReplyLabel(replyNode);
        Pipeline.setNode('pipe-reply', 'running');
        StepLog.add(replyNode, 'running');

        setTimeout(() => {
            // Phase 3 — reply done, END
            Pipeline.setNode('pipe-reply', 'done');
            Pipeline.lightArrow(2);
            StepLog.add(replyNode, 'success');

            Pipeline.setNode('pipe-end', 'done');
            StepLog.add('END', 'success');

            onComplete();
        }, 900);
    }, 800);
}

/* ── Form submit handler ─────────────────────────────────── */
async function handleSubmit(e) {
    e.preventDefault();
    const emailText = document.getElementById('email-input').value.trim();
    if (!emailText) return;

    // Reset UI state
    Loading.set(true);
    Results.hide();
    Results.resetEmpty();
    StepLog.clear();
    Pipeline.reset();

    try {
        // Call POST /analyze
        const data = await analyzeEmail(emailText);
        const replyNode = NODE_MAP[data.category] ?? 'personal_reply';

        // Animate pipeline steps, then render
        animatePipeline(replyNode, () => {
            Loading.set(false);
            Results.render(data);
        });

    } catch (err) {
        Pipeline.reset();
        StepLog.add('Error', 'error');
        Loading.set(false);
        Results.showError(err.message);
        console.error('[SmartEmail] Analyze failed:', err);
    }
}

/* ── Bootstrap ───────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
    initHealthCheck();
    initCopyButton();
    initCharCounter();
    document.getElementById('analyze-form').addEventListener('submit', handleSubmit);
});
