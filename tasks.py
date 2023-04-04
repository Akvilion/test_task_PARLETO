'''
0. To run file type `python tasks.py in_1000000.json`.
   Example structure of `in_xxxxx.json`:
   ```
   {
    "items": [
        {
            "package": "FLEXIBLE",
            "created": "2020-03-10T00:00:00",
            "summary": [
                {
                    "period": "2019-12",
                    "documents": {
                        "incomes": 63,
                        "expenses": 13
                    }
                },
                {
                    "period": "2020-02",
                    "documents": {
                        "incomes": 45,
                        "expenses": 81
                    }
                }
            ]
        },
        {
            "package": "ENTERPRISE",
            "created": "2020-03-19T00:00:00",
            "summary": [
                {
                    "period": "2020-01",
                    "documents": {
                        "incomes": 15,
                        "expenses": 52
                    }
                },
                {
                    "period": "2020-02",
                    "documents": {
                        "incomes": 76,
                        "expenses": 47
                    }
                }
            ]
        }
    ]
   }
   ```
1. Please make below tasks described in docstring of functions in 7 days.
2. Changes out of functions body are not allowed.
3. Additional imports are not allowed.
4. Send us your solution (only tasks.py) through link in email.
   In annotations write how much time you spent for each function.
5. The data in the file is normalized.
6. First we will run automatic tests checking (using: 1 mln and 100 mln items):
   a) proper results and edge cases
   b) CPU usage
   c) memory usage
7. If your solution will NOT pass automatic tests (we allow some errors)
   application will be automatically rejected without additional feedback.
   You can apply again after 90 days.
8. Our develepers will review code (structure, clarity, logic).
'''
import datetime
import collections
import itertools


def task_1(data_in):
    '''
        Return number of items per created[year-month].
        Add missing [year-month] with 0 if no items in data.
        ex. {
            '2020-03': 29,
            '2020-04': 0, # created[year-month] does not occur in data
            '2020-05': 24
        }
    '''
    Data = collections.namedtuple('Data', ['package', 'created', 'summary'])

    Summary = collections.namedtuple('Summary', ['period', 'documents'])

    Documents = collections.namedtuple('Document', ['incomes', 'expenses'])

    all_items = itertools.chain.from_iterable(data_in.values())  # тут треба замінити на наше число

    data = (Data(package=elem['package'], created=elem['created'], summary=[Summary(period=datetime.datetime.strptime(item['period'], '%Y-%m'), documents=Documents(**item["documents"])) for item in elem['summary']]) for elem in all_items)

    counts = collections.defaultdict(int)

    for item in data:
        for summary in item.summary:
            period = summary.period
            counts[period] += 1

    start_month = min(counts.keys())
    end_month = max(counts.keys())

    month = start_month
    while month <= end_month:
        year_month = month
        if year_month not in counts:
            counts[year_month] = 0
        if month.month == 12:
            month = month.replace(year=month.year+1)
            month = month.replace(month=1)
        else:
            month = month.replace(month=month.month+1)

    counts = dict(sorted(counts.items()))

    formatted_data = {}
    for dt, value in counts.items():
        formatted_key = dt.strftime('%Y-%m')
        formatted_data[formatted_key] = value


    return formatted_data


def task_2(data_in):
    '''
        Return number of documents per period (incomes, expenses, total).
        Return only periods provided in data.
        ex. {
            '2020-04': {
                'incomes': 2480,
                'expenses': 2695,
                'total': 5175
            },
            '2020-05': {
                'incomes': 2673,
                'expenses': 2280,
                'total': 4953
            }
        }
    '''
    Data = collections.namedtuple('Data', ['package', 'created', 'summary'])

    Summary = collections.namedtuple('Summary', ['period', 'documents'])

    Documents = collections.namedtuple('Document', ['incomes', 'expenses'])

    all_items = itertools.chain.from_iterable(data_in.values())

    data = (Data(package=elem['package'], created=elem['created'], summary=[Summary(period=item['period'], documents=Documents(**item["documents"])) for item in elem['summary']]) for elem in all_items)

    result: dict = {}
    for item in data:
        for summary in item.summary:
            period = summary.period
            incomes = summary.documents.incomes
            expenses = summary.documents.expenses
            
            # If the period has not been seen before, add it to the result dictionary
            if period not in result:
                result[period] = {'incomes': 0, 'expenses': 0, 'total': 0}
            
            # Add the income and expenses for the current summary to the result dictionary
            result[period]['incomes'] += incomes
            result[period]['expenses'] += expenses
            result[period]['total'] += incomes + expenses
    
    return result


def task_3(data_in):
    '''
        Return arithmetic average(integer) number of documents per day
        in last three months counted from last period in data (all packages)
        for package in ['ENTERPRISE', 'FLEXIBLE']
        as one int
        ex. 64
    '''
    Data = collections.namedtuple('Data', ['package', 'created', 'summary'])

    Summary = collections.namedtuple('Summary', ['period', 'documents'])

    Documents = collections.namedtuple('Document', ['incomes', 'expenses'])

    all_items = itertools.chain.from_iterable(data_in.values())

    data = (Data(package=elem['package'], created=datetime.datetime.fromisoformat(elem['created']), summary=[Summary(period=datetime.datetime.strptime(item['period'], '%Y-%m'), documents=Documents(**item["documents"])) for item in elem['summary']]) for elem in all_items)

    documents_per_days = {}

    for item in data:
        if item.created in documents_per_days:
            documents_per_days[item.created] += len(item.summary)
        else:
            documents_per_days[item.created] = len(item.summary)
        
    
    latest_date = max(documents_per_days)
    m1: str = (latest_date - datetime.timedelta(days=latest_date.day))
    m2: str = (m1 - datetime.timedelta(days=m1.day))
    m2_start = datetime.datetime(year=m2.year, month=m2.month, day=1)

    total_days = latest_date.day + m1.day + m2.day

    filtered_d = {key: value for key, value in documents_per_days.items() if key > m2_start}

    total_docs = sum(value for value in filtered_d.values())

    return total_docs // total_days


if __name__ == '__main__':
    import json
    import sys
    try:
        with open(sys.argv[1]) as fp:
            data_in = json.load(fp)
    except IndexError:
        print(f'''USAGE:
    {sys.executable} {sys.argv[0]} <filename>

Example:
    {sys.executable} {sys.argv[0]} in_1000000.json
''')
    else:
        for func in [task_1, task_2, task_3]:
            print(f'\n>>> {func.__name__.upper()}')
            print(json.dumps(func(data_in), ensure_ascii=False, indent=2))


