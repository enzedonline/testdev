$(document).ready(() => {
  const newTabElement = document.querySelector('[data-preview-new-tab]');
  const pagePreview = document.querySelector('[data-tippy-content="Preview"]');
  
  if (newTabElement && pagePreview) {
    const clonedNewTabElement = newTabElement.cloneNode(true);
    clonedNewTabElement.setAttribute("custom-tooltip", ""); 
    pagePreview.insertAdjacentElement('afterend', clonedNewTabElement);
  }
});

// wait for an object to load, pass back resolved object
const waitForObject = async (object) => {
  const resolvedObject = await Promise.resolve(object);
  if (!resolvedObject) {
    return new Promise((resolve) => {
      window.addEventListener('load', () => {
        resolve(resolvedObject);
      });
    });
  }
  return resolvedObject;
};

// include js script only if not already included
const include_js = (js, id) => {
  return new Promise((resolve, reject) => {
    let script_tag = document.getElementById(id);

    if (!script_tag) {
      const head = document.head || document.getElementsByTagName('head')[0];
      script_tag = document.createElement('script');
      script_tag.type = 'text/javascript';
      script_tag.src = js;
      script_tag.id = id;
      script_tag.onload = resolve; // Resolve the promise when script is loaded
      script_tag.onerror = reject; // Reject the promise on error
      head.appendChild(script_tag);
    } else {
      resolve(); // Resolve the promise if script is already loaded
    }
  });
};

// include css only if not already included
const include_css = (css, id) => {
  let link_tag = document.getElementById(`${id}`)
  if (!link_tag) {
    const head = document.head || document.getElementsByTagName('head')[0];
    let link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `${css}`;
    link.id = `${id}`;
    head.appendChild(link);
  }
}

