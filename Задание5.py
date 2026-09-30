import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb


def update_currency_label(event):
    code = target_combobox.get()
    name = currencies[code]
    currency_label.config(text=name)


def exchange():
    target_code = target_combobox.get()
    base1_code = base_combobox.get()
    base2_code = base2_combobox.get()

    if not target_code or not base1_code or not base2_code:
        mb.showerror('Ошибка', 'Выберите обе базовые и целевую валюты')
        return

    results = []
    for base_code in [base1_code, base2_code]:
        try:
            result = requests.get(f"https://open.er-api.com/v6/latest/{base_code}")
            result.raise_for_status()
            data = result.json()
            if target_code in data['rates']:
                exchange_rate = data['rates'][target_code]
                base = currencies[base_code]
                target = currencies[target_code]
                results.append(f'{exchange_rate:.1f} {target} за 1 {base}')
            else:
                results.append(f'Валюта {target_code} не найдена для {base_code}')
        except Exception as e:
            results.append(f'Ошибка для {base_code}: {e}')

    mb.showinfo('Курсы обмена', '\n\n'.join(results))


currencies = {
    "USD": "Доллар США",
    "EUR": "Евро",
    "CNY": "Юань",
    "RUB": "Российский рубль",
}

pop_curr = ['EUR', 'USD', 'RUB', 'CNY']

root = Tk()
root.title("Курс валют")
root.geometry("300x200")

Label(text='Базовая валюта').pack(pady=10, padx=10)
base_combobox = ttk.Combobox(values=list(currencies.keys()))
base_combobox.pack()

Label(text='Вторая базовая валюта').pack(pady=10, padx=10)
base2_combobox = ttk.Combobox(values=list(currencies.keys()))
base2_combobox.pack()

Label(text='Целевая валюта').pack(pady=10, padx=10)
target_combobox = ttk.Combobox(values=list(currencies))
target_combobox.pack()

currency_label = ttk.Label()
currency_label.pack(pady=10, padx=10)

button = Button(text='Получить курс', command=exchange)
button.pack()

target_combobox.bind("<<ComboboxSelected>>", update_currency_label)
root.mainloop()