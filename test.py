import json
import os
from datetime import datetime

DATA_PATH = "local_data.json"


DEFAULT_ALLOCATION = {
    "housing": 0.40,  
    "food": 0.25,      
    "transport": 0.10,
    "utilities": 0.08, 
    "savings": 0.10,   
    "misc": 0.07       
}

WARN_THRESHOLD = 0.85  

def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"incomes": [], "expenses": [], "allocation": DEFAULT_ALLOCATION}


def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_income(data, amount, note=""):
    entry = {"amount": float(amount), "note": note, "date": datetime.now().isoformat()}
    data["incomes"].append(entry)
    save_data(data)
    return entry


def allocate_budget(total, allocation):
    return {k: round(total * v, 2) for k, v in allocation.items()}


def add_expense(data, category, amount, note=""):
    entry = {"category": category, "amount": float(amount), "note": note, "date": datetime.now().isoformat()}
    data["expenses"].append(entry)
    save_data(data)
    return entry


def spent_by_category(data):
    totals = {}
    for e in data["expenses"]:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return totals


def current_budget_state(data):
    total_income = sum(i["amount"] for i in data["incomes"])
    allocation = allocate_budget(total_income, data.get("allocation", DEFAULT_ALLOCATION))
    spent = spent_by_category(data)
    state = {}
    for cat, limit in allocation.items():
        spent_amt = spent.get(cat, 0.0)
        state[cat] = {"limit": limit, "spent": spent_amt, "left": round(limit - spent_amt, 2)}
    return total_income, state


def check_warnings(state):
    warnings = []
    for cat, v in state.items():
        limit = v["limit"]
        spent = v["spent"]
        if limit == 0:
            continue
        ratio = spent / limit
        if ratio >= 1.0:
            warnings.append((cat, "перерасход (лимит исчерпан)"))
        elif ratio >= WARN_THRESHOLD:
            warnings.append((cat, f"высокий расход — использовано {int(ratio*100)}%"))
    return warnings


def suggestions_for_cat(cat, state):
    left = state[cat]["left"]
    limit = state[cat]["limit"]
    spent = state[cat]["spent"]
    tips = []
    if spent == 0:
        return ["Пока трат нет — хорошо. Держать так."]
    if cat == "food":
        tips.append("Планируйте меню на неделю и покупайте по списку.")
        tips.append("Сравнивайте цены в приложениях и используйте акции.")
    if cat == "transport":
        tips.append("По возможности ходите пешком или пользуйтесь проездными.")
        tips.append("Объединяйте поездки — меньше топлива.")
    if cat == "housing":
        tips.append("Проверьте счета: можно ли экономить на электричестве/газе.")
        tips.append("Посмотри, доступен ли государственный субсидированный тариф.")
    if cat == "savings":
        tips.append("Если резерв не растет — уменьшите misc на период и переводите по чуть-чуть.")
    if left < 0:
        tips.append("Понять где перерасход и временно урезать необязательные траты.")
    else:
        tips.append("Контролируй — осталось {:.2f}.".format(left))
    return tips


def pretty_print_state(total_income, state):
    print("\n=== Текущее состояние бюджета ===")
    print(f"Общий доход: {total_income:.2f}\n")
    for cat, v in state.items():
        print(f"- {cat:10} | лимит: {v['limit']:8.2f} | потрачено: {v['spent']:8.2f} | осталось: {v['left']:8.2f}")
    print("=================================\n")


def main():
    data = load_data()
    
    if not data["incomes"]:
        print("Добавляю демо-доход 2000 для первого прогона (можешь удалить позже).")
        add_income(data, 2000.0, "demo income")

    total_income, state = current_budget_state(data)
    pretty_print_state(total_income, state)

    warnings = check_warnings(state)
    if warnings:
        print("Внимание: предупреждения по категориям:")
        for cat, msg in warnings:
            print(f" * {cat}: {msg}")
        print()

    print("Советы по категориям:")
    for cat in state:
        tips = suggestions_for_cat(cat, state)
        print(f"\n[{cat}]")
        for t in tips[:3]:
            print("  -", t)

    print("\nКоманды: ")
    print("1) add_income <amount> [note]")
    print("2) add_expense <category> <amount> [note]")
    print("3) exit\n")

 
    while True:
        cmd = input(">>> ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        if parts[0] == "exit":
            break
        if parts[0] == "add_income" and len(parts) >= 2:
            amt = parts[1]
            note = " ".join(parts[2:]) if len(parts) > 2 else ""
            add_income(data, amt, note)
            total_income, state = current_budget_state(data)
            pretty_print_state(total_income, state)
        elif p
