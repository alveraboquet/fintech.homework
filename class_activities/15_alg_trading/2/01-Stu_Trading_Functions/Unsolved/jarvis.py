def initialize(cash=None):
    """Initialize the dashboard, data storage, and account balances."""
    return

def build_dashboard():
    """Build the dashboard."""

    price_df = signals_df[['close','SMA50','SMA100']]
    price_chart = price_df.hvplot.line().opts(xaxis=None)

    portfolio_evaluation_table = portfolio_evaluation_table_hvplot.table(columns=['index', 'Backatest'])

    dashboard = pn.Column("Trading Dashboard", price_chart, portfolio_evaluation_table)

    return dashboard

def fetch_data():
    """Fetches the latest prices."""

    filepath = Path('../Resources/aaple.csv')
    data_df = pd.read_csv(filepath)

    # Print data
    print(data_df.head())

    return data_df

def generate_signals():
    """Generates trading signals for a given dataset."""

    signals_df = data_df[:,['date','close']].copy()
    signals_df = signals_df.set_index('date', drop=True)
    
    short_window = 50
    long_window = 100

    signals_df['SMA50'] = signals_df['close'].rolling(window=short_window).mean()
    signals_df['SMA100'] = signals_df['close'].rolling(window=long_window).mean()
    signals_df['Signal'] = 0.0

    signals_df["Signal"][short_window:] = np.where(
        signals_df["SMA50"][short_window:] > signals_df["SMA100"][short_window:], 1.0, 0.0)

    signals_df["Entry/Exit"] = signals_df["Signal"].diff()

    return signals_df


def execute_backtest():
    """Backtests signal data."""

    # Set initial capital
    initial_capital = float(100000)

    # Set the share size
    share_size = -500

    # Take a 500 share position where the dual moving average crossover is 1 (SMA50 is greater than SMA100)
    signals_df["Position"] = share_size * signals_df["Signal"]

    # Find the points in time where a 500 share position is bought or sold
    signals_df["Entry/Exit Position"] = signals_df["Position"].diff()

    # Multiply share price by entry/exit positions and get the cumulatively sum
    signals_df["Portfolio Holdings"] = (
        signals_df["Close"] * signals_df["Entry/Exit Position"].cumsum())

    # Subtract the initial capital by the portfolio holdings to get the amount of liquid cash in the portfolio
    signals_df["Portfolio Cash"] = (
        initial_capital - (signals_df["Close"] * signals_df["Entry/Exit Position"]).cumsum())

    # Get the total portfolio value by adding the cash amount by the portfolio holdings (or investments)
    signals_df["Portfolio Total"] = (
        signals_df["Portfolio Cash"] + signals_df["Portfolio Holdings"])

    # Calculate the portfolio daily returns
    signals_df["Portfolio Daily Returns"] = signals_df["Portfolio Total"].pct_change()

    # Calculate the cumulative returns
    signals_df["Portfolio Cumulative Returns"] = (
        1 + signals_df["Portfolio Daily Returns"]).cumprod() - 1

    # Print the DataFrame
    # signals_df.head()
    return signals_df

def execute_trade_strategy():
    """Makes a buy/sell/hold decision."""
    return

def evaluate_metrics():
    """Generates evaluation metrics from backtested signal data."""

        # Prepare DataFrame for metrics
    metrics = [
        'Annual Return',
        'Cumulative Returns',
        'Annual Volatility',
        'Sharpe Ratio',
        'Sortino Ratio']

    columns = ['Backtest']

    # Initialize the DataFrame with index set to evaluation metrics and column as `Backtest` (just like PyFolio)
    portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)

    # Calculate cumulative return
    portfolio_evaluation_df.loc['Cumulative Returns'] = signals_df['Portfolio Cumulative Returns'][-1]

    # Calculate annualized return
    portfolio_evaluation_df.loc['Annual Return'] = (
        signals_df['Portfolio Daily Returns'].mean() * 252)

        # Calculate annual volatility
        portfolio_evaluation_df.loc['Annual Volatility'] = (
            signals_df['Portfolio Daily Returns'].std() * np.sqrt(252))
    return

def update_dashboard():
    """Updates the dashboard."""
    return

def main():
    """Main Event Loop."""
    # @TODO: Call the functions above in the correct order to execute a trade

    data_df = fetch_data()
    signals_df = generate_signals(data_df)
    tested_signals_df = execute_backtest(signals_df)
    portfolio_evaluation_df = evaluate_metrics(tested_signals_df)
    dashboard = build_dashboard(tested_signals_df, portfolio_evaluation_df)
    hvplot.show(dashboard)

    return