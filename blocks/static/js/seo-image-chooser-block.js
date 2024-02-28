// js/seo-image-chooser-block.js

class SEOImageChooserBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    // hide description field if required=False and no image selected
    // apply required mark to description as will always be required if shown

    render(placeholder, prefix, initialState, initialError) {
        // set description field required=true - only affects rendering
        this.childBlockDefs.find(obj => obj.name === 'description').meta.required = true;

        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );
        if (!this.required) {
            // StructBlock is optional, hide description section if no image value
            const structBlock = block.container[0];
            const imageInput = structBlock.querySelector(`#${prefix}-image`);
            const descriptionSection = structBlock.querySelector('[data-contentpath="description"]');
            const updateDisplay = () => {
                descriptionSection.style.display = imageInput.value.trim() === "" ? "none" : "block";
            };
            imageInput.addEventListener("change", updateDisplay);
            updateDisplay();
        }
        return block;
    }
}

window.telepath.register('blocks.seo_image_chooser.SEOImageChooserBlock', SEOImageChooserBlockDefinition);
