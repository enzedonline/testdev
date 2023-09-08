// js/flex-card-block.js

class FlexCardBlockDefinition extends window.wagtailStreamField.blocks
    .StructBlockDefinition {
    render(placeholder, prefix, initialState, initialError) {
        const block = super.render(
            placeholder,
            prefix,
            initialState,
            initialError,
        );
        const structBlock = block.container[0];
        const imageInput = structBlock.querySelector(`#${prefix}-image-image`);
        const layoutInput = structBlock.querySelector(`#${prefix}-layout`);
        const imageMinSection = structBlock.querySelector('[data-contentpath="image_min"]');
        const imageMaxSection = structBlock.querySelector('[data-contentpath="image_max"]');
        const layoutSection = structBlock.querySelector('[data-contentpath="layout"]');
        const breakpointSection = structBlock.querySelector('[data-contentpath="breakpoint"]');
        structBlock.imageDepependentElements = [imageInput, imageMaxSection, imageMinSection, layoutSection, breakpointSection];
        structBlock.imageDepependentElements.forEach(element => {
            element.style.marginInlineStart = "1em";
        })

        const showHideBreakpoint = () => {
            breakpointSection.style.display = layoutSection.style.display === 'block' && layoutInput.value.endsWith('-responsive') ? "block" : "none";
        }
        layoutInput.addEventListener("change", showHideBreakpoint);

        const showHideImageElements = () => {
            structBlock.imageDepependentElements.forEach(element => {
                element.style.display = imageInput.value.trim() === "" ? "none" : "block";
            })
            showHideBreakpoint();
        }
        imageInput.addEventListener("change", showHideImageElements);
        showHideImageElements();


        return block;
    }
}

window.telepath.register('blocks.models.FlexCardBlock', FlexCardBlockDefinition);
