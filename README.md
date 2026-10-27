# tpl-ir-report

Шаблон отчёта об инциденте: машиночитаемое ядро + человеческое повествование.

## Зачем два файла

- `report.json` — факты, которые можно проверять автоматически (таймлайн, активы, IOC).
- `report.md` — объяснение для людей: контекст, гипотезы, выводы.

Схема в CI ловит пропущенные поля и битые таймлайны до того, как отчёт уйдёт заказчику.

## Использование

```bash
cp report.example.json report.json
cp report.md my-report.md
python3 schema/validate.py report.json
```

## Поля

| Поле | Тип | Обязательно |
|---|---|---|
| `incident_id` | string | да |
| `title` | string | да |
| `severity` | low/medium/high/critical | да |
| `status` | open/contained/eradicated/recovered/closed | да |
| `detected_at` | ISO-8601 | да |
| `summary` | string | да |
| `timeline[]` | {timestamp, event} | да |
| `affected_assets[]` | string | да |
| `indicators[]` | string | да |
| `root_cause` | string | да |
| `actions[]` | {action, owner, status} | да |
