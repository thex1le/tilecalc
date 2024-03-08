from flask import Flask, render_template, request, session, redirect, url_for
import math
from fractions import Fraction
app = Flask(__name__)
app.secret_key = 'UsingMyRoseLove2SignTheSecretKey'


# Conversion constants
METERS_TO_FEET = 3.28084
MM_TO_INCHES = 1 / 25.4  # 1 inch = 25.4 mm

def convert_to_feet(value, unit):
    """Converts the value to feet if it's in inches."""
    if unit == 'inches':
        return value / 12
    return value

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST' and 'clear' in request.form:
        # Clear session and redirect to refresh the page
        session.clear()
        return redirect(url_for('home'))

    conversion_result = None
    conversion_type = None

    if request.method == 'POST':
        # Handle meter to feet conversion
        if 'convert_meters' in request.form:
            meters = float(request.form.get('meters', 0))
            conversion_result = meters * METERS_TO_FEET
            conversion_type = 'meters_to_feet'
            session['meters'] = meters
        # Handle mm to inches conversion
        elif 'convert_mm' in request.form:
            mm = float(request.form.get('mm', 0))
            conversion_result = mm * MM_TO_INCHES
            conversion_type = 'mm_to_inches'
            session['mm'] = mm
        # Handle decimal to fraction conversion
        elif 'convert_decimal' in request.form:
            decimal = float(request.form.get('decimal', 0))
            conversion_result = str(Fraction(decimal).limit_denominator())
            conversion_type = 'decimal_to_fraction'
            session['decimal'] = decimal
        # Handle fraction to decimal conversion
        elif 'convert_fraction' in request.form:
            fraction_input = request.form.get('fraction', '0')
            try:
                conversion_result = float(sum(Fraction(s) for s in fraction_input.split()))
                conversion_type = 'fraction_to_decimal'
                session['fraction'] = fraction_input
            except ValueError:
                conversion_result = "Invalid fraction"

        session['conversion_result'] = conversion_result
        session['conversion_type'] = conversion_type
        
        if 'calc_tile_boxes' in request.form:
            print(request.form)
            tile_sq_ft = float(request.form.get('tileSqft', 1))
            room_sqft = float(request.form.get('roomSqft', 1))
            cost_sqft = float(request.form.get('costSqft', 0))
            # note we round up to the next whole box since you cant sell half boxes
            
            cost_per_box = tile_sq_ft * cost_sqft
            boxes_needed = room_sqft / tile_sq_ft
            boxes_needed_rounded = math.ceil(boxes_needed)
            print(boxes_needed)
            boxes_need_w_waste = math.ceil(boxes_needed + (boxes_needed * .1))
            print(boxes_needed + (boxes_needed * .1))
            print(boxes_need_w_waste)
            total_cost = boxes_needed_rounded * cost_per_box
            total_cost_w_waste = boxes_need_w_waste * cost_per_box
            # Save the inputs, units, and the result in session
            session['conversion_type'] = 'tile_boxes'
            session['boxes_required'] = boxes_needed_rounded
            session['boxes_required_waste'] = boxes_need_w_waste
            session['total_cost'] = round(total_cost, 3)
            session['total_cost_w_waste'] = round(total_cost_w_waste, 3)
            session['cost_per_sqft'] = cost_sqft
            session['tile_square_footage'] = tile_sq_ft
            print(total_cost_w_waste)

        if 'tile_calc_sq_foot' in request.form:
            length = float(request.form.get('length', 0))
            length_unit = request.form.get('length_unit')
            width = float(request.form.get('width', 0))
            width_unit = request.form.get('width_unit')

            # Convert both to feet for the calculation
            length_in_feet = convert_to_feet(length, length_unit)
            width_in_feet = convert_to_feet(width, width_unit)

            square_footage = length_in_feet * width_in_feet
            # Save the inputs, units, and the result in session
            session['tile_length'] = length
            session['tile_length_unit'] = length_unit
            session['tile_width'] = width
            session['tile_width_unit'] = width_unit
            session['tile_square_footage'] = square_footage
            session['conversion_type'] = 'tile_square_footage'

        elif 'calc_sq_foot' in request.form:
            length = float(request.form.get('length', 0))
            length_unit = request.form.get('length_unit')
            width = float(request.form.get('width', 0))
            width_unit = request.form.get('width_unit')

            # Convert both to feet for the calculation
            length_in_feet = convert_to_feet(length, length_unit)
            width_in_feet = convert_to_feet(width, width_unit)

            square_footage = length_in_feet * width_in_feet
            # Save the inputs, units, and the result in session
            session['length'] = length
            session['length_unit'] = length_unit
            session['width'] = width
            session['width_unit'] = width_unit
            session['square_footage'] = square_footage
            session['conversion_type'] = 'square_footage'

    return render_template('index.html', conversion_result=conversion_result, conversion_type=conversion_type)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
