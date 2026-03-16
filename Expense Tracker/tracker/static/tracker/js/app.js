/* ═══════════════════════════════════════════════════════════════
   Flux - Smart Finance  ·  Async SPA Logic
   ═══════════════════════════════════════════════════════════════ */

const API = {
    list:      '/api/transactions/',
    create:    '/api/transactions/create/',
    update:    (id) => `/api/transactions/${id}/update/`,
    delete:    (id) => `/api/transactions/${id}/delete/`,
    dashboard: '/api/dashboard/',
};

// ── State ──────────────────────────────────────────────────────
let transactions = [];
let categoryChart = null;
let trendChart = null;
let editingId = null;

// ── Chart colors ───────────────────────────────────────────────
const CHART_COLORS = [
    '#7c6aff', '#f87171', '#34d399', '#fbbf24', '#60a5fa',
    '#f472b6', '#a78bfa', '#fb923c', '#2dd4bf', '#e879f9',
    '#38bdf8',
];

// ── Bootstrap ──────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    setDefaultDate();
    attachFilterListeners();
    refresh();
});

async function refresh() {
    await Promise.all([fetchTransactions(), fetchDashboard()]);
}

// ── FETCH helpers ──────────────────────────────────────────────
function getFilterParams() {
    const params = new URLSearchParams();
    const type     = document.getElementById('filter-type').value;
    const category = document.getElementById('filter-category').value;
    const payment  = document.getElementById('filter-payment').value;
    const from     = document.getElementById('filter-date-from').value;
    const to       = document.getElementById('filter-date-to').value;

    if (type)     params.set('type', type);
    if (category) params.set('category', category);
    if (payment)  params.set('payment_mode', payment);
    if (from)     params.set('date_from', from);
    if (to)       params.set('date_to', to);
    return params.toString();
}

async function fetchTransactions() {
    try {
        const qs = getFilterParams();
        const url = qs ? `${API.list}?${qs}` : API.list;
        const res = await fetch(url);
        transactions = await res.json();
        renderTable();
    } catch (e) {
        showToast('Failed to load transactions', 'error');
    }
}

async function fetchDashboard() {
    try {
        const qs = getFilterParams();
        const url = qs ? `${API.dashboard}?${qs}` : API.dashboard;
        const res = await fetch(url);
        const data = await res.json();
        renderDashboard(data);
        renderCharts(data);
    } catch (e) {
        showToast('Failed to load dashboard', 'error');
    }
}

// ── RENDER: Dashboard cards ────────────────────────────────────
function renderDashboard(data) {
    animateValue('total-income',  formatCurrency(data.total_income));
    animateValue('total-expense', formatCurrency(data.total_expense));
    animateValue('balance',       formatCurrency(data.balance));
    animateValue('savings-rate',  `${data.savings_rate}%`);
}

function animateValue(id, newValue) {
    const el = document.getElementById(id);
    if (el.textContent !== newValue) {
        el.style.transform = 'scale(1.08)';
        el.textContent = newValue;
        setTimeout(() => { el.style.transform = 'scale(1)'; }, 250);
    }
}

function formatCurrency(val) {
    const num = parseFloat(val) || 0;
    return '₹' + num.toLocaleString('en-IN', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
}

// ── RENDER: Charts ─────────────────────────────────────────────
function renderCharts(data) {
    renderCategoryChart(data.category_breakdown);
    renderTrendChart(data.monthly_trend);
}

function renderCategoryChart(categories) {
    const canvas = document.getElementById('chart-category');
    const emptyMsg = document.getElementById('chart-category-empty');

    if (!categories || categories.length === 0) {
        if (categoryChart) { categoryChart.destroy(); categoryChart = null; }
        canvas.classList.add('hidden');
        emptyMsg.classList.remove('hidden');
        return;
    }
    canvas.classList.remove('hidden');
    emptyMsg.classList.add('hidden');

    const labels = categories.map(c => c.category);
    const values = categories.map(c => parseFloat(c.total));

    if (categoryChart) categoryChart.destroy();
    categoryChart = new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels,
            datasets: [{
                data: values,
                backgroundColor: CHART_COLORS.slice(0, labels.length),
                borderWidth: 0,
                hoverOffset: 8,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '68%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: '#9a9abb',
                        padding: 16,
                        usePointStyle: true,
                        pointStyleWidth: 10,
                        font: { family: "'Inter', sans-serif", size: 11 },
                    },
                },
                tooltip: {
                    backgroundColor: '#1a1a3e',
                    titleColor: '#eeeef6',
                    bodyColor: '#9a9abb',
                    borderColor: 'rgba(255,255,255,0.06)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 10,
                    callbacks: {
                        label: (ctx) => ` ₹${ctx.parsed.toLocaleString('en-IN')}`,
                    },
                },
            },
        },
    });
}

function renderTrendChart(trend) {
    const canvas = document.getElementById('chart-trend');
    const emptyMsg = document.getElementById('chart-trend-empty');

    if (!trend || trend.length === 0) {
        if (trendChart) { trendChart.destroy(); trendChart = null; }
        canvas.classList.add('hidden');
        emptyMsg.classList.remove('hidden');
        return;
    }
    canvas.classList.remove('hidden');
    emptyMsg.classList.add('hidden');

    const labels  = trend.map(t => t.month);
    const incomes  = trend.map(t => parseFloat(t.income));
    const expenses = trend.map(t => parseFloat(t.expense));

    if (trendChart) trendChart.destroy();
    trendChart = new Chart(canvas, {
        type: 'line',
        data: {
            labels,
            datasets: [
                {
                    label: 'Income',
                    data: incomes,
                    borderColor: '#34d399',
                    backgroundColor: 'rgba(52, 211, 153, 0.08)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 2.5,
                    pointRadius: 4,
                    pointBackgroundColor: '#34d399',
                    pointHoverRadius: 6,
                },
                {
                    label: 'Expenses',
                    data: expenses,
                    borderColor: '#f87171',
                    backgroundColor: 'rgba(248, 113, 113, 0.08)',
                    fill: true,
                    tension: 0.4,
                    borderWidth: 2.5,
                    pointRadius: 4,
                    pointBackgroundColor: '#f87171',
                    pointHoverRadius: 6,
                },
            ],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.04)' },
                    ticks: { color: '#5a5a7a', font: { family: "'Inter', sans-serif", size: 11 } },
                },
                y: {
                    grid: { color: 'rgba(255,255,255,0.04)' },
                    ticks: {
                        color: '#5a5a7a',
                        font: { family: "'Inter', sans-serif", size: 11 },
                        callback: (v) => '₹' + v.toLocaleString('en-IN'),
                    },
                },
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#9a9abb',
                        padding: 16,
                        usePointStyle: true,
                        font: { family: "'Inter', sans-serif", size: 11 },
                    },
                },
                tooltip: {
                    backgroundColor: '#1a1a3e',
                    titleColor: '#eeeef6',
                    bodyColor: '#9a9abb',
                    borderColor: 'rgba(255,255,255,0.06)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    padding: 10,
                    callbacks: {
                        label: (ctx) => ` ${ctx.dataset.label}: ₹${ctx.parsed.y.toLocaleString('en-IN')}`,
                    },
                },
            },
        },
    });
}

// ── RENDER: Transaction table ──────────────────────────────────
function renderTable() {
    const tbody = document.getElementById('txn-tbody');

    if (transactions.length === 0) {
        tbody.innerHTML = `<tr class="empty-state"><td colspan="7">No transactions yet — add one to get started!</td></tr>`;
        return;
    }

    tbody.innerHTML = transactions.map(t => `
        <tr data-id="${t.id}">
            <td>${formatDate(t.date)}</td>
            <td>${escapeHtml(t.description)}</td>
            <td><span class="pill">${t.category}</span></td>
            <td>${t.payment_mode}</td>
            <td><span class="badge badge-${t.type}">${t.type}</span></td>
            <td class="text-right amount-${t.type}">₹${parseFloat(t.amount).toLocaleString('en-IN')}</td>
            <td class="text-center">
                <div class="action-btns">
                    <button class="btn-icon btn-edit" onclick="editTransaction(${t.id})" aria-label="Edit">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                    </button>
                    <button class="btn-icon btn-delete" onclick="deleteTransaction(${t.id})" aria-label="Delete">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/></svg>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

function formatDate(iso) {
    const d = new Date(iso + 'T00:00:00');
    return d.toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' });
}

function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// ── MODAL ──────────────────────────────────────────────────────
function openModal(txn = null) {
    const overlay = document.getElementById('modal-overlay');
    const form = document.getElementById('txn-form');
    const title = document.getElementById('modal-title');
    const submitBtn = document.getElementById('btn-submit');

    form.reset();
    setDefaultDate();

    if (txn) {
        editingId = txn.id;
        title.textContent = 'Edit Transaction';
        submitBtn.textContent = 'Update';
        document.getElementById('txn-id').value = txn.id;
        document.getElementById('txn-amount').value = txn.amount;
        document.getElementById('txn-description').value = txn.description;
        document.getElementById('txn-category').value = txn.category;
        document.getElementById('txn-payment').value = txn.payment_mode;
        document.getElementById('txn-date').value = txn.date;
        setType(txn.type);
    } else {
        editingId = null;
        title.textContent = 'Add Transaction';
        submitBtn.textContent = 'Add Transaction';
        setType('expense');
    }

    overlay.classList.remove('hidden');
    setTimeout(() => document.getElementById('txn-amount').focus(), 100);
}

function closeModal(e) {
    if (e && e.target !== e.currentTarget) return;
    document.getElementById('modal-overlay').classList.add('hidden');
    editingId = null;
}

function setType(type) {
    const btns = document.querySelectorAll('.toggle-btn');
    btns.forEach(b => b.classList.toggle('active', b.dataset.value === type));
}

function getSelectedType() {
    const active = document.querySelector('.toggle-btn.active');
    return active ? active.dataset.value : 'expense';
}

function setDefaultDate() {
    const dateInput = document.getElementById('txn-date');
    if (!dateInput.value) {
        dateInput.value = new Date().toISOString().split('T')[0];
    }
}

// ── FORM SUBMIT ────────────────────────────────────────────────
async function handleFormSubmit(e) {
    e.preventDefault();

    const payload = {
        amount:       document.getElementById('txn-amount').value,
        description:  document.getElementById('txn-description').value,
        type:         getSelectedType(),
        category:     document.getElementById('txn-category').value,
        payment_mode: document.getElementById('txn-payment').value,
        date:         document.getElementById('txn-date').value,
    };

    try {
        let res;
        if (editingId) {
            res = await fetch(API.update(editingId), {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
        } else {
            res = await fetch(API.create, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
        }

        if (!res.ok) {
            const err = await res.json();
            showToast(err.errors ? err.errors.join(', ') : 'Something went wrong', 'error');
            return;
        }

        closeModal();
        showToast(editingId ? 'Transaction updated!' : 'Transaction added!', 'success');
        await refresh();
    } catch (e) {
        showToast('Network error', 'error');
    }
}

// ── EDIT / DELETE ──────────────────────────────────────────────
function editTransaction(id) {
    const txn = transactions.find(t => t.id === id);
    if (txn) openModal(txn);
}

async function deleteTransaction(id) {
    if (!confirm('Delete this transaction?')) return;

    try {
        const res = await fetch(API.delete(id), { method: 'DELETE' });
        if (res.ok) {
            showToast('Transaction deleted', 'success');
            await refresh();
        }
    } catch (e) {
        showToast('Failed to delete', 'error');
    }
}

// ── FILTERS ────────────────────────────────────────────────────
function attachFilterListeners() {
    ['filter-type', 'filter-category', 'filter-payment', 'filter-date-from', 'filter-date-to'].forEach(id => {
        document.getElementById(id).addEventListener('change', () => refresh());
    });
}

function clearFilters() {
    ['filter-type', 'filter-category', 'filter-payment', 'filter-date-from', 'filter-date-to'].forEach(id => {
        document.getElementById(id).value = '';
    });
    refresh();
}

// ── TOAST ──────────────────────────────────────────────────────
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    setTimeout(() => { toast.className = 'toast hidden'; }, 3000);
}
