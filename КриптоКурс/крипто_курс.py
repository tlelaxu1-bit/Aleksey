# -*- coding: utf-8 -*-
"""
Приложение «Курсы криптовалют»
Отображает текущие курсы популярных криптовалют к доллару США.
Источник данных: CoinGecko API (https://www.coingecko.com/en/api)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json
from datetime import datetime


# --- Настройки ---

# Список криптовалют для отображения
# Ключ — id в API CoinGecko, значение — отображаемое название
COINS = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "binancecoin": "BNB (BNB)",
    "solana": "Solana (SOL)",
    "ripple": "XRP (XRP)",
}

# URL API CoinGecko для получения цен
API_URL = (
    "https://api.coingecko.com/api/v3/simple/price"
    "?ids=bitcoin,ethereum,binancecoin,solana,ripple"
    "&vs_currencies=usd"
)


# --- Класс приложения ---

class CryptoRatesApp:
    """Главный класс приложения."""

    def __init__(self, root):
        """Инициализация интерфейса."""
        self.root = root
        self.root.title("Курсы криптовалют")
        self.root.geometry("420x420")
        self.root.resizable(False, False)

        # Словарь для хранения ссылок на ячейки с ценами
        self.price_labels = {}

        self._build_ui()

    def _build_ui(self):
        """Создание элементов интерфейса."""
        # --- Заголовок ---
        title = tk.Label(
            self.root,
            text="Курсы криптовалют",
            font=("Arial", 16, "bold"),
            bg="#4a90d9",
            fg="white",
            pady=10,
        )
        title.pack(fill="x")

        subtitle = tk.Label(
            self.root,
            text="Текущие курсы к USD (CoinGecko API)",
            font=("Arial", 9),
            fg="#666666",
        )
        subtitle.pack(pady=(5, 10))

        # --- Таблица ---
        # Фрейм для таблицы
        table_frame = tk.Frame(self.root)
        table_frame.pack(padx=20, pady=5)

        # Заголовок таблицы
        tk.Label(
            table_frame,
            text="Криптовалюта",
            font=("Arial", 10, "bold"),
            width=18,
            anchor="w",
        ).grid(row=0, column=0, sticky="w", padx=5)
        tk.Label(
            table_frame,
            text="Цена (USD)",
            font=("Arial", 10, "bold"),
            width=12,
            anchor="e",
        ).grid(row=0, column=1, sticky="e", padx=5)

        # Строки с криптовалютами
        for i, (coin_id, coin_name) in enumerate(COINS.items(), start=1):
            tk.Label(
                table_frame,
                text=coin_name,
                font=("Arial", 10),
                width=18,
                anchor="w",
            ).grid(row=i, column=0, sticky="w", padx=5, pady=3)

            price_label = tk.Label(
                table_frame,
                text="---",
                font=("Arial", 10),
                width=12,
                anchor="e",
            )
            price_label.grid(row=i, column=1, sticky="e", padx=5, pady=3)
            self.price_labels[coin_id] = price_label

        # --- Кнопка обновления ---
        self.refresh_btn = tk.Button(
            self.root,
            text="Обновить",
            font=("Arial", 11),
            bg="#4a90d9",
            fg="white",
            activebackground="#3a7bbf",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=self.refresh,
        )
        self.refresh_btn.pack(pady=15)

        # --- Статус-бар ---
        self.status_label = tk.Label(
            self.root,
            text="Последнее обновление: ---",
            font=("Arial", 8),
            fg="#999999",
            anchor="w",
        )
        self.status_label.pack(side="bottom", fill="x", padx=10, pady=(0, 10))

    def fetch_prices(self):
        """Запрос к API CoinGecko и возврат словаря цен."""
        req = urllib.request.Request(
            API_URL,
            headers={"User-Agent": "CryptoRatesApp/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data

    def refresh(self):
        """Обновление цен через API."""
        self.refresh_btn.config(state="disabled", text="Загрузка...")
        self.root.update()

        try:
            data = self.fetch_prices()

            # Обновляем цены в таблице
            for coin_id in COINS:
                if coin_id in data and "usd" in data[coin_id]:
                    price = data[coin_id]["usd"]
                    # Форматируем цену: если меньше $1 — 4 знака, иначе 2
                    if price < 1:
                        price_text = f"${price:.4f}"
                    else:
                        price_text = f"${price:,.2f}"
                    self.price_labels[coin_id].config(text=price_text)
                else:
                    self.price_labels[coin_id].config(text="Н/Д")

            # Обновляем статус-бар
            now = datetime.now().strftime("%H:%M:%S")
            self.status_label.config(text=f"Последнее обновление: {now}")

        except Exception as e:
            messagebox.showerror(
                "Ошибка",
                f"Не удалось получить данные:\n{e}",
            )
            self.status_label.config(text="Ошибка обновления")
        finally:
            self.refresh_btn.config(state="normal", text="Обновить")


# --- Запуск приложения ---

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoRatesApp(root)

    # Автоматически загружаем данные при запуске
    root.after(100, app.refresh)

    root.mainloop()
