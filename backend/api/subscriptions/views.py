from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Subscription


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def subscription_status(request):
    sub = Subscription.objects.filter(user=request.user).first()
    if not sub:
        return Response({"status": "none", "days_remaining": None, "next_due_date": None})

    return Response({
        "status": sub.computed_status,
        "days_remaining": sub.days_remaining,
        "next_due_date": sub.current_period_end,
        "amount_cents": sub.amount_cents,
    })
