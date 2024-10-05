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
  let link_tag = document.getElementById(id);
  if (!link_tag) {
    const head = document.head || document.getElementsByTagName('head')[0];
    link_tag = document.createElement('link');
    link_tag.rel = 'stylesheet';
    link_tag.href = css;
    link_tag.id = id;
    head.appendChild(link_tag);
  }
};

const highlightCodeBlock = (blockID, codeBlockCSS, theme, themeCSS, highlightScript, language, languageScript) => {
  include_css(codeBlockCSS, "code-block-style");
  include_css(themeCSS, `code-block-highlight-${theme}`);
  if (!!language) {
    Promise.all([
      include_js(highlightScript, "code-block-highlight-script"),
      include_js(languageScript, `code-highlight-${language}`)
    ]).then(() => {
      hljs.highlightElement(document.getElementById(blockID));
    }).catch(error => {
      console.error('Error loading scripts:', error);
    });
  }
}

const copyToClipboard = (event, id) => {
  const buttonText = event.target.innerText
  const copyText = document.getElementById(id);
  navigator.clipboard.writeText(copyText.innerText);
  event.target.innerText = 'Copied ✓';
  event.target.classList.add('copied-to-clipboard');
  setTimeout(() => {
    event.target.innerText = buttonText;
    event.target.classList.remove('copied-to-clipboard');
  }, 1000);
}

