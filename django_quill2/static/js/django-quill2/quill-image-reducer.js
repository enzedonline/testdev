class ImageReducer {
    constructor(quill, options = {}) {
        this.quill = quill;
        this.jpeg_compression = options['jpeg_compression'] ?? 0.7;
        this.maxWidth = options['max_width'] ?? null;
        this.toast_label = options['toast_label'] ?? "Reduced";
        this.silent = options['silent'] ?? false;
        this.prompt = options['prompt'] ?? this.default_prompt();
        if (
            typeof this.jpeg_compression !== 'number' ||
            this.jpeg_compression <= 0 ||
            this.jpeg_compression > 1
        ) {
            console.warn(
                'Invalid jpeg_compression value. It should be a number > 0 and <= 1. Setting to default value of 0.7.'
            );
            this.jpeg_compression = 0.7;
        }
        const toolbar = this.quill.getModule('toolbar');
        if (toolbar) {
            toolbar.addHandler('image-reducer', this.reduceImages.bind(this));
            const button = toolbar.container.querySelector('button.ql-image-reducer');
            if (button) {
                button.innerHTML = this._icon();
            }
            this._toast_css();
        }
    }

    _icon() {
        return `
            <svg viewBox="0 0 24 24" class="ql-stroke ql-fill">
            <path 
                d="m 17.25,7.3125001 c 0.240624,0 0.4375,0.1968751 0.4375,0.4375 V 16.494531 L 17.550781,16.316796 13.83203,11.504297 c -0.123044,-0.161329 -0.317187,-0.254298 -0.51953,-0.254298 -0.202345,0 -0.39375,0.09297 -0.519532,0.254298 l -2.26953,2.936718 -0.833985,-1.167578 C 9.5664062,13.101171 9.3695312,13 9.15625,13 8.9429687,13 8.7460937,13.101171 8.6230468,13.276171 l -2.1875,3.062501 L 6.3125,16.508203 v -0.0081 -8.7499986 c 0,-0.240625 0.196875,-0.4375001 0.4375,-0.4375001 z M 6.75,6 C 5.7847656,6 5,6.7847658 5,7.7500001 V 16.499999 C 5,17.465234 5.7847656,18.25 6.75,18.25 h 10.5 c 0.965235,0 1.75,-0.784766 1.75,-1.750001 V 7.7500001 C 19,6.7847658 18.215235,6 17.25,6 Z m 2.1875,5.249999 a 1.3125001,1.3125001 0 1 0 0,-2.6249989 1.3125001,1.3125001 0 1 0 0,2.6249989 z" 
                style="stroke-width:0.0273438;" 
            />
            <g style="fill:currentColor;" transform="matrix(0.70438624,0,0,0.70439443,-2.717965,-0.84445189)">
                <path d="m 36.913763,26.519898 h -5.085406 c -0.610249,0 -1.017081,0.406832 -1.017081,1.017081 v 5.085405 c 0,0.610249 0.406832,1.017081 1.017081,1.017081 v 0 c 0.610249,0 1.017081,-0.406832 1.017081,-1.017081 V 28.55406 h 4.068325 c 0.610249,0 1.017081,-0.406832 1.017081,-1.017081 0,-0.610249 -0.406832,-1.017081 -1.017081,-1.017081 z" style="stroke-width:1.01708" />
                <path d="M 9.9611146,26.519898 H 4.8757093 c -0.6102487,0 -1.0170812,0.406832 -1.0170812,1.017081 0,0.610249 0.4068325,1.017081 1.0170812,1.017081 h 4.0683242 v 4.068324 c 0,0.610249 0.4068321,1.017081 1.0170811,1.017081 v 0 c 0.6102494,0 1.0170814,-0.406832 1.0170814,-1.017081 v -5.085405 c 0,-0.610249 -0.406832,-1.017081 -1.0170814,-1.017081 z" style="stroke-width:1.01708" />
                <path d="m 31.828357,9.7380604 h 5.085405 c 0.610249,0 1.017081,-0.4068324 1.017081,-1.017081 0,-0.6102487 -0.406832,-1.0170811 -1.017081,-1.0170811 H 32.845438 V 3.6355741 c 0,-0.6102487 -0.406832,-1.0170811 -1.017081,-1.0170811 -0.610249,0 -1.017081,0.4068324 -1.017081,1.0170811 v 5.0854053 c 0,0.6102486 0.406832,1.017081 1.017081,1.017081 z" style="stroke-width:1.01708" />
                <path d="m 9.9611145,2.618493 c -0.6102487,0 -1.0170811,0.4068324 -1.0170811,1.0170811 V 7.7038983 H 4.8757092 c -0.6102487,0 -1.0170811,0.4068324 -1.0170811,1.0170811 0,0.6102486 0.4068324,1.017081 1.0170811,1.017081 h 5.0854053 c 0.6102405,0 1.0170725,-0.4068324 1.0170725,-1.017081 V 3.6355741 c 0,-0.6102487 -0.406832,-1.0170811 -1.0170725,-1.0170811 z" style="stroke-width:1.01708" />
            </g>
            </svg>
        `;
    }

    _toast_css() {
        const style = document.createElement('style');
        const css = `
            .quill-toast {
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 10px 20px;
                background-color: #333;
                color: #fff;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                opacity: 1;
                transition: opacity 1s ease-out;
                z-index: 1000;
            }
            .quill-toast.fade-out {
                opacity: 0;
            }
        `;
        if (style.styleSheet) {
            style.styleSheet.cssText = css;
        } else {
            style.appendChild(document.createTextNode(css));
        }
        document.head.appendChild(style);
    }

    async reduceImages() {
        const payloadSizeInitial = new TextEncoder().encode(this.quill.container.outerHTML).length;
        const imageElements = Array.from(this.quill.root.querySelectorAll('img'));
        const resizePromises = imageElements.map(img => new Promise((resolve, reject) => {
            if (img.src.startsWith('data:image') && img.hasAttribute('width')) {
                const [width, height] = this.parseDimensions(img);
                if (width != null && (width < img.naturalWidth)) { // only resize if width set & is smaller than image natural width
                    // Create a new image element
                    const newImg = new Image();
                    newImg.src = img.src;
                    // Once the image has loaded, resize it
                    newImg.onload = () => {
                        // Create a canvas element
                        const canvas = document.createElement('canvas');
                        canvas.width = width;
                        canvas.height = height;
                        // Draw the image onto the canvas
                        const ctx = canvas.getContext('2d');
                        ctx.drawImage(newImg, 0, 0, width, height);
                        // Get the resized image data URL in JPEG format with a quality of this.jpeg_compression
                        const resizedDataUrl = canvas.toDataURL('image/jpeg', this.jpeg_compression);
                        // Convert data URLs to byte length
                        const originalSize = new TextEncoder().encode(img.src).length;
                        const resizedSize = new TextEncoder().encode(resizedDataUrl).length;
                        // Check if the resized image is smaller than the original
                        if (resizedSize < originalSize) {
                            // Set the resized image data URL to the original image
                            img.src = resizedDataUrl;
                            // Remove the width and height attributes
                            img.removeAttribute('width');
                            img.removeAttribute('height');
                        }
                        resolve();
                    };
                    newImg.onerror = (error) => {
                        console.error('Image loading failed:', error);
                        reject(error);
                    };
                } else {
                    resolve(); // no resizing needed
                };
            } else {
                resolve(); // image resizing not applicable
            }
        }));

        // Wait for all image resizing to complete
        await Promise.all(resizePromises);

        // Calculate the resulting payload size difference, show result in toast message
        const payloadSizeResult = new TextEncoder().encode(this.quill.container.outerHTML).length;
        const diffKB = new Intl.NumberFormat().format(Math.trunc((payloadSizeInitial - payloadSizeResult) / 1024));
        this.showToast(`${this.toast_label} ${diffKB}KB`);
    }

    parseDimensions(img) {
        let width = img.getAttribute('width');
        if (typeof width === 'number' 
            || (typeof width === 'string' && width === String(parseFloat(width))) 
            || width.toLowerCase().endsWith('px')) {
            width = parseFloat(width);
        } else if (width.endsWith('%')) {
            width = parseFloat(this.maxWidth); // if no max_width set, this is null, resize will be skipped for relative sized images
        } else if (width.toLowerCase().endsWith('em') || width.toLowerCase().endsWith('rem')) {
            width = parseFloat(width) * 16; // assume 16px per unit
        } else {
            // unknown width attribute, return null to skip resizing
            return [null, null];
        };
        let height = img.getAttribute('height');
        if (height === parseFloat(height) || height.toLowerCase().endsWith('px')) {
            height = parseFloat(height);
        } else if (height.toLowerCase().endsWith('em') || height.toLowerCase().endsWith('rem')) {
            height = parseFloat(height) * 16; // assume 16px per unit
        } else {
            // use aspect ratio
            height = width / (img.naturalWidth / img.naturalHeight);
        };
        return [width, height];
    }

    showToast = message => {
        const toast = document.createElement('div');
        toast.className = 'quill-toast';
        toast.textContent = message;
        document.body.appendChild(toast);
        setTimeout(() => {
            toast.classList.add('fade-out');
            toast.addEventListener('transitionend', () => {
                toast.remove();
            })
        }, 2000);
    }

    default_prompt = ```
        This will compress all resized embedded images to their new size.<br>
        This process cannot be undone.
    ```;
    more_info = ```
        You can reduce the file size and save disk space by compressing pictures. The compression reduces both the file size and picture dimensions based on their width setting.<br>
        Images with an absolute width will be compressed if that width is smaller than the natural width of the image.<br>
        Images with a relative width ${this.maxWidth ? `will be reduced to ${this.maxWidth}px if larger.` : 'will not be reduced.'}.<br>
        This process only affects embedded images and is not applied to linked external images.
    ```;
}
