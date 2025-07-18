class QuillWrapper {
    constructor(id, options, tooltips, labels, buttonIcons) {
        this.options = options.quillOptions;
        window.qw = this;
        this.registerComponents(options.quillRegister)
        // add keyboard bindings to window.QuillKeyboardBindings prior to loading this module
        // see ./quill-register.js for example
        this.options.modules.keyboard = this.options.modules.keyboard || {};
        this.options.modules.keyboard.bindings = this.options.modules.keyboard.bindings || {};
        // this.options.modules.keyboard.bindings = {
        //     ...this.options.modules.keyboard.bindings,
        //     ...window.QuillKeyboardBindings || {}
        // };
        // register linebreak (br) and divider (hr) if included in options
        this.registerDivider();
        this.registerLineBreak();
        this.registerCodeBlockFix();
        // create Quill instance
        this.targetDiv = document.getElementById(`quill-${id}`);
        if (!this.targetDiv) throw 'Target div(' + `quill-${id}` + ') id was invalid';
        this.targetInput = document.getElementById(`quill-input-${id}`);
        if (!this.targetInput) throw 'Target Input id was invalid';
        this.quill = new Quill(`#quill-${id}`, this.options);
        if (this.targetInput.value) {
            const parsedInput = JSON.parse(this.targetInput.value);
            const delta = JSON.parse(parsedInput.delta);
            this.quill.setContents(delta);
        }
        window.quill = this.quill;

        // toolbar config
        this.toolbarContainer = this.targetDiv.parentElement.querySelector('div[role="toolbar"]');
        if (this.toolbarContainer) {
            this.addTooltips(tooltips);
            this.replaceLabels(labels);
            this.replaceButtonIcons(buttonIcons);
        }
        // paste smart
        if (!!QuillPasteSmart) {
            this.configurePasteSmart();
        }
        // write changes to hidden input on text-change
        // Note that QuillField.clean() will further process the thml value on save
        this.quill.on('text-change', () => {
            const delta = JSON.stringify(this.quill.getContents());
            this.targetInput.value = JSON.stringify({ delta: delta, html: this.quill.getSemanticHTML() });
        });

        // form submit event handler
        // this.onSubmit = this.onSubmit.bind(this);
        // this.form = this.targetInput.closest('form');
        // this.form?.addEventListener('submit', this.onSubmit)

    }

    onSubmit(event) {
        event.preventDefault();
        // ensure any lingering changes have been updated
        // this.quill.emitter.emit(
        //     this.quill.constructor.events.TEXT_CHANGE, 0, this.quill.getLength(), 'api'
        // );
        this.form.submit();
    }

    registerComponents(registerList) {
        registerList.map(([path, module]) => {
            try {
                const registerClass = typeof module === 'string' ? this.getClassFromString(module) : module;
                Quill.register(path, registerClass);
            } catch (error) {
                console.error(`Quill failed to register (${path}, ${module}):`, error);
            };
        });
    }

    addKeyboardBindings(bindingsList) {
        this.options.modules.keyboard = this.options.modules.keyboard || {};
        bindings = {}
        bindingsList.forEach((binding) => {
            bindings = {
                ...this.options.modules.keyboard.bindings,
                ...window.QuillKeyboardBindings || {}
            };

        })
    }

    // set titles on toolbar buttons - multilang support 
    addTooltips(tooltips) {
        if (tooltips) {
            tooltips.map(([selector, tooltip]) => {
                try {
                    this.toolbarContainer.querySelectorAll(selector).forEach(element => {
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
        if (labels) {
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

    configurePasteSmart() {
        this.clipboard = this.quill.getModule('clipboard');
        // handle quill-paste-smart image file paste when imageCompressor loaded 
        if (typeof imageCompressor !== 'undefined' && !('handleImagePaste' in this.quill.options.modules.clipboard)) {
            // handle image file pasting here if quill-image-compress loaded
            // this does not affect pasting html images
            this.imageCompressor = this.quill.getModule('imageCompressor');
            this.clipboard.handleImagePaste = (image) => {
                const reader = new FileReader();
                reader.onload = async (e) => {
                    const dataUrl = await this.imageCompressor.downscaleImageFromUrl(e.target.result);
                    const range = this.quill.getSelection();
                    this.quill.insertEmbed(range.index, 'image', dataUrl ? dataUrl : e.target.result);
                }
                reader.readAsDataURL(image);
            }
        }

        this.clipboard.hooks = this.clipboard.hooks || {};
        // strip empty paragraph tags if removeEmptyLines set to true in options
        if (this.quill.options.modules.clipboard.removeEmptyLines) {
            this.clipboard.hooks = {
                ...this.clipboard.hooks,
                ...{
                    uponSanitizeElement(node) {
                        {
                            if (node.tagName === 'P' && !node.hasChildNodes() && !node.textContent) {
                                node.remove();
                            }
                        }
                    },
                }
            };
        }

    }

    // set button icons listed in settings
    replaceButtonIcons(buttonIcons) {
        if (buttonIcons) {
            buttonIcons.map(([selector, svg]) => {
                try {
                    this.toolbarContainer.querySelectorAll(selector).forEach(element => {
                        element.innerHTML = svg;
                    });
                } catch (error) {
                    console.warn(`Quill ButtonIcons - Invalid selector: ${selector}. Error: ${error.message}`);
                }
            });
        }
    }

    // If 'divider' included in toolber, create blot type and register toolbar handler
    registerDivider() {
        const hasDivider = this.options.modules?.toolbar?.container.some(itemArray => itemArray[0] === 'divider');
        if (hasDivider) {
            const BlockEmbed = Quill.import('blots/block/embed');
            class DividerBlot extends BlockEmbed {
                static blotName = 'divider';
                static tagName = 'hr';
            }
            Quill.register(DividerBlot);
            this.options.modules.toolbar.handlers.divider = (value) => {
                const selection = this.quill.getSelection(focus = true);
                let position = 0;
                // divider will replace any selected text
                if (!!selection.length) {
                    this.quill.deleteText(selection);
                }
                // if last position in editor, add newline after divider (caret will not be after hr otherwise)
                if (selection.index === this.quill.getLength() - 1) {
                    this.quill.insertText(selection.index, '\n')
                }
                // if at end of block, insert divider after newline character (quill will add a newline after divider otherwise)
                if (JSON.stringify(this.quill.getContents(selection.index, 1)) == JSON.stringify({ ops: [{ insert: "\n" }] })) {
                    position = selection.index + 1;
                } else {
                    position = selection.index;
                }
                this.quill.insertEmbed(position, 'divider', true);
                // move selection after divider
                this.quill.setSelection(selection.index + 2);
            }

        }
    }

    // If 'linbreak' included in toolbar, create blot type, register toolbar and keyboard shortcut handler
    registerLineBreak() {
        const hasLineBreak = this.options.modules?.toolbar?.container.some(childArray => childArray.includes('linebreak'));
        if (hasLineBreak) {
            const InlineEmbed = Quill.import('blots/embed');
            class LineBreakBlot extends InlineEmbed {
                static blotName = 'linebreak';
                static tagName = 'br';
            }
            Quill.register(LineBreakBlot);
            this.linebreakHandler = () => {
                const selection = this.quill.getSelection(focus = true);
                // br will replace any selected text
                if (!!selection.length) {
                    this.quill.deleteText(selection);
                }
                // Quill will not handle <br> at end of block - insert space after <br> if next char is newline char
                if (JSON.stringify(this.quill.getContents(selection.index, 1)) == JSON.stringify({ ops: [{ insert: "\n" }] })) {
                    this.quill.insertText(selection.index, ' ');
                }
                this.quill.insertEmbed(selection.index, 'linebreak', true);
                // move selection after linebreak
                this.quill.setSelection(selection.index + 1);
            }
            this.options.modules.toolbar.handlers.linebreak = this.linebreakHandler
            this.options.modules.keyboard.bindings.linebreak = {
                key: 'Enter',
                shiftKey: true,
                handler: this.linebreakHandler
            }
        }
    }

    registerCodeBlockFix() {
        if (QuillSyntaxCodeBlockContainer.default) {
            Quill.register('formats/code-block-container', QuillSyntaxCodeBlockContainer.default, true);
        }
    }

    getClassFromString(className) {
        const ClassObj = window[className] || eval(className);
        return typeof ClassObj === 'function' ? ClassObj : undefined;
    };
}