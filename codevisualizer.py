import tkinter as tk
from tkinter import ttk
import re

class CodeTile:
    def __init__(self, parent, title, code, row, col):
        self.parent = parent
        self.title = title
        self.code = code
        self.expanded = False
        
        # タイルフレーム
        self.frame = ttk.LabelFrame(parent, text=title, padding="10")
        self.frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # 概要表示
        self.summary_label = ttk.Label(self.frame, text=f"📦 {title}\n{len(code.split('\n'))} lines", 
                                      font=("Arial", 10))
        self.summary_label.pack()
        
        # 展開ボタン
        self.toggle_btn = ttk.Button(self.frame, text="🔍 詳細を見る", 
                                   command=self.toggle_code)
        self.toggle_btn.pack(pady=5)
        
        # コード表示エリア（初期は非表示）
        self.code_text = tk.Text(self.frame, height=15, width=50, wrap=tk.WORD)
        self.code_text.insert(tk.END, code)
        self.code_text.config(state=tk.DISABLED)
        
        # 編集ボタン
        self.edit_btn = ttk.Button(self.frame, text="✏️ このタイルを修正", 
                                 command=self.request_edit)
        
    def toggle_code(self):
        if self.expanded:
            # コードを隠す
            self.code_text.pack_forget()
            self.edit_btn.pack_forget()
            self.toggle_btn.config(text="🔍 詳細を見る")
            self.expanded = False
        else:
            # コードを表示
            self.code_text.pack(pady=5)
            self.edit_btn.pack(pady=2)
            self.toggle_btn.config(text="📦 タイルに戻す")
            self.expanded = True
    
    def request_edit(self):
        # 修正要求ダイアログ
        edit_window = tk.Toplevel(self.parent)
        edit_window.title(f"修正要求: {self.title}")
        edit_window.geometry("400x200")
        
        ttk.Label(edit_window, text=f"「{self.title}」の修正内容を入力:").pack(pady=10)
        
        instruction = tk.Text(edit_window, height=5, width=45)
        instruction.pack(pady=10)
        instruction.insert(tk.END, f"{self.title}の機能で、")
        
        def submit_request():
            request = instruction.get(1.0, tk.END).strip()
            print(f"[EDIT_REQUEST] {self.title}: {request}")
            # ここで実際のAI修正処理を呼び出し
            edit_window.destroy()
        
        ttk.Button(edit_window, text="🤖 AIに修正依頼", 
                  command=submit_request).pack(pady=5)

class CodeVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 CODE VISUALIZER - CLIのGUI化")
        self.root.geometry("1200x800")
        
        # メインフレーム
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # タイトル
        title = ttk.Label(main_frame, text="🎯 CODE VISUALIZER", 
                         font=("Arial", 18, "bold"))
        title.pack(pady=(0, 20))
        
        # 説明
        desc = ttk.Label(main_frame, 
                        text="AIが生成したコードをタイル状に分割表示。各タイルをクリックして詳細確認・修正依頼が可能")
        desc.pack(pady=(0, 10))
        
        # タイルコンテナ
        self.tile_container = ttk.Frame(main_frame)
        self.tile_container.pack(fill=tk.BOTH, expand=True)
        
        # サンプルコードをタイル化
        self.create_sample_tiles()
        
        # コード追加ボタン
        ttk.Button(main_frame, text="📝 新しいコードを追加", 
                  command=self.add_code_dialog).pack(pady=10)
    
    def create_sample_tiles(self):
        sample_codes = [
            {
                "title": "ファイル読み込み処理",
                "code": """def read_file(filepath):
    \"\"\"ファイルを読み込んでテキストを返す\"\"\"
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] ファイルが見つかりません: {filepath}")
        return None"""
            },
            {
                "title": "データ処理・変換",
                "code": """def process_data(raw_data):
    \"\"\"生データを処理して構造化\"\"\"
    lines = raw_data.split('\\n')
    processed = []
    for line in lines:
        if line.strip():  # 空行をスキップ
            processed.append(line.strip().upper())
    return processed"""
            },
            {
                "title": "結果出力・保存",
                "code": """def save_results(data, output_path):
    \"\"\"処理結果をファイルに保存\"\"\"
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for item in data:
                f.write(f"{item}\\n")
        print(f"[INFO] 結果を保存しました: {output_path}")
    except Exception as e:
        print(f"[ERROR] 保存に失敗: {e}")"""
            },
            {
                "title": "メイン実行処理",
                "code": """def main():
    \"\"\"メイン処理の実行\"\"\"
    input_file = "input.txt"
    output_file = "output.txt"
    
    # ファイル読み込み
    raw_data = read_file(input_file)
    if raw_data is None:
        return
    
    # データ処理
    processed = process_data(raw_data)
    
    # 結果保存
    save_results(processed, output_file)"""
            }
        ]
        
        # 2x2グリッドでタイル配置
        for i, code_info in enumerate(sample_codes):
            row = i // 2
            col = i % 2
            CodeTile(self.tile_container, 
                    code_info["title"], 
                    code_info["code"], 
                    row, col)
    
    def add_code_dialog(self):
        # 新しいコード追加ダイアログ
        add_window = tk.Toplevel(self.root)
        add_window.title("新しいコードを追加")
        add_window.geometry("600x500")
        
        ttk.Label(add_window, text="タイトル:").pack(pady=5)
        title_entry = ttk.Entry(add_window, width=50)
        title_entry.pack(pady=5)
        
        ttk.Label(add_window, text="コード:").pack(pady=5)
        code_text = tk.Text(add_window, height=20, width=70)
        code_text.pack(pady=5)
        
        def add_tile():
            title = title_entry.get()
            code = code_text.get(1.0, tk.END).strip()
            if title and code:
                # 新しいタイルを追加（簡易実装）
                print(f"[NEW_TILE] {title}")
                add_window.destroy()
        
        ttk.Button(add_window, text="📦 タイルとして追加", 
                  command=add_tile).pack(pady=10)

if __name__ == "__main__":
    app = CodeVisualizer()
    app.root.mainloop()
