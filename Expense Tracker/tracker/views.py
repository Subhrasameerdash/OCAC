"""Thin views — all business logic lives on the Transaction model."""
import json
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Transaction


# ── SPA shell ───────────────────────────────────────────────────

def index(request):
    """Serve the single-page app."""
    return render(request, 'tracker/index.html')


# ── Helpers ─────────────────────────────────────────────────────

def _filtered_qs(params):
    """Apply optional query-param filters to a Transaction queryset."""
    qs = Transaction.objects.all()
    if params.get('type'):
        qs = qs.filter(type=params['type'])
    if params.get('category'):
        qs = qs.filter(category=params['category'])
    if params.get('date_from'):
        qs = qs.filter(date__gte=params['date_from'])
    if params.get('date_to'):
        qs = qs.filter(date__lte=params['date_to'])
    if params.get('payment_mode'):
        qs = qs.filter(payment_mode=params['payment_mode'])
    return qs


def _serialize(txn):
    date_val = txn.date
    if hasattr(date_val, 'isoformat'):
        date_val = date_val.isoformat()
    created_val = txn.created_at
    if hasattr(created_val, 'isoformat'):
        created_val = created_val.isoformat()
    return {
        'id': txn.id,
        'amount': str(txn.amount),
        'date': str(date_val),
        'description': txn.description,
        'type': txn.type,
        'category': txn.category,
        'payment_mode': txn.payment_mode,
        'created_at': str(created_val),
    }


def _parse_body(request):
    """Parse JSON body and validate required fields."""
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return None, JsonResponse({'error': 'Invalid JSON'}, status=400)

    errors = []
    if not data.get('description', '').strip():
        errors.append('description is required')
    try:
        amount = Decimal(str(data.get('amount', '')))
        if amount <= 0:
            errors.append('amount must be positive')
    except (InvalidOperation, ValueError):
        errors.append('amount must be a valid number')

    if data.get('type') not in ('income', 'expense'):
        errors.append('type must be income or expense')

    if errors:
        return None, JsonResponse({'errors': errors}, status=400)

    return data, None


# ── API endpoints ───────────────────────────────────────────────

@require_http_methods(['GET'])
def transaction_list(request):
    qs = _filtered_qs(request.GET)
    return JsonResponse([_serialize(t) for t in qs], safe=False)


@csrf_exempt
@require_http_methods(['POST'])
def transaction_create(request):
    data, err = _parse_body(request)
    if err:
        return err

    txn = Transaction.objects.create(
        amount=data['amount'],
        date=data.get('date') or None,
        description=data['description'].strip(),
        type=data['type'],
        category=data.get('category', 'Other'),
        payment_mode=data.get('payment_mode', 'Cash'),
    )
    txn.refresh_from_db()
    return JsonResponse(_serialize(txn), status=201)


@csrf_exempt
@require_http_methods(['PUT'])
def transaction_update(request, pk):
    txn = get_object_or_404(Transaction, pk=pk)
    data, err = _parse_body(request)
    if err:
        return err

    txn.amount = data['amount']
    txn.date = data.get('date') or txn.date
    txn.description = data['description'].strip()
    txn.type = data['type']
    txn.category = data.get('category', txn.category)
    txn.payment_mode = data.get('payment_mode', txn.payment_mode)
    txn.save()
    txn.refresh_from_db()
    return JsonResponse(_serialize(txn))


@csrf_exempt
@require_http_methods(['DELETE'])
def transaction_delete(request, pk):
    txn = get_object_or_404(Transaction, pk=pk)
    txn.delete()
    return JsonResponse({'deleted': True})


@require_http_methods(['GET'])
def dashboard_summary(request):
    qs = _filtered_qs(request.GET)
    income = Transaction.total_income(qs)
    expense = Transaction.total_expense(qs)
    balance = income - expense
    savings = Transaction.savings_rate(qs)

    # Category breakdown (for doughnut chart)
    categories = Transaction.category_breakdown(qs)
    cat_data = [{'category': c['category'], 'total': str(c['total'])} for c in categories]

    # Monthly trend (for line chart)
    trend_raw = Transaction.monthly_trend(qs)
    trend = {}
    for row in trend_raw:
        month_key = row['month'].strftime('%Y-%m')
        if month_key not in trend:
            trend[month_key] = {'month': month_key, 'income': '0', 'expense': '0'}
        trend[month_key][row['type']] = str(row['total'])
    trend_data = list(trend.values())

    return JsonResponse({
        'total_income': str(income),
        'total_expense': str(expense),
        'balance': str(balance),
        'savings_rate': savings,
        'category_breakdown': cat_data,
        'monthly_trend': trend_data,
    })
