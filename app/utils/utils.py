def date_formatter(items: dict) -> dict:
    for item in items:
        item['datetime'] = item['datetime'].strftime("%d.%m.%Y %H:%M")

    return items