class QuillWrapper {
    constructor(targetDivId, targetInputId, quillOptions, tooltips, labels) {
        this.targetDiv = document.getElementById(targetDivId);
        if (!this.targetDiv) throw 'Target div(' + targetDivId + ') id was invalid';
        this.targetInput = document.getElementById(targetInputId);
        if (!this.targetInput) throw 'Target Input id was invalid';
        this.quill = new Quill('#' + targetDivId, quillOptions);
        window.quill = this.quill;
        this.qlEditor = this.targetDiv.querySelector('div.ql-editor');
        this.toolbar = this.targetDiv.parentElement.querySelector('div[role="toolbar"]')
        this.setClearFormattingIcon();
        this.addTooltips(tooltips);
        this.replaceLabels(labels);
        this.quill.on('text-change', () => {
            const delta = JSON.stringify(this.quill.getContents());
            // const htmlClone = this.qlEditor.cloneNode(true);
            // this.targetInput.value = JSON.stringify({ delta: delta, html: htmlClone.innerHTML });
            // once getSemanticHTML() supports iframes, replace previous two lines with:
            this.targetInput.value = JSON.stringify({ delta: delta, html: this.quill.getSemanticHTML() });
        });
    }

    // add title attributes to toolbar buttons
    addTooltips(tooltips) {
        if (this.toolbar) {
            tooltips.forEach(([selector, tooltip]) => {
                try {
                    this.toolbar.querySelectorAll(selector).forEach(element => {
                        element.setAttribute('title', tooltip);
                    });
                } catch (error) {
                    console.warn(`Quill Tooltips - Invalid selector: ${selector}. Error: ${error.message}`);
                }
            });
        }
    }

    // set labels on toolbar items - multilang support for dropdown items such as font/heading size
    replaceLabels(labels) {
        if (this.toolbar) {
            try {
                const style = document.createElement('style');
                style.innerHTML = labels.map(([selector, label]) => {
                    return `${selector} { content: '${label}' !important; }`;
                }).join(' ');
                document.head.appendChild(style);
            } catch (error) {
                console.warn(`Quill Toolbar Labels - Error: ${error.message}`);
            }
        }
    }

    // replace default clear formats button icon
    setClearFormattingIcon() {
        if (this.toolbar) {
            try {
                const svg = `
                <svg viewBox="0 0 16 16" class="ql-stroke ql-fill">
                    <text xml:space="preserve" style="font-family:'Segoe UI';letter-spacing:-1.33px;display:inline;stroke:none;stroke-width:80;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:3.6;stroke-opacity:1">
                        <tspan x="-0.15" y="10.5""><tspan style="font-size:14px;letter-spacing:-1.33px;">A</tspan><tspan style="font-size:12px;letter-spacing:-1.33px;">b</tspan></tspan>
                    </text>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="m 11.55528,14.622154 c -0.227641,0.227692 -0.432256,0.432308 -0.620666,0.608615 h 4.680767 c 0.212411,0 0.384616,0.172205 0.384616,0.384616 C 15.999997,15.827795 15.827792,16 15.615381,16 H 9.4615373 C 9.4521285,16 9.4428029,15.999641 9.433569,15.999 9.0725938,15.985179 8.7663529,15.829179 8.4659633,15.6 8.1647378,15.370154 7.8284045,15.033846 7.4167636,14.622154 l -0.038948,-0.03893 C 6.9661638,14.17159 6.6298203,13.835282 6.3999999,13.534052 6.1597897,13.219179 6,12.897948 6,12.513948 6,12.13 6.1597897,11.808718 6.3999999,11.493898 6.6298255,11.192667 6.9661638,10.856359 7.3778149,10.444718 L 10.444717,7.3778154 C 10.856357,6.9661692 11.192665,6.6298205 11.493896,6.4 11.808717,6.1597897 12.129998,6 12.513946,6 c 0.384,0 0.705231,0.1597897 1.020104,0.4 0.301229,0.2298257 0.637537,0.5661641 1.049178,0.9778154 l 0.03893,0.038948 c 0.411692,0.411641 0.748,0.7479744 0.977846,1.0492 0.240205,0.3148359 0.4,0.6360974 0.4,1.020067 0,0.3839642 -0.159795,0.7052516 -0.4,1.0200726 -0.229795,0.30123 -0.566154,0.637538 -0.977795,1.049128 z M 10.969177,7.9412257 c 0.435898,-0.4359026 0.736052,-0.7348924 0.991333,-0.9296719 0.246412,-0.1880051 0.405283,-0.2423231 0.553436,-0.2423231 0.148154,0 0.307078,0.054318 0.553487,0.2423231 0.255283,0.1947795 0.555436,0.4937693 0.991333,0.9296719 0.435898,0.4359076 0.734924,0.7360512 0.929693,0.9913384 0.188,0.2464102 0.242307,0.4053126 0.242307,0.5534667 0,0.1481484 -0.0543,0.3070509 -0.242307,0.5534572 -0.194769,0.255281 -0.493795,0.555435 -0.929693,0.991333 l -2.150409,2.15041 -3.0895785,-3.08959 z M 9.4860294,15.230769 c 0.1481482,0 0.3070507,-0.05431 0.5534566,-0.242307 0.255282,-0.19477 0.555436,-0.493795 0.991333,-0.929693 L 11.36446,13.725128 8.2748505,10.635538 7.941225,10.969179 c -0.4359024,0.435898 -0.7348921,0.736052 -0.9296715,0.991334 -0.188005,0.24641 -0.242323,0.405282 -0.242323,0.553435 0,0.148155 0.054318,0.307078 0.242323,0.553488 0.1947794,0.255282 0.4937691,0.555436 0.9296715,0.991333 0.4359076,0.435898 0.736051,0.734924 0.9913381,0.929693 0.2464101,0.188 0.4053123,0.242307 0.5534663,0.242307 z" fill="#1c274c" style="stroke-width:0.512821;stroke:none;stroke-opacity:1;fill:#800080;fill-opacity:1" />
                    <path style="fill:#800080;fill-opacity:1;stroke:none;stroke-width:2.33151;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:3.6;stroke-opacity:1" d="M 12.490893,6.2895037 C 11.908309,6.311098 11.495224,6.7701604 11.108037,7.1485086 10.223446,8.0141312 9.3434654,8.8865775 8.4751728,9.7673361 8.2554765,10.002503 8.3518654,10.373754 8.5938102,10.553923 c 1.0085139,0.997504 1.9946268,2.019222 3.0219118,2.996851 0.253499,0.175199 0.587709,0.06359 0.763832,-0.167236 0.969605,-0.973445 1.964079,-1.924181 2.890198,-2.939606 0.332687,-0.344171 0.571111,-0.8604099 0.376309,-1.3328209 C 15.39051,8.5356629 14.888205,8.1236551 14.468457,7.6707587 14.013719,7.2374559 13.59871,6.73852 13.044911,6.4272541 12.873603,6.3410236 12.684182,6.2839769 12.490893,6.2895037 Z" />
                </svg>
                `;
                const clearButton = this.toolbar.querySelector('button.ql-clean');
                clearButton.innerHTML = svg;
            } catch (error) {
                console.warn(`Quill Toolbar Clear Formatting Icon Error: ${error.message} `);
            }
        }
    }
}