import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_renko(tick_data, brick_size):
    """
    Generates Renko bricks from tick data.
    """
    renko_bricks = []
    if len(tick_data) == 0:
        return renko_bricks

    first_price = tick_data['price'].iloc[0]
    # Align the first brick to a multiple of the brick size
    base_price = int(first_price / brick_size) * brick_size

    for index, row in tick_data.iterrows():
        price = row['price']

        if not renko_bricks:
            # First brick
            if price >= base_price + brick_size:
                renko_bricks.append({'type': 'up', 'open': base_price, 'close': base_price + brick_size})
                base_price += brick_size
            elif price <= base_price - brick_size:
                renko_bricks.append({'type': 'down', 'open': base_price, 'close': base_price - brick_size})
                base_price -= brick_size
            continue

        if renko_bricks[-1]['type'] == 'up':
            # Check for reversal
            if price <= base_price - (2 * brick_size):
                renko_bricks.append({'type': 'down', 'open': base_price, 'close': base_price - brick_size})
                base_price -= brick_size
                # Continue adding bricks in the new direction
                while price <= base_price - brick_size:
                    renko_bricks.append({'type': 'down', 'open': base_price, 'close': base_price - brick_size})
                    base_price -= brick_size
            # Check for continuation
            while price >= base_price + brick_size:
                renko_bricks.append({'type': 'up', 'open': base_price, 'close': base_price + brick_size})
                base_price += brick_size

        elif renko_bricks[-1]['type'] == 'down':
            # Check for reversal
            if price >= base_price + (2 * brick_size):
                renko_bricks.append({'type': 'up', 'open': base_price, 'close': base_price + brick_size})
                base_price += brick_size
                # Continue adding bricks in the new direction
                while price >= base_price + brick_size:
                    renko_bricks.append({'type': 'up', 'open': base_price, 'close': base_price + brick_size})
                    base_price += brick_size
            # Check for continuation
            while price <= base_price - brick_size:
                renko_bricks.append({'type': 'down', 'open': base_price, 'close': base_price - brick_size})
                base_price -= brick_size

    return renko_bricks

def visualize_renko(renko_bricks, brick_size):
    """
    Visualizes the Renko chart.
    """
    fig, ax = plt.subplots(1)
    ax.set_title('Renko Chart')
    ax.set_xlabel('Brick Number')
    ax.set_ylabel('Price')

    for i, brick in enumerate(renko_bricks):
        if brick['type'] == 'up':
            facecolor = 'green'
        else:
            facecolor = 'red'

        rect = patches.Rectangle(
            (i, brick['open']),
            1, # width
            brick['close'] - brick['open'], # height
            facecolor=facecolor
        )
        ax.add_patch(rect)

    ax.autoscale_view()
    plt.savefig('renko_chart.png')

if __name__ == "__main__":
    # Load data
    tick_data = pd.read_csv('btc_tick_data.csv')

    # Define brick size
    brick_size = 5.0

    # Generate Renko bricks
    renko_bricks = generate_renko(tick_data, brick_size)

    # Visualize the chart
    visualize_renko(renko_bricks, brick_size)

    print("Renko chart generated and saved as renko_chart.png")