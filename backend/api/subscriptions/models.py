from django.conf import settings
from django.db import models
from django.utils import timezone
import calendar
from datetime import date


def last_day_of_month(d: date) -> date:
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    return date(d.year, d.month, days_in_month)


def next_month_last_day(d: date) -> date:
    # avança para o 1º dia do próximo mês e volta um dia
    if d.month == 12:
        first_next = date(d.year + 1, 1, 1)
    else:
        first_next = date(d.year, d.month + 1, 1)
    return last_day_of_month(first_next)


class Subscription(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("past_due", "Past due"),
        ("canceled", "Canceled"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    # Vencimento vigente (sempre último dia do mês)
    current_period_end = models.DateField(blank=True, null=True)
    amount_cents = models.IntegerField(default=1000)  # R$10,00
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Um registro por usuário (simples). Se quiser histórico, remova esta constraint.
        constraints = [
            models.UniqueConstraint(fields=["user"], name="unique_user_subscription"),
        ]

    def __str__(self):
        return f"{self.user} - {self.status} - {self.current_period_end}"

    @property
    def days_remaining(self) -> int | None:
        if not self.current_period_end:
            return None
        today = timezone.now().date()
        return (self.current_period_end - today).days

    @property
    def computed_status(self) -> str:
        if self.status == "canceled":
            return "canceled"
        if self.days_remaining is None:
            return "past_due"
        return "active" if self.days_remaining >= 0 else "past_due"

    def renew_to_next_month(self):
        """Avança o período para o último dia do próximo mês."""
        base = self.current_period_end or timezone.now().date()
        self.current_period_end = next_month_last_day(base)
        self.save(update_fields=["current_period_end", "updated_at"])

    def save(self, *args, **kwargs):
        # Define o vencimento automaticamente ao salvar pela primeira vez
        if not self.current_period_end:
            today = timezone.now().date()
            self.current_period_end = last_day_of_month(today)
        super().save(*args, **kwargs)
