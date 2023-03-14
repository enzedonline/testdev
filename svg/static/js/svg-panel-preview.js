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
            renderSvgPanelPreview(svgTextField.value);
            svgTextField.addEventListener("input", () => {
                renderSvgPanelPreview(svgTextField.value);
            });
            svgFile.addEventListener("change", (e) => {
                e.preventDefault(); 
                const input = svgFile.files[0]; 
                const reader = new FileReader(); 
                reader.onload = function (e) {
                    svgTextField.value = e.target.result; 
                    renderSvgPanelPreview(e.target.result); 
                }; 
                reader.readAsText(input); 
            });
        };
    });
};