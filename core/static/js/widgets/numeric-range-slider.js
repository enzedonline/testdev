class NumericRangeSlider {
    constructor(id, options) {
        this.inputElement = document.getElementById(`${id}`);
        if (!this.inputElement) {
            throw new Error(`Element with id "${id}" not found`);
        }
        if (!options || typeof options !== 'object') {
            throw new Error('Options object is required');
        }
        this.getSliderOptions(options);
        this.addSlider();
    }

    getSliderOptions(options) {
        // Parse options from the Django template
        this.options = {};
        this.options.min = parseFloat(options.minValue);
        this.options.max = parseFloat(options.maxValue);
        this.options.step = parseFloat(options.step);
        this.options.unit = options.unit;
        this.options.prefix = options.prefix;
        this.options.decimalPlaces = parseInt(options.decimalPlaces);
        this.options.majorIntervals = parseInt(options.majorIntervals);
        this.options.minorIntervals = parseInt(options.minorIntervals);
        this.options.verticalLabels = JSON.parse(options.verticalLabels)

        const initialValue = this.inputElement.value
        if (!(Array.isArray(initialValue) && initialValue.length === 0)) {
            let parsingError = false, errorMessage;
            try {
                const parsed = JSON.parse(initialValue).map(parseFloat);
                if (!(Array.isArray(parsed) && parsed.length === 2)) {
                    throw new Error('Invalid range format: expected array of length 2');
                }
                [this.lower, this.upper] = parsed;
                if (isNaN(this.lower)) { this.lower = this.options.min; parsingError = true; };
                if (isNaN(this.upper) || this.upper === undefined) { this.upper = this.options.max; parsingError = true; };
            } catch (error) {
                parsingError = true;
            }
            if (parsingError) {
                errorMessage = ("There was an error reading the range values from the database.")
            } else {
                if (this.lower < this.options.min || this.upper > this.options.max) {
                    errorMessage = (`The stored value ${this.inputElement.value} is outside of the bounds of the range limit.`)
                }
            }
            if (errorMessage) {
                const errorLabel = this.inputElement.parentElement.insertBefore(
                    document.createElement('p'), this.inputElement.parentElement.firstChild
                );
                errorLabel.className = "numeric-range-slider-db-value-error error-message";
                errorLabel.innerText = errorMessage
            }
        } else {
            this.lower = this.options.min;
            this.upper = this.options.max;
        }

        // Calculate pip value array. Ensure the last value is exactly 100 to handle rounding errors
        this.options.pipValues = new Array(this.options.majorIntervals + 1);
        for (let i = 0; i < this.options.majorIntervals; i++) {
            this.options.pipValues.push((100 * i) / (this.options.majorIntervals));
        }
        this.options.pipValues.push(100);
        // Calculate minor tick density based on the number of major & minor intervals to ensure the pips are evenly spaced
        this.options.density = 100 / (this.options.majorIntervals * this.options.minorIntervals);

    }

    setInputValue() {
        this.inputElement.value = `[${this.sliderElement.noUiSlider.get()}]`;
    }

    addSlider(callback) {
        this.sliderWrapper = this.inputElement.parentElement.insertAdjacentElement('afterend', document.createElement('div'));
        this.sliderElement = this.sliderWrapper.appendChild(document.createElement('div'));
        this.sliderElement.classList = `numeric-range-slider${this.options.verticalLabels ? ' vertical-labels' : ''}`;

        noUiSlider.create(this.sliderElement, {
            start: [this.lower, this.upper],
            step: this.options.step,
            connect: true,
            tooltips: wNumb({
                decimals: this.options.decimalPlaces,
                prefix: this.options.prefix,
                suffix: this.options.unit
            }),
            range: {
                'min': [this.options.min],
                'max': [this.options.max]
            },
            pips: {
                mode: 'positions',
                values: this.options.pipValues,
                density: this.options.density,
                stepped: true,
                format: wNumb({
                    decimals: this.options.decimalPlaces,
                    prefix: this.options.prefix,
                    suffix: this.options.unit
                })
            }
        });
        // Set the height of the slider wrapper to the height of the slider including the pips & labels
        this.sliderWrapper.style.height = `${this.sliderElement.scrollHeight}px`;
        // update input value on slider change
        this.sliderElement.noUiSlider.on('set', () => this.setInputValue());
    }

}


