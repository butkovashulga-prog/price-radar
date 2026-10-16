# LPP Ukraine — UTM генератор

Сторінка для рекрутерів: збирає UTM-посилання на вакансії PeopleForce і скорочує їх через is.gd.

- Уся логіка в `index.html` і працює в браузері. `app.py` (Flask) лише віддає цю сторінку, API-ключів немає.
- Історія посилань зберігається в браузері користувача (localStorage, ключ `lpp_utm_history_v3`), її можна вивантажити в CSV.
- Публікація: Render, Web Service, Build `pip install -r requirements.txt`, Start `gunicorn app:app`.
- Локальний запуск: `pip install -r requirements.txt`, потім `python app.py`, далі відкрити http://localhost:5000

Попередній проект Price Radar лежить в історії комітів до цього коміту.
