const getClassFromString = (className) => {
    const ClassObj = window[className] || eval(className);
    return typeof ClassObj === 'function' ? ClassObj : undefined;
};

const registerWithQuill = (path, module) => {
    try {
        const registerClass = typeof module === 'string' ? getClassFromString(module) : module;
        Quill.register(path, registerClass);
    } catch (error) {
        console.error(`Quill failed to register (${path}, ${module}):`, error);
    }
};

registerWithQuill("modules/imageCompressor", "imageCompressor");
registerWithQuill("modules/image-reducer", "ImageReducer");
registerWithQuill('modules/blotFormatter2', 'QuillBlotFormatter2.default');
registerWithQuill('modules/better-table-plus', "quillBetterTablePlus");
registerWithQuill("modules/insert-better-table-plus", "InsertBetterTablePlus");
