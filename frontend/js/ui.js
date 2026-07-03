/**
 * ui.js — All DOM manipulation and rendering.
 * Exports: UI namespace with methods for status, loading,
 *          pipeline, step log, and result rendering.
 */

/* ── Category metadata ───────────────────────────────────── */
const CATEGORY_META = {
    Job:       { icon: '💼', cls: 'cat-job'       },
    Complaint: { icon: '⚠️',  cls: 'cat-complaint' },
    Sales:     { icon: '📊', cls: 'cat-sales'     },
    Personal:  { icon: '👤', cls: 'cat-personal'  },
};

/** Safely get element by ID */
const el = id => document.getElementById(id);

/* ══════════════════════════════════════════════════════════
   STATUS BAR
   ══════════════════════════════════════════════════════════ */
export const Status = {
    set(state, text) {
        const dot  = el('status-dot');
        const span = el('status-text');
        if (!dot || !span) return;
        dot.className    = `status-dot ${state}`;   // 'active' | 'warning' | 'inactive'
        span.textContent = text;
    }
};

/* ══════════════════════════════════════════════════════════
   LOADING STATE
   ══════════════════════════════════════════════════════════ */
export const Loading = {
    /** @param {boolean} on */
    set(on) {
        const btn    = el('btn-analyze');
        const label  = el('btn-label');
        const loader = el('btn-loader');
        if (!btn) return;
        btn.disabled             = on;
        label.style.display      = on ? 'none' : 'inline';
        loader.classList.toggle('visible', on);
    }
};

/* ══════════════════════════════════════════════════════════
   STEP LOG
   ══════════════════════════════════════════════════════════ */
export const StepLog = {
    clear() {
        el('steps-log').innerHTML =
            '<li class="step-empty">No execution yet — submit an email to begin.</li>';
    },

    /** @param {string} name @param {'running'|'success'|'error'} status */
    add(name, status) {
        const log = el('steps-log');
        const empty = log.querySelector('.step-empty');
        if (empty) empty.remove();

        let li = document.getElementById(`step-${name}`);
        if (!li) {
            li = document.createElement('li');
            li.id = `step-${name}`;
            log.appendChild(li);
        }
        li.innerHTML = `
            <span>⟶ <strong>${name}</strong></span>
            <span class="step-status ${status}">${status}</span>
        `;
    }
};

/* ══════════════════════════════════════════════════════════
   PIPELINE VISUALIZER
   ══════════════════════════════════════════════════════════ */
export const Pipeline = {
    _arrows: null,

    _getArrows() {
        if (!this._arrows) this._arrows = Array.from(document.querySelectorAll('.pipe-arrow'));
        return this._arrows;
    },

    reset() {
        ['pipe-start', 'pipe-classify', 'pipe-reply', 'pipe-end'].forEach(id => {
            const n = el(id);
            if (n) { n.classList.remove('idle', 'running', 'done'); n.classList.add('idle'); }
        });
        this._getArrows().forEach(a => a.classList.remove('lit'));
    },

    /** @param {string} nodeId @param {'idle'|'running'|'done'} state */
    setNode(nodeId, state) {
        const n = el(nodeId);
        if (!n) return;
        n.classList.remove('idle', 'running', 'done');
        n.classList.add(state);
    },

    /** Light arrow connector by index (0-based) */
    lightArrow(index) {
        const arr = this._getArrows();
        if (arr[index]) arr[index].classList.add('lit');
    },

    /** Update the dynamic reply-node label */
    setReplyLabel(name) {
        const span = el('pipe-reply-label');
        if (span) span.textContent = name;
    }
};

/* ══════════════════════════════════════════════════════════
   RESULTS PANEL
   ══════════════════════════════════════════════════════════ */
export const Results = {
    show() {
        el('result-area').style.display    = 'block';
        el('result-divider').style.display = 'block';
        el('empty-state').style.display    = 'none';
    },

    hide() {
        el('result-area').style.display    = 'none';
        el('result-divider').style.display = 'none';
        el('empty-state').style.display    = 'flex';
    },

    /**
     * Render category, confidence, and reply to the DOM.
     * @param {{ category: string, confidence: number, reply: string }} data
     */
    render({ category, confidence, reply }) {
        const meta = CATEGORY_META[category] ?? { icon: '📧', cls: 'cat-personal' };

        // Category badge
        const badge = el('category-badge');
        badge.className          = `category-badge ${meta.cls}`;
        el('badge-icon').textContent = meta.icon;
        el('badge-text').textContent = category;

        // Confidence bar (animate after paint)
        const pct = Math.round(confidence * 100);
        requestAnimationFrame(() => {
            el('conf-bar').style.width = `${pct}%`;
        });
        el('conf-value').textContent = `${pct}%`;

        // Reply text
        el('reply-box').textContent = reply;

        this.show();
    },

    /** Show an error inside the result panel instead of results */
    showError(message) {
        el('result-area').style.display    = 'none';
        el('result-divider').style.display = 'none';
        const empty = el('empty-state');
        empty.style.display = 'flex';
        empty.innerHTML = `
            <div class="empty-icon">❌</div>
            <p style="color:var(--rose);font-size:0.9rem">${message}</p>
        `;
    },

    resetEmpty() {
        const empty = el('empty-state');
        empty.style.display = 'flex';
        empty.innerHTML = `
            <div class="empty-icon">🤖</div>
            <p>Results will appear here after analysis.</p>
        `;
    }
};

/* ══════════════════════════════════════════════════════════
   COPY BUTTON
   ══════════════════════════════════════════════════════════ */
export function initCopyButton() {
    el('btn-copy')?.addEventListener('click', () => {
        const text = el('reply-box')?.textContent ?? '';
        navigator.clipboard.writeText(text).then(() => {
            const btn = el('btn-copy');
            btn.classList.add('copied');
            el('copy-label').textContent = '✓ Copied!';
            setTimeout(() => {
                btn.classList.remove('copied');
                el('copy-label').textContent = 'Copy Reply';
            }, 2200);
        });
    });
}

/* ══════════════════════════════════════════════════════════
   CHARACTER COUNTER
   ══════════════════════════════════════════════════════════ */
export function initCharCounter() {
    el('email-input')?.addEventListener('input', function () {
        const n = this.value.length;
        el('char-count').textContent = `${n.toLocaleString()} character${n !== 1 ? 's' : ''}`;
    });
}
