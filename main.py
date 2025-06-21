import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDRectangleFlatButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

# Configure window size
Window.size = (1000, 700)

# Nifty 50 symbols (reduced for testing)
NIFTY_50_SYMBOLS = [
    'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS',
    'HINDUNILVR.NS', 'ITC.NS', 'KOTAKBANK.NS', 'BHARTIARTL.NS', 'LT.NS',
    'SBIN.NS', 'BAJFINANCE.NS', 'HCLTECH.NS', 'ASIANPAINT.NS', 'MARUTI.NS',
    'TITAN.NS', 'SUNPHARMA.NS', 'AXISBANK.NS', 'ULTRACEMCO.NS', 'NTPC.NS',
    'ONGC.NS', 'NESTLEIND.NS', 'POWERGRID.NS', 'M&M.NS', 'TECHM.NS',
    'WIPRO.NS', 'ADANIPORTS.NS', 'JSWSTEEL.NS', 'HDFCLIFE.NS', 'DRREDDY.NS',
    'BAJAJFINSV.NS', 'TATASTEEL.NS', 'BRITANNIA.NS', 'GRASIM.NS', 'SHREECEM.NS',
    'UPL.NS', 'DIVISLAB.NS', 'IOC.NS', 'COALINDIA.NS', 'BPCL.NS', 'CIPLA.NS',
    'HINDALCO.NS', 'INDUSINDBK.NS', 'EICHERMOT.NS', 'HEROMOTOCO.NS', 'VEDL.NS',
    'JINDALSTEL.NS', 'GAIL.NS', 'TATACONSUM.NS', 'HDFCAMC.NS', 'APOLLOHOSP.NS'
]


# Color scheme
COLORS = {
    'primary': get_color_from_hex('#2E86AB'),
    'secondary': get_color_from_hex('#A23B72'),
    'background': get_color_from_hex('#F5F5F5'),
    'overbought': get_color_from_hex('#E63946'),
    'oversold': get_color_from_hex('#2A9D8F'),
    'neutral': get_color_from_hex('#F4A261')
}

Builder.load_string('''
<MainLayout>:
    orientation: 'vertical'
    spacing: '10dp'
    padding: '10dp'
    md_bg_color: app.colors['background']

    MDTopAppBar:
        id: toolbar
        title: "Nifty 50 RSI Analyzer"
        elevation: 10
        left_action_items: [["chart-line", lambda x: None]]
        md_bg_color: app.colors['primary']
        specific_text_color: [1, 1, 1, 1]

    BoxLayout:
        size_hint_y: None
        height: dp(60)
        spacing: '20dp'
        padding: '10dp'

        MDRectangleFlatButton:
            id: rsi_period_btn
            text: "RSI Period: 14"
            on_release: root.open_period_menu()
            size_hint_x: 0.2
            md_bg_color: app.colors['secondary']
            text_color: [1, 1, 1, 1]

        MDFlatButton:
            text: "Refresh Data"
            on_release: app.refresh_data()
            size_hint_x: 0.2
            md_bg_color: app.colors['primary']
            text_color: [1, 1, 1, 1]

        MDLabel:
            id: last_updated_label
            text: "Last Updated: Not updated yet"
            halign: 'right'
            size_hint_x: 0.6
            theme_text_color: 'Secondary'

    BoxLayout:
        id: table_container
        orientation: 'vertical'
''')

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app = App.get_running_app()
        self.table = None
        self.create_table()

    def create_table(self):
        """Initialize the data table"""
        if self.table:
            self.ids.table_container.remove_widget(self.table)
        
        self.table = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Symbol", dp(30)),
                ("Price (₹)", dp(25)),
                (f"RSI ({self.app.rsi_period})", dp(25)),
                ("Status", dp(30))
            ],
            row_data=[],
            elevation=2,
            background_color_header=COLORS['primary'],
            background_color_cell=COLORS['background'],
            background_color_selected_cell=COLORS['secondary']
        )
        self.ids.table_container.add_widget(self.table)

    def open_period_menu(self):
        menu_items = [
            {"text": "RSI 7", "on_release": lambda x="7": self.set_rsi_period(x)},
            {"text": "RSI 14", "on_release": lambda x="14": self.set_rsi_period(x)},
            {"text": "RSI 21", "on_release": lambda x="21": self.set_rsi_period(x)},
            {"text": "RSI 28", "on_release": lambda x="28": self.set_rsi_period(x)},
            {"text": "RSI 35", "on_release": lambda x="35": self.set_rsi_period(x)},
            {"text": "RSI 42", "on_release": lambda x="42": self.set_rsi_period(x)},
            {"text": "RSI 49", "on_release": lambda x="49": self.set_rsi_period(x)},
            {"text": "RSI 56", "on_release": lambda x="56": self.set_rsi_period(x)},
            {"text": "RSI 63", "on_release": lambda x="63": self.set_rsi_period(x)},
            {"text": "RSI 70", "on_release": lambda x="70": self.set_rsi_period(x)}
        ]
        MDDropdownMenu(
            caller=self.ids.rsi_period_btn,
            items=menu_items,
            width_mult=4,
            background_color=COLORS['background']
        ).open()

    def set_rsi_period(self, period):
        self.ids.rsi_period_btn.text = f"RSI Period: {period}"
        self.app.rsi_period = int(period)
        self.app.refresh_data()

class RSITable(MDApp):
    colors = COLORS
    rsi_period = 14
    
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.main_layout = MainLayout()
        self.refresh_data()
        return self.main_layout

    def refresh_data(self, *args):
        if not hasattr(self, 'main_layout'):
            return
            
        self.main_layout.ids.toolbar.title = "Nifty 50 RSI Analyzer (Updating...)"
        self.main_layout.ids.last_updated_label.text = f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        table_data = []
        
        for symbol in NIFTY_50_SYMBOLS:
            try:
                data = yf.download(
                    symbol,
                    period="2mo",
                    progress=False,
                    auto_adjust=True
                )
                
                if len(data) < self.rsi_period + 1:
                    continue
                
                close_prices = data['Close'].values
                if close_prices.ndim != 1:
                    close_prices = close_prices.flatten()
                
                rsi = self.calculate_rsi(close_prices, self.rsi_period)
                
                if len(rsi) == 0 or np.isnan(rsi[-1]):
                    continue
                
                last_rsi = float(rsi[-1])
                last_price = float(close_prices[-1])
                
                if last_rsi > 70:
                    status = "🔴 Overbought"
                elif last_rsi < 30:
                    status = "🟢 Oversold"
                else:
                    status = "⚪ Neutral"
                
                table_data.append((
                    symbol.replace('.NS', ''),
                    f"{last_price:.2f}",
                    f"{last_rsi:.2f}",
                    status
                ))
                
            except Exception as e:
                print(f"Error processing {symbol}: {str(e)}")
                continue
        
        # Recreate table with new period
        self.main_layout.create_table()
        self.main_layout.table.column_data = [
            ("Symbol", dp(30)),
            ("Price (₹)", dp(25)),
            (f"RSI ({self.rsi_period})", dp(25)),
            ("Status", dp(30))
        ]
        self.main_layout.table.row_data = sorted(table_data, key=lambda x: float(x[2]), reverse=True)
        self.main_layout.ids.toolbar.title = "Nifty 50 RSI Analyzer"

    def calculate_rsi(self, prices, window=14):
        """Robust RSI calculation with complete error handling"""
        if len(prices) < window + 1:
            return np.array([])
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[:window])
        avg_loss = np.mean(losses[:window])
        
        if avg_loss == 0:
            return np.full(len(prices), 100) if avg_gain > 0 else np.full(len(prices), 50)
        
        rs = avg_gain / avg_loss
        rsi = np.zeros(len(prices))
        rsi[:window] = 100 - (100 / (1 + rs))
        
        for i in range(window, len(prices)):
            delta = deltas[i-1]
            current_gain = max(delta, 0)
            current_loss = max(-delta, 0)
            
            avg_gain = (avg_gain * (window - 1) + current_gain) / window
            avg_loss = (avg_loss * (window - 1) + current_loss) / window
            
            if avg_loss == 0:
                rsi[i] = 100 if avg_gain > 0 else 50
            else:
                rs = avg_gain / avg_loss
                rsi[i] = 100 - (100 / (1 + rs))
        
        return rsi

if __name__ == "__main__":
    RSITable().run()