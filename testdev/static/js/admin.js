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
const include_js = (js, options={}) => {
  return new Promise((resolve, reject) => {
    let script_tag = document.querySelector(`script[src="${js}"]`);
    if (!script_tag) {
      const head = document.head || document.getElementsByTagName('head')[0];
      script_tag = document.createElement('script');
      script_tag.src = js;
      script_tag.type = options.type || 'text/javascript';
      if (options.integrity) script_tag.integrity = options.integrity;
      if (options.crossorigin) script_tag.crossOrigin = options.crossorigin;
      if (options.defer) script_tag.defer = true;
      if (options.async) script_tag.async = true;
      script_tag.onload = () => {
        script_tag.dataset.scriptLoaded = true; // Set attribute once loaded
        resolve();
      };
      script_tag.onerror = () => {
        console.error(`Failed to load script: ${js}`);
        reject(new Error(`Script load error: ${js}`));
      };
      head.appendChild(script_tag);
    } else {
      // Script tag exists, check if it's fully loaded
      if (script_tag.dataset.scriptLoaded === "true") {
        resolve();  // Script is already fully loaded, resolve immediately
      } else {
        // Script is still loading, add event listeners
        script_tag.addEventListener('load', resolve);
        script_tag.addEventListener('error', reject);
      }
    }
  });
};

// include css only if not already included
const include_css = (css, options = {}) => {
  let link_tag = document.querySelector(`link[href="${css}"]`);
  if (!link_tag) {
    try {
      const head = document.head || document.getElementsByTagName('head')[0];
      link_tag = document.createElement('link');
      link_tag.rel = 'stylesheet';
      link_tag.href = css;
      link_tag.type = options.type || "text/css";
      if (options.media) link_tag.media = options.media;
      if (options.integrity) link_tag.integrity = options.integrity;
      if (options.crossorigin) link_tag.crossOrigin = options.crossorigin; 
      head.appendChild(link_tag);
    } catch (error) {
      console.error(`Failed to load ${css}:`, error);
    }
  }
};

// get cookie value
const getCookie = name => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
          cookie = cookie.trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === `${name}=`) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
};
