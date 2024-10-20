const localDateTime = (elementID, dateString) => {
  const element = document.getElementById(elementID);
  // Only run if element exists and date is valid
  if (element != null) {
    const date_options = {
      // weekday: "short",
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    const time_options = {
      hour: "2-digit",
      minute: "2-digit",
      hour12: false
    };
    element.innerText = convertUTCDateToLocalDate(dateString, date_options, time_options);
  }
  else {
    console.warn('An null element was passed to localDate, check the element exists on the current page.')
  }
}

// Usage: document.getElementById("id").innerText = convertUTCDateToLocalDate(new Date('2021-08-12 09:58:22'));
// Non-numeric month format will cause errors in multi-lingual setting
const convertUTCDateToLocalDate = (dateString, date_options, time_options) => {
  const date = new Date(Date.parse(dateString + " UTC"));
  if (date instanceof Date && !isNaN(date)) {
    const formattedDate = date.toLocaleDateString(undefined, date_options);
    const formattedTime = date.toLocaleTimeString(undefined, time_options);
    const localTimezone = date.toLocaleDateString(navigator.language, { timeZoneName: 'short' }).split(/\s+/).pop();
    return `${formattedDate} ${formattedTime} (${localTimezone})`;
  } else {
    console.warn('Date string could not be parsed, check a valid ISO formatted datetime string is being passed.')
  }
};

const localiseDates = (
  className,
  date_options = { weekday: "short", year: "numeric", month: "long", day: "numeric" },
  time_options = { hour: "numeric", minute: "2-digit", hour12: true }
) => {
  document.querySelectorAll(`.${className}`).forEach((element) => {
    const utcDateString = element.innerText;
    const localDateString = convertUTCDateToLocalDate(utcDateString, date_options, time_options);
    element.innerText = localDateString;
  });
}

// set all external links to open in new tab
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('a[href^="http"], a[href^="/documents/"]').forEach(link => {
    link.setAttribute('target', '_blank');
    link.setAttribute('rel', 'nofollow noopener');
  });
});

// change rich text <fa> font awesome tags: 
// <fa style="display:none;">something</fa> -> <fa class="something">&nbsp;&nbsp;&nbsp;&nbsp;</fa>
document.addEventListener('DOMContentLoaded', () => {
  fa_icons = document.getElementsByTagName('fa');
  for (let i = 0; i < fa_icons.length; i++) {
    const fa_class = fa_icons[i].innerText;
    if (fa_class) {
      fa_icons[i].className = fa_icons[i].innerText;
      fa_icons[i].innerHTML = "&nbsp;".repeat(4);
      fa_icons[i].removeAttribute('style');
    }
  }
});

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


