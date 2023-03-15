// src: https://css-tricks.com/creating-an-editable-textarea-that-supports-syntax-highlighted-code/
function update(element) {
    let text = element.value;
    let id = element.id;
    let element_prefix = id.slice(0, id.indexOf('-') + 1);
    let result_element = document.querySelector("#" + element_prefix + "highlighting-content");
    // Handle final newlines (see article)
    if(text[text.length-1] == "\n") {
      text += " ";
    }
    // Update code
    result_element.innerHTML = text.replace(new RegExp("&", "g"), "&amp;").replace(new RegExp("<", "g"), "&lt;"); /* Global RegExp */
    // Syntax Highlight
    Prism.highlightElement(result_element);
  }
  
  function sync_scroll(element) {
    let id = element.id;
    let element_prefix = id.slice(0, id.indexOf('-') + 1);
    /* Scroll result to scroll coords of event - sync with textarea */
    let result_element = document.querySelector("#" + element_prefix + "highlighting");
    // Get and set x and y
    result_element.scrollTop = element.scrollTop;
    result_element.scrollLeft = element.scrollLeft;
  }
  
  function check_tab(element, event) {
    let code = element.value;
    if(event.key == "Tab") {
      /* Tab key pressed */
      event.preventDefault(); // stop normal
      let before_tab = code.slice(0, element.selectionStart); // text before tab
      let after_tab = code.slice(element.selectionEnd, element.value.length); // text after tab
      let cursor_pos = element.selectionStart + 1; // where cursor moves after tab - moving forward by 1 char to after tab
      element.value = before_tab + "\t" + after_tab; // add tab char
      // move cursor
      element.selectionStart = cursor_pos;
      element.selectionEnd = cursor_pos;
      update(element.value); // Update text to include indent
    }
  }