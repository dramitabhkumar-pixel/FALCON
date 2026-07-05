from dataclasses import dataclass, field
from datetime import datetime

from enums import OrderStatus, OrderSide


@dataclass
class Order:

    order_id: int

    symbol: str

    side: OrderSide

    quantity: int

    entry_price: float

    stop_loss: float

    target: float

    status: OrderStatus = OrderStatus.NEW

    filled_price: float | None = None

    exit_price: float | None = None

    pnl: float = 0.0

    remarks: str = ""

    created_at: datetime = field(default_factory=datetime.now)

    closed_at: datetime | None = None