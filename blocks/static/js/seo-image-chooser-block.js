// js/seo-image-block.js

class SEOImageChooserBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );
        const structBlock = block.container[0];
        const imageInput = structBlock.querySelector(`#${prefix}-image`);
        const seoTitleSection = structBlock.querySelector('[data-contentpath="seo_title"]');
        const seoTitleLabel = seoTitleSection.querySelector("label.w-field__label");

        const requiredMark = document.createElement('span');
        requiredMark.innerText = "*";
        requiredMark.className = "w-required-mark";
        seoTitleLabel.appendChild(requiredMark)

        const updateDisplay = () => {
            seoTitleSection.style.display = imageInput.value.trim() === "" ? "none" : "block";
        };

        imageInput.addEventListener("change", updateDisplay);
        updateDisplay();

        return block;
    }
}

window.telepath.register('blocks.models.SEOImageChooserBlock', SEOImageChooserBlockDefinition);
