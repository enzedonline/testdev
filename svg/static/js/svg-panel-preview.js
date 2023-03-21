let svgTextField, svgFile, svgPreview, svgMsg

const renderSvgPanelPreview = (svg) => {
    if (svg.includes('<script')) {
        svgPreview.removeAttribute("class");
        svgPreview.innerHTML='<p class="error-message">' + svgMsg.noScript + '</p>';
    } else if (svg.includes('<svg') && svg.includes('</svg>')) {
        svgPreview.innerHTML=svg;
        svg_tag = svgPreview.getElementsByTagName('svg')[0];
        if (!svg_tag.hasAttribute('viewBox')) {
            svgPreview.removeAttribute("class");
            svgPreview.innerHTML='<p class="error-message">' + svgMsg.noViewbox + '</p>';
        } else {
            svgPreview.setAttribute("class", "svg-preview");
            svg_tag.removeAttribute('height');
            svg_tag.removeAttribute('width');                           
        }
    } else {
        svgPreview.removeAttribute("class");
        svgPreview.innerHTML='<p>' + svgMsg.pleaseEnter + '</p>';
    }
}

const readFile = (source, target) => {
    const reader = new FileReader();
    reader.addEventListener('load', (event) => {
        target.value = event.target.result;
        renderSvgPanelPreview(event.target.result); 
        target.style.height = target.scrollHeight 
            + parseFloat(getComputedStyle(target).paddingTop) 
            + parseFloat(getComputedStyle(target).paddingBottom) + 'px';
    });
    reader.readAsText(source);
}
const initialiseSvgPanel = () => {
    window.addEventListener('DOMContentLoaded', (event) => {
        const svgFieldNameElement = document.getElementById("svg_field_name")
        if (svgFieldNameElement) {
            const fieldName = JSON.parse(svgFieldNameElement.textContent);
            const textfieldId = JSON.parse(document.getElementById("svg_textfield_id").textContent);
            svgMsg = JSON.parse(document.getElementById("svg_msg").textContent);
            svgTextField = document.getElementById(textfieldId);
            svgFile = document.getElementById(fieldName + 'File');
            svgPreview = document.getElementById(fieldName + '-svgPreview');
            svgTextField.style.fontFamily = 'monospace';
            svgTextField.style.fontSize = '0.8em';
            svgTextField.style.maxHeight = '25em';
            svgTextField.style.overflowY = 'auto';
            renderSvgPanelPreview(svgTextField.value);
            
            svgTextField.addEventListener("input", () => {
                renderSvgPanelPreview(svgTextField.value);
            });
            svgFile.addEventListener("change", (e) => {
                e.preventDefault(); 
                const input = svgFile.files[0]; 
                readFile(input, svgTextField);
                svgFile.value = '';
            });
            svgTextField.parentElement.addEventListener('dragover', (event) => {
                event.stopPropagation();
                event.preventDefault();
                event.dataTransfer.dropEffect = 'copy';
            });
            svgTextField.parentElement.addEventListener('drop', (event) => {
                event.stopPropagation();
                event.preventDefault();
                const input = event.dataTransfer.files[0];
                readFile(input, svgTextField)
            });
    
        };
    });
};