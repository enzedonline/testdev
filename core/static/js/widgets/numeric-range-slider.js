class NumericRangeSlider {
    constructor(id) {
        this.inputElement = document.getElementById(`${id}`)
        this.getSliderValues();
        this.addSlider();
        window.test = this;
    }
    
    getSliderValues() {
        this.settings = { ...this.inputElement.dataset };
        this.settings.min = parseFloat(this.settings.minValue);
        this.settings.max = parseFloat(this.settings.maxValue);
        this.settings.step = parseFloat(this.settings.step);
        this.settings.pipCount = parseInt(this.settings.pipCount);
        this.settings.pipDecimals = parseInt(this.settings.pipDecimals);
        this.settings.density = parseInt(this.settings.minorTickDensity);
        this.settings.verticalLabels = JSON.parse(this.settings.verticalLabels)

        this.sliderElement = this.inputElement.parentElement.appendChild(document.createElement('div'));
        this.sliderElement.classList = `numeric-range-slider${this.settings.verticalLabels ? ' vertical-labels' : ''}`;

        const initialValue = this.inputElement.value
        if (!(Array.isArray(initialValue) && initialValue.length === 0)) {
            let parsingError = false, errorMessage;
            try {
                [this.lower, this.upper] = JSON.parse(initialValue).map(parseFloat);
                if (isNaN(this.lower)) { this.lower = this.settings.min; parsingError = true; };
                if (isNaN(this.upper) || this.upper === undefined) { this.upper = this.settings.max; parsingError = true; };
            } catch (error) {
                parsingError = true;
            }
            if (parsingError) {
                errorMessage = ("There was an error reading the range values from the database.")
            } else {
                if (this.lower < this.settings.min || this.upper > this.settings.max) {
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
            this.lower = this.settings.min;
            this.upper = this.settings.max;
        }

        // Calculate pip value array. Ensure the last value is exactly 100 to handle rounding errors
        this.settings.pipValues = [];
        for (let i = 0; i < this.settings.pipCount - 1; i++) {
            this.settings.pipValues.push((100 * i) / (this.settings.pipCount - 1));
        }
        this.settings.pipValues.push(100);

    }

    setInputValue() {
        this.inputElement.value = `[${this.sliderElement.noUiSlider.get()}]`;
    }

    addSlider(callback) {
        noUiSlider.create(this.sliderElement, {
            start: [this.lower, this.upper],
            step: this.settings.step,
            connect: true,
            tooltips: wNumb({
                decimals: this.settings.pipDecimals,
                prefix: this.settings.pipPrefix,
                suffix: this.settings.unit
            }),
            range: {
                'min': [this.settings.min],
                'max': [this.settings.max]
            },
            pips: {
                mode: 'positions',
                values: this.settings.pipValues,
                density: this.settings.density,
                stepped: true,
                format: wNumb({
                    decimals: this.settings.pipDecimals,
                    prefix: this.settings.pipPrefix,
                    suffix: this.settings.unit
                })
            }
        });
        this.sliderElement.parentElement.style.height = `${this.sliderElement.scrollHeight}px`;
        this.sliderElement.noUiSlider.on('set', () => { this.setInputValue() })
    }

}


