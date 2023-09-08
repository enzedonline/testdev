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
  let script_tag = document.getElementById(`${id}`)
  if (!script_tag) {
    let target_tag = document.getElementsByTagName("head")[0];
    let script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = `${js}`;
    script.id = `${id}`;
    target_tag.appendChild(script);
    if (document.getElementById(`${id}`)) {
      return script;
    }
    else {
      return null;
    } 
  }
  else {
    return script_tag;
  }
}

// include css only if not already included
const include_css = (css, id) => {
  let link_tag = document.getElementById(`${id}`)
  if (!link_tag) {
    let target_tag = document.getElementsByTagName("head")[0];
    let link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = `${css}`;
    link.id = `${id}`;
    target_tag.appendChild(link);
    if (document.getElementById(`${id}`)) {
      return link;
    }
    else {
      return null;
    } 
  }
  else {
    return link_tag;
  }
}

