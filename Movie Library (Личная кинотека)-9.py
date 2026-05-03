import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("1200x700")  # Уменьшил размер окна
        self.root.configure(bg='#1a1a2e')
        
        # Жанры фильмов
        self.genres = ["Боевик", "Комедия", "Драма", "Фантастика", "Ужасы", 
                       "Триллер", "Мелодрама", "Приключения", "Детектив", "Анимация"]
        
        # Данные
        self.movies = []
        self.current_file = "movies.json"
        self.filter_genre = "все"
        self.filter_year_from = ""
        self.filter_year_to = ""
        
        # Загрузка данных
        self.load_data()
        
        # Создание интерфейса
        self.create_widgets()
        self.update_movies_table()
        self.update_statistics()
    
    def create_widgets(self):
        # Заголовок
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(title_frame, text="🎬 MOVIE LIBRARY", 
                font=('Arial', 18, 'bold'), fg='#00d4ff', bg='#1a1a2e').pack()
        
        tk.Label(title_frame, text="Личная кинотека", 
                font=('Arial', 10), fg='#e0e0e0', bg='#1a1a2e').pack()
        
        tk.Label(title_frame, text="© Суроян Роман Асланович, 8 класс, 2026 г.", 
                font=('Arial', 9), fg='#f39c12', bg='#1a1a2e').pack(pady=2)
        
        # Основная панель
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill='both', expand=True, padx=15, pady=5)
        
        # Левая панель
        left_panel = tk.Frame(main_frame, bg='#1a1a2e')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Правая панель
        right_panel = tk.Frame(main_frame, bg='#1a1a2e')
        right_panel.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # ===== ЛЕВАЯ ПАНЕЛЬ - ДОБАВЛЕНИЕ =====
        add_frame = tk.LabelFrame(left_panel, text=" 🎬 ДОБАВИТЬ ФИЛЬМ ", 
                                   font=('Arial', 10, 'bold'), 
                                   fg='#00d4ff', bg='#16213e')
        add_frame.pack(fill='x', pady=5, padx=5)
        
        fields_frame = tk.Frame(add_frame, bg='#16213e')
        fields_frame.pack(padx=15, pady=15)
        
        # Название
        tk.Label(fields_frame, text="🎥 Название фильма:", font=('Arial', 10, 'bold'), 
                fg='white', bg='#16213e').grid(row=0, column=0, sticky='w', pady=5)
        self.title_entry = tk.Entry(fields_frame, width=25, font=('Arial', 10), bg='white')
        self.title_entry.grid(row=0, column=1, padx=8, pady=5)
        
        # Жанр
        tk.Label(fields_frame, text="📂 Жанр:", font=('Arial', 10, 'bold'), 
                fg='white', bg='#16213e').grid(row=1, column=0, sticky='w', pady=5)
        self.genre_combo = ttk.Combobox(fields_frame, values=self.genres, 
                                        width=22, font=('Arial', 10))
        self.genre_combo.set('Боевик')
        self.genre_combo.grid(row=1, column=1, padx=8, pady=5)
        
        # Год выпуска
        tk.Label(fields_frame, text="📅 Год выпуска:", font=('Arial', 10, 'bold'), 
                fg='white', bg='#16213e').grid(row=2, column=0, sticky='w', pady=5)
        self.year_entry = tk.Entry(fields_frame, width=25, font=('Arial', 10), bg='white')
        self.year_entry.grid(row=2, column=1, padx=8, pady=5)
        
        # Рейтинг
        tk.Label(fields_frame, text="⭐ Рейтинг (0-10):", font=('Arial', 10, 'bold'), 
                fg='white', bg='#16213e').grid(row=3, column=0, sticky='w', pady=5)
        self.rating_entry = tk.Entry(fields_frame, width=25, font=('Arial', 10), bg='white')
        self.rating_entry.grid(row=3, column=1, padx=8, pady=5)
        
        # Кнопка добавления
        tk.Button(fields_frame, text="➕ ДОБАВИТЬ ФИЛЬМ", command=self.add_movie,
                 bg='#00d4ff', fg='#1a1a2e', font=('Arial', 10, 'bold'),
                 padx=10, pady=8, cursor='hand2').grid(row=4, column=0, columnspan=2, pady=15)
        
        # ===== ЛЕВАЯ ПАНЕЛЬ - СТАТИСТИКА =====
        stats_frame = tk.LabelFrame(left_panel, text=" 📊 СТАТИСТИКА ", 
                                     font=('Arial', 10, 'bold'), 
                                     fg='#00d4ff', bg='#16213e')
        stats_frame.pack(fill='both', expand=True, pady=5, padx=5)
        
        stats_container = tk.Frame(stats_frame, bg='#16213e')
        stats_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.stats_text = tk.Text(stats_container, height=10, width=35,
                                  bg='#16213e', fg='#00d4ff',
                                  font=('Consolas', 8), wrap='word',
                                  relief='flat', borderwidth=0)
        
        stats_scroll = ttk.Scrollbar(stats_container, orient='vertical', command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scroll.set)
        
        self.stats_text.pack(side='left', fill='both', expand=True)
        stats_scroll.pack(side='right', fill='y')
        
        # ===== ПРАВАЯ ПАНЕЛЬ - ФИЛЬТРЫ =====
        filter_frame = tk.LabelFrame(right_panel, text=" 🔍 ФИЛЬТРАЦИЯ ", 
                                      font=('Arial', 10, 'bold'), 
                                      fg='#00d4ff', bg='#16213e')
        filter_frame.pack(fill='x', pady=5, padx=5)
        
        filter_inner = tk.Frame(filter_frame, bg='#16213e')
        filter_inner.pack(padx=10, pady=10)
        
        # Фильтр по жанру
        tk.Label(filter_inner, text="Жанр:", font=('Arial', 9, 'bold'), 
                fg='white', bg='#16213e').grid(row=0, column=0, sticky='w', pady=3)
        
        self.filter_genre_combo = ttk.Combobox(filter_inner, 
                                               values=['все'] + self.genres, 
                                               width=18, font=('Arial', 9))
        self.filter_genre_combo.set('все')
        self.filter_genre_combo.grid(row=0, column=1, padx=8, pady=3)
        
        # Фильтр по году
        tk.Label(filter_inner, text="Год от:", font=('Arial', 9, 'bold'), 
                fg='white', bg='#16213e').grid(row=1, column=0, sticky='w', pady=3)
        self.filter_year_from_entry = tk.Entry(filter_inner, width=12, font=('Arial', 9))
        self.filter_year_from_entry.grid(row=1, column=1, padx=8, pady=3)
        
        tk.Label(filter_inner, text="Год до:", font=('Arial', 9, 'bold'), 
                fg='white', bg='#16213e').grid(row=2, column=0, sticky='w', pady=3)
        self.filter_year_to_entry = tk.Entry(filter_inner, width=12, font=('Arial', 9))
        self.filter_year_to_entry.grid(row=2, column=1, padx=8, pady=3)
        
        # Кнопки фильтрации
        btn_frame = tk.Frame(filter_inner, bg='#16213e')
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Button(btn_frame, text="🔍 ПРИМЕНИТЬ", command=self.apply_filter,
                 bg='#0f3460', fg='white', font=('Arial', 9, 'bold'),
                 cursor='hand2', padx=10, pady=3).pack(side='left', padx=3)
        
        tk.Button(btn_frame, text="🔄 СБРОСИТЬ", command=self.reset_filter,
                 bg='#533483', fg='white', font=('Arial', 9, 'bold'),
                 cursor='hand2', padx=10, pady=3).pack(side='left', padx=3)
        
        # ===== ПРАВАЯ ПАНЕЛЬ - ТАБЛИЦА =====
        table_frame = tk.LabelFrame(right_panel, text=" 📋 СПИСОК ФИЛЬМОВ ", 
                                     font=('Arial', 10, 'bold'), 
                                     fg='#00d4ff', bg='#16213e')
        table_frame.pack(fill='both', expand=True, pady=5, padx=5)
        
        table_container = tk.Frame(table_frame, bg='#16213e')
        table_container.pack(fill='both', expand=True, padx=8, pady=8)
        
        columns = ('title', 'genre', 'year', 'rating')
        self.tree = ttk.Treeview(table_container, columns=columns, show='headings', height=8)
        
        self.tree.heading('title', text='🎬 НАЗВАНИЕ')
        self.tree.heading('genre', text='📂 ЖАНР')
        self.tree.heading('year', text='📅 ГОД')
        self.tree.heading('rating', text='⭐ РЕЙТИНГ')
        
        self.tree.column('title', width=180)
        self.tree.column('genre', width=100)
        self.tree.column('year', width=70, anchor='center')
        self.tree.column('rating', width=120, anchor='center')
        
        scroll_y = ttk.Scrollbar(table_container, orient='vertical', command=self.tree.yview)
        scroll_x = ttk.Scrollbar(table_container, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scroll_y.pack(side='right', fill='y')
        scroll_x.pack(side='bottom', fill='x')
        
        # ===== ПРАВАЯ ПАНЕЛЬ - КНОПКИ JSON =====
        json_frame = tk.LabelFrame(right_panel, text=" 💾 РАБОТА С ДАННЫМИ ", 
                                    font=('Arial', 10, 'bold'), 
                                    fg='#00d4ff', bg='#16213e')
        json_frame.pack(fill='x', pady=5, padx=5)
        
        json_buttons = tk.Frame(json_frame, bg='#16213e')
        json_buttons.pack(fill='x', padx=10, pady=10)
        
        tk.Button(json_buttons, text="💾 СОХРАНИТЬ", command=self.save_json,
                 bg='#0f3460', fg='white', font=('Arial', 9, 'bold'),
                 cursor='hand2', pady=6).pack(side='left', padx=3, expand=True, fill='x')
        
        tk.Button(json_buttons, text="📂 ЗАГРУЗИТЬ", command=self.load_json,
                 bg='#0f3460', fg='white', font=('Arial', 9, 'bold'),
                 cursor='hand2', pady=6).pack(side='left', padx=3, expand=True, fill='x')
        
        tk.Button(json_buttons, text="🗑️ ОЧИСТИТЬ", command=self.clear_all,
                 bg='#e94560', fg='white', font=('Arial', 9, 'bold'),
                 cursor='hand2', pady=6).pack(side='left', padx=3, expand=True, fill='x')
        
        self.file_info = tk.Label(json_frame, text=f"📄 Файл: {self.current_file}", 
                                  font=('Arial', 8), fg='#95a5a6', bg='#16213e')
        self.file_info.pack(pady=5)
        
        # ===== ИНСТРУКЦИЯ =====
        self.create_instruction(right_panel)
    
    def create_instruction(self, parent):
        """Создание компактной инструкции с прокруткой"""
        instr_frame = tk.LabelFrame(parent, text=" 📖 ИНСТРУКЦИЯ ", 
                                    font=('Arial', 10, 'bold'), 
                                    fg='#00d4ff', bg='#16213e')
        instr_frame.pack(fill='both', expand=True, pady=5, padx=5)
        
        text_frame = tk.Frame(instr_frame, bg='#16213e')
        text_frame.pack(fill='both', expand=True, padx=8, pady=8)
        
        instr_text = tk.Text(text_frame, 
                             bg='#16213e', 
                             fg='#00d4ff',
                             font=('Consolas', 8), 
                             wrap='word',
                             relief='flat', 
                             borderwidth=0,
                             height=8,
                             selectbackground='#0f3460')
        
        scroll_instr = ttk.Scrollbar(text_frame, orient='vertical', command=instr_text.yview)
        instr_text.configure(yscrollcommand=scroll_instr.set)
        
        instruction = """
╔════════════════════════════════════════════════════════════╗
║                   📖 КРАТКАЯ ИНСТРУКЦИЯ                    ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  📌 КАК ДОБАВИТЬ ФИЛЬМ:                                    ║
║  1. Введите название фильма                                ║
║  2. Выберите жанр                                          ║
║  3. Укажите год выпуска (1888-2026)                       ║
║  4. Укажите рейтинг (0-10)                                ║
║  5. Нажмите "ДОБАВИТЬ ФИЛЬМ"                              ║
║                                                            ║
║  🔍 ФИЛЬТРАЦИЯ:                                            ║
║  • Выберите жанр или укажите диапазон годов               ║
║  • Нажмите "ПРИМЕНИТЬ"                                    ║
║  • Нажмите "СБРОСИТЬ" для отмены фильтра                  ║
║                                                            ║
║  📊 СТАТИСТИКА:                                            ║
║  • Обновляется автоматически                              ║
║  • Показывает средний рейтинг, лучший/худший фильм,       ║
║    распределение по жанрам                                ║
║                                                            ║
║  💾 РАБОТА С JSON:                                         ║
║  • "СОХРАНИТЬ" - сохранить коллекцию в файл               ║
║  • "ЗАГРУЗИТЬ" - загрузить коллекцию из файла             ║
║  • "ОЧИСТИТЬ" - удалить все фильмы                        ║
║                                                            ║
║  💡 СОВЕТЫ:                                                ║
║  • Регулярно сохраняйте коллекцию                         ║
║  • Используйте фильтры для поиска                         ║
║  • Оценивайте фильмы честно                               ║
║                                                            ║
║  ⚠️ ВАЖНО:                                                 ║
║  • Год: только числа от 1888 до 2026                     ║
║  • Рейтинг: числа от 0 до 10 (можно 8.5)                 ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

        © Суроян Роман Асланович, 8 класс, 2026
        """
        
        instr_text.insert('1.0', instruction)
        instr_text.config(state='disabled')
        
        instr_text.pack(side='left', fill='both', expand=True)
        scroll_instr.pack(side='right', fill='y')
    
    def add_movie(self):
        """Добавление фильма"""
        title = self.title_entry.get().strip()
        genre = self.genre_combo.get()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()
        
        if not title:
            messagebox.showerror("Ошибка", "❌ Введите название фильма!")
            return
        
        if not year:
            messagebox.showerror("Ошибка", "❌ Введите год выпуска!")
            return
        
        try:
            year_int = int(year)
            if year_int < 1888 or year_int > 2026:
                messagebox.showerror("Ошибка", "❌ Год должен быть от 1888 до 2026!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "❌ Год должен быть числом!")
            return
        
        if not rating:
            messagebox.showerror("Ошибка", "❌ Введите рейтинг!")
            return
        
        try:
            rating_float = float(rating)
            if rating_float < 0 or rating_float > 10:
                messagebox.showerror("Ошибка", "❌ Рейтинг должен быть от 0 до 10!")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "❌ Рейтинг должен быть числом!")
            return
        
        movie = {
            "title": title,
            "genre": genre,
            "year": year_int,
            "rating": rating_float
        }
        self.movies.append(movie)
        self.movies.sort(key=lambda x: x['title'])
        
        self.title_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
        
        self.update_movies_table()
        self.update_statistics()
        self.save_json()
        
        messagebox.showinfo("Успех", f"✅ Фильм добавлен!\n\n🎬 {title}\n📂 {genre}\n📅 {year}\n⭐ {rating}")
    
    def update_movies_table(self):
        """Обновление таблицы фильмов"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filtered = self.get_filtered_movies()
        
        for movie in filtered:
            stars = "⭐" * int(movie['rating'] // 2) + "☆" * (5 - int(movie['rating'] // 2))
            rating_display = f"{movie['rating']:.1f} {stars}"
            
            self.tree.insert('', 'end', values=(
                movie['title'],
                movie['genre'],
                movie['year'],
                rating_display
            ))
    
    def get_filtered_movies(self):
        """Получение отфильтрованных фильмов"""
        filtered = self.movies.copy()
        
        if self.filter_genre != "все":
            filtered = [m for m in filtered if m['genre'] == self.filter_genre]
        
        if self.filter_year_from:
            try:
                year_from = int(self.filter_year_from)
                filtered = [m for m in filtered if m['year'] >= year_from]
            except:
                pass
        
        if self.filter_year_to:
            try:
                year_to = int(self.filter_year_to)
                filtered = [m for m in filtered if m['year'] <= year_to]
            except:
                pass
        
        return filtered
    
    def update_statistics(self):
        """Обновление статистики"""
        self.stats_text.config(state='normal')
        self.stats_text.delete('1.0', tk.END)
        
        filtered = self.get_filtered_movies()
        
        total = len(filtered)
        
        if total > 0:
            avg_rating = sum(m['rating'] for m in filtered) / total
            max_rating = max(m['rating'] for m in filtered)
            min_rating = min(m['rating'] for m in filtered)
            max_title = max((m['rating'], m['title']) for m in filtered)[1]
            min_title = min((m['rating'], m['title']) for m in filtered)[1]
        else:
            avg_rating = 0
            max_rating = 0
            min_rating = 0
            max_title = "-"
            min_title = "-"
        
        genre_counts = {}
        for genre in self.genres:
            genre_counts[genre] = len([m for m in filtered if m['genre'] == genre])
        
        stats = f"""
╔══════════════════════════════════════╗
║            📊 СТАТИСТИКА             ║
╠══════════════════════════════════════╣
║                                      ║
║  🎬 ВСЕГО ФИЛЬМОВ: {total:>4}                   ║
║                                      ║
║  ⭐ СР. РЕЙТИНГ: {avg_rating:>5.1f}/10            ║
║                                      ║
║  🏆 ЛУЧШИЙ:                          ║
║     {max_rating:.1f}⭐ - {max_title[:20]}   ║
║                                      ║
║  📉 ХУДШИЙ:                          ║
║     {min_rating:.1f}⭐ - {min_title[:20]}   ║
║                                      ║
║  📂 ПО ЖАНРАМ:                       ║
"""
        
        for genre, count in genre_counts.items():
            if count > 0:
                stats += f"     {genre}: {count:>2} шт.\n"
        
        stats += """
║                                      ║
╚══════════════════════════════════════╝
"""
        
        self.stats_text.insert('1.0', stats)
        self.stats_text.config(state='disabled')
    
    def apply_filter(self):
        """Применение фильтра"""
        self.filter_genre = self.filter_genre_combo.get()
        self.filter_year_from = self.filter_year_from_entry.get().strip()
        self.filter_year_to = self.filter_year_to_entry.get().strip()
        
        if self.filter_year_from:
            try:
                int(self.filter_year_from)
            except:
                messagebox.showerror("Ошибка", "❌ Год 'от' должен быть числом!")
                return
        
        if self.filter_year_to:
            try:
                int(self.filter_year_to)
            except:
                messagebox.showerror("Ошибка", "❌ Год 'до' должен быть числом!")
                return
        
        self.update_movies_table()
        self.update_statistics()
        
        filtered = self.get_filtered_movies()
        messagebox.showinfo("Фильтр", f"🔍 Применён фильтр!\n\n📊 Найдено фильмов: {len(filtered)}")
    
    def reset_filter(self):
        """Сброс фильтра"""
        self.filter_genre = "все"
        self.filter_genre_combo.set("все")
        self.filter_year_from_entry.delete(0, tk.END)
        self.filter_year_to_entry.delete(0, tk.END)
        self.filter_year_from = ""
        self.filter_year_to = ""
        
        self.update_movies_table()
        self.update_statistics()
        
        messagebox.showinfo("Фильтр", f"🔄 Фильтр сброшен!\n\n📊 Всего фильмов: {len(self.movies)}")
    
    def save_json(self):
        """Сохранение в JSON"""
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=2)
            self.file_info.config(text=f"📄 Файл: {self.current_file} ✓ Сохранено")
            messagebox.showinfo("Успех", f"✅ Данные сохранены!\n\n📁 Файл: {self.current_file}\n🎬 Фильмов: {len(self.movies)}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"❌ Не удалось сохранить!\n{str(e)}")
    
    def load_json(self):
        """Загрузка из JSON"""
        file_path = filedialog.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Выберите JSON файл для загрузки"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                    if isinstance(loaded_data, list):
                        self.movies = loaded_data
                        self.current_file = file_path
                        self.reset_filter()
                        self.update_movies_table()
                        self.update_statistics()
                        self.file_info.config(text=f"📄 Файл: {self.current_file}")
                        
                        messagebox.showinfo("Успех", f"✅ Загружено {len(self.movies)} фильмов!\n\n📁 Файл: {file_path}")
                    else:
                        messagebox.showerror("Ошибка", "❌ Неверный формат файла!")
                        
            except json.JSONDecodeError:
                messagebox.showerror("Ошибка", "❌ Файл повреждён!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"❌ Не удалось загрузить!\n{str(e)}")
    
    def load_data(self):
        """Загрузка данных при запуске"""
        if os.path.exists(self.current_file):
            try:
                with open(self.current_file, 'r', encoding='utf-8') as f:
                    self.movies = json.load(f)
                print(f"Загружено {len(self.movies)} фильмов из {self.current_file}")
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.movies = []
    
    def clear_all(self):
        """Очистка всех данных"""
        if messagebox.askyesno("Подтверждение", "🗑️ Удалить ВСЕ фильмы?\n\nЭто действие нельзя отменить!"):
            self.movies = []
            self.reset_filter()
            self.update_movies_table()
            self.update_statistics()
            self.save_json()
            messagebox.showinfo("Успех", "✅ Все фильмы удалены!")


if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()
        
      
