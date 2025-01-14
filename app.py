from flask import Flask, request, render_template, jsonify, send_file
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import mplcursors
import io
import sympy as sp  # For equation parsing
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('signu-graph.html')

@app.route('/plot', methods=['POST'])
def plot_signal():
    try:
        # Parse the request
        data = request.json
        equation = data.get('equation')
        mode = data.get('mode', 'continuous')
        x_min = float(data.get('xMin', 0))
        x_max = float(data.get('xMax', 5))
        y_min = data.get('yMin')
        y_max = data.get('yMax')

        app.logger.debug(f"Received equation: {equation}, mode: {mode}, x_min: {x_min}, x_max: {x_max}, y_min: {y_min}, y_max: {y_max}")

        # Validate the equation
        if not equation:
            return jsonify({'error': 'No equation provided.'}), 400

        # Symbols for time (t) and discrete sample index (n)
        t, n = sp.symbols('t n')
        expr = sp.sympify(equation)

        # Generate the signal
        sample_rate = 1000
        t_vals = np.linspace(x_min, x_max, sample_rate)
        n_vals = np.arange(x_min, x_max, 1)

        if mode == 'discrete':
            x_vals = n_vals
            y_vals = [float(expr.subs(n, val)) for val in n_vals]
        else:
            x_vals = t_vals
            y_vals = [float(expr.subs(t, val)) for val in t_vals]

        # Create the plot
        plt.clf()
        sns.set(style='whitegrid')
        fig, ax = plt.subplots(figsize=(10, 6))

        if mode == 'discrete':
            sns.lineplot(x=x_vals, y=y_vals, ax=ax, marker='o', linestyle='')
        else:
            sns.lineplot(x=x_vals, y=y_vals, ax=ax)

        ax.set_title("Generated Signal")
        ax.set_xlabel("Time (seconds)" if mode == 'continuous' else "n (samples)")
        ax.set_ylabel("Amplitude")

        # Apply user-provided axis limits
        if y_min is not None and y_max is not None:
            ax.set_ylim(float(y_min), float(y_max))

        ax.set_xlim(x_min, x_max)

        # Add interactive cursor
        mplcursors.cursor(ax, hover=True)

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        fig.savefig(img, format='png')
        img.seek(0)
        plt.close(fig)

        return send_file(img, mimetype='image/png')

    except Exception as e:
        app.logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
