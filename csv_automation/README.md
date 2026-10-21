# CSV Report Automation

Ожидаемые колонки: `date`, `category`, `amount`, `status`.

```bash
python csv_automation/report.py csv_automation/sample.csv --output report.json
```

Утилита завершится с ненулевым кодом при отсутствии обязательной колонки, пустом значении или некорректной сумме.

