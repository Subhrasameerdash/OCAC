from django.db import models
from django.utils import timezone


class Transaction(models.Model):
    """A single financial transaction — the core domain object."""

    class TransactionType(models.TextChoices):
        INCOME = 'income', 'Income'
        EXPENSE = 'expense', 'Expense'

    class Category(models.TextChoices):
        FOOD = 'Food', 'Food'
        TRANSPORT = 'Transport', 'Transport'
        ENTERTAINMENT = 'Entertainment', 'Entertainment'
        BILLS = 'Bills', 'Bills'
        SHOPPING = 'Shopping', 'Shopping'
        HEALTH = 'Health', 'Health'
        EDUCATION = 'Education', 'Education'
        SALARY = 'Salary', 'Salary'
        FREELANCE = 'Freelance', 'Freelance'
        INVESTMENT = 'Investment', 'Investment'
        OTHER = 'Other', 'Other'

    class PaymentMode(models.TextChoices):
        CASH = 'Cash', 'Cash'
        UPI = 'UPI', 'UPI'
        CARD = 'Card', 'Card'
        NET_BANKING = 'Net Banking', 'Net Banking'

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.now)
    description = models.CharField(max_length=255)
    type = models.CharField(
        max_length=7,
        choices=TransactionType.choices,
        default=TransactionType.EXPENSE,
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )
    payment_mode = models.CharField(
        max_length=20,
        choices=PaymentMode.choices,
        default=PaymentMode.CASH,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_type_display()} — ₹{self.amount} ({self.description})"

    # ── Aggregation helpers (fat model) ──────────────────────────

    @classmethod
    def total_income(cls, qs=None):
        qs = qs if qs is not None else cls.objects.all()
        result = qs.filter(type='income').aggregate(total=models.Sum('amount'))
        return result['total'] or 0

    @classmethod
    def total_expense(cls, qs=None):
        qs = qs if qs is not None else cls.objects.all()
        result = qs.filter(type='expense').aggregate(total=models.Sum('amount'))
        return result['total'] or 0

    @classmethod
    def balance(cls, qs=None):
        return cls.total_income(qs) - cls.total_expense(qs)

    @classmethod
    def savings_rate(cls, qs=None):
        income = cls.total_income(qs)
        if income == 0:
            return 0
        return round(float(cls.balance(qs)) / float(income) * 100, 1)

    @classmethod
    def category_breakdown(cls, qs=None):
        """Return expense totals grouped by category."""
        qs = qs if qs is not None else cls.objects.all()
        return list(
            qs.filter(type='expense')
            .values('category')
            .annotate(total=models.Sum('amount'))
            .order_by('-total')
        )

    @classmethod
    def monthly_trend(cls, qs=None):
        """Return income & expense totals grouped by month."""
        from django.db.models.functions import TruncMonth
        qs = qs if qs is not None else cls.objects.all()
        return list(
            qs.annotate(month=TruncMonth('date'))
            .values('month', 'type')
            .annotate(total=models.Sum('amount'))
            .order_by('month')
        )
