from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import seaborn as sns
import math
import logging
import traceback
import re

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Set Seaborn style globally
sns.set(style="darkgrid")

def validate_equation(equation):
    """Validate and clean the equation string."""
    logger.debug(f"Original equation: {equation}")
    
    # Remove any whitespace
    equation = equation.strip().replace(' ', '')
    
    # Fix common typos and mistakes
    replacements = {
        'ex_valuesp': 'exp',
        'ex_values': 'exp',
        'ex_': 'exp',
        'x_values': 'x',  # Replace any accidental x_values with x
    }
    
    for old, new in replacements.items():
        equation = equation.replace(old, new)
    
    # Ensure proper parentheses
    if '(' in equation:
        open_count = equation.count('(')
        close_count = equation.count(')')
        if open_count > close_count:
            equation += ')' * (open_count - close_count)
    
    # Validate final equation format
    valid_functions = ['exp', 'sin', 'cos', 'tan', 'log', 'sqrt', 'abs']
    valid_pattern = r'^([a-z]+\([x0-9\+\-\*\/\s\.]+\))$'
    
    #if not re.match(valid_pattern, equation):
    #    raise ValueError(f"Invalid equation format: {equation}. Please use format like 'exp(x)' or 'sin(x)'")
    
    logger.debug(equation)
    function_name = equation.split('(')[0]
    #if function_name not in valid_functions:
    #    raise ValueError(f"Unknown function: {function_name}. Valid functions are: {', '.join(valid_functions)}")
    
    logger.debug(f"Cleaned equation: {equation}")
    return equation

@app.route('/')
def index():
    return render_template('signu-graph.html')

@app.route('/plot', methods=['POST'])
def plot():
    try:
        logger.debug("Received plot request")
        data = request.get_json()
        logger.debug(f"Received data: {data}")

        # Get and validate equation
        raw_equation = data['equation']
        logger.debug(f"Raw equation received: {raw_equation}")
        
        try:
            equation = validate_equation(raw_equation)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
            
        mode = data['mode']
        x_min = float(data['xMin'])
        x_max = float(data['xMax'])
        y_min = float(data['yMin']) if data['yMin'] is not None else None
        y_max = float(data['yMax']) if data['yMax'] is not None else None

        logger.debug(f"Processed equation: {equation}")
        logger.debug(f"Parameters: mode={mode}, x_min={x_min}, x_max={x_max}")

        # Define allowed mathematical functions
        allowed_functions = {
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'exp': lambda x: np.exp(np.clip(x, -100, 100)),
            'log': np.log,
            'sqrt': np.sqrt,
            'pi': np.pi,
            'abs': np.abs
        }

        # Generate x values
        x_values = np.linspace(x_min, x_max, 500)
        
        # Replace 'x' with 'x_values' in the equation
        modified_equation = equation.replace('x', 'x_values')
        logger.debug(f"Modified equation for evaluation: {modified_equation}")
        
        # Add x_values to the evaluation namespace
        eval_namespace = {
            "__builtins__": None,
            "x_values": x_values,
            **allowed_functions
        }

        # Evaluate the equation
        try:
            y_values = eval(modified_equation, eval_namespace)
        except Exception as e:
            logger.error(f"Evaluation error: {str(e)}")
            raise ValueError(f"Error evaluating equation: {equation}. Please check the syntax.")

        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(x_values, y_values, label=f'Equation: {equation}', color='b')
        
        ax.set_title('Generated Signal Plot', fontsize=14)
        ax.set_xlabel('x-axis', fontsize=12)
        ax.set_ylabel('y-axis', fontsize=12)
        
        if y_min is not None:
            ax.set_ylim(bottom=y_min)
        if y_max is not None:
            ax.set_ylim(top=y_max)
        
        ax.legend()
        
        # Convert to image
        img_io = BytesIO()
        fig.savefig(img_io, format='png', bbox_inches='tight', dpi=100)
        img_io.seek(0)
        
        plt.close(fig)
        
        # Convert to base64
        import base64
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
        return jsonify({'plot_image': img_base64})

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)