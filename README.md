# Salary Scanner

This Python project retrieves salary data from HeadHunter (hh.ru) and SuperJob (superjob.ru), calculates the average ruble salaries for a list of programming languages, and displays consolidated statistics in the terminal.

---

## Features

- Support for multiple sources: HeadHunter and SuperJob  
- Configurable list of programming languages via CLI  
- Fetch vacancies from the last 30 days with pagination  
- Calculate average salary (RUR) using:
  - if both “from” and “to” are present: `(from + to) / 2`
  - if only “from” is present: `from * 1.2`
  - if only “to” is present: `to * 0.8`  
- Output results in readable ASCII tables  

---

## Prerequisites

- Python 3.6 or newer  
- A `requirements.txt` file listing project dependencies  

---

## Installation and Setup

1. **Clone the repository or download the scripts**  
   ```bash
   git clone https://github.com/your_username/your_repo.git
   cd your_repo
   ```

2. **(Optional) Create and activate a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate       # Linux/macOS
   venv\Scripts\activate        # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**  
   Create a `.env` file in the project root containing:
   ```dotenv
   SJ_SECRET_KEY=your_superjob_api_key
   ```

---

## Environment Variables

The application uses the following environment variables:

- `SJ_SECRET_KEY` — SuperJob API App ID (used as `X-Api-App-Id` header)

Ensure you have created the `.env` file and defined these variables before running the program.

---

## Usage

Run the script with the `--search` option followed by programming languages separated by spaces:

```bash
python main.py --search Python JavaScript Java
```

- If `--search` is omitted, the default set of languages is:  
  `Python JavaScript Typescript Java C#`  
- You can specify any combination, for example:  
  ```bash
  python main.py --search Go Rust
  ```

---

## Example Output

```
+HeadHunter Moscow------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 2000             | 509                 | 196886.0         |
| OR                    | 8000             | 4984                | 179647.0         |
| JavaScript            | 2000             | 695                 | 187340.0         |
| Typescript            | 845              | 231                 | 218586.0         |
| Java                  | 1822             | 277                 | 209904.0         |
| C#                    | 894              | 225                 | 213136.0         |
+-----------------------+------------------+---------------------+------------------+

+SuperJob Moscow--------+------------------+---------------------+------------------+
| Язык программирования | Вакансий найдено | Вакансий обработано | Средняя зарплата |
+-----------------------+------------------+---------------------+------------------+
| Python                | 9                | 3                   | 154667.0         |
| OR                    | 0                | 0                   | 0.0              |
| JavaScript            | 5                | 3                   | 108000.0         |
| Typescript            | 0                | 0                   | 0.0              |
| Java                  | 3                | 1                   | 90000.0          |
| C#                    | 1                | 1                   | 237500.0         |
+-----------------------+------------------+---------------------+------------------+

```

---

## Notes

- The script processes only vacancies with salaries in rubles (RUR).  
- To adjust pagination settings, modify `per_page` and `max_pages` parameters in the source code.  
- You can extend this project by adding new modules (`api/`, `processing/`, `stats/`, `printer/`) for additional sources or calculations.
