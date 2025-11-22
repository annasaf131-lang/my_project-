def analyze_orders(orders):
    total = 0
    status_sums = {"оплачен": 0, "ожидающий": 0, "отменён": 0}
    category_sums = {"электроника": 0, "книги": 0, "одежда": 0}

    for order in orders:
        total += order.get("сумма", 0)
        status = order.get("статус")
        category = order.get("категория")

        if status in status_sums:
            status_sums[status] += order.get("сумма", 0)
        if category in category_sums:
            category_sums[category] += order.get("сумма", 0)

    return {
        "всего": total,
        **status_sums,
        **category_sums
    }

orders = [
    {"сумма": 120, "статус": "оплачен", "категория": "электроника"},
    {"сумма": 50, "статус": "ожидающий", "категория": "книги"},
    {"сумма": 200, "статус": "оплачен", "категория": "одежда"},
    {"сумма": 80, "статус": "отменён", "категория": "электроника"}
]

result = analyze_orders(orders)
print(result)

# название функции и переменных на русском языке для лучшего понимания контекста задачи
# использование словарей для аккумулирования сумм по статусам и категориям