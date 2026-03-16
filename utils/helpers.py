class DateHelper:
    @staticmethod
    def format_date(date):
        return date.strftime('%Y-%m-%d')

    @staticmethod
    def format_datetime(datetime):
        return datetime.strftime('%Y-%m-%d %H:%M:%S')

class CurrencyHelper:
    @staticmethod
    def format_currency(amount):
        return f'${amount:,.2f}'

class StatisticsHelper:
    @staticmethod
    def calculate_mean(numbers):
        if len(numbers) == 0:
            return 0
        return sum(numbers) / len(numbers)

    @staticmethod
    def calculate_median(numbers):
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_numbers[mid - 1] + sorted_numbers[mid]) / 2
        return sorted_numbers[mid]

    @staticmethod
    def calculate_mode(numbers):
        frequency = {}
        for number in numbers:
            frequency[number] = frequency.get(number, 0) + 1
        mode = max(frequency.items(), key=lambda x: x[1])[0]
        return mode
