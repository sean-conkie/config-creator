
    /**
     * `update(text, targetId)` is a function that takes in a string of text and a targetId, and
     * updates the HTML element with the targetId with the text
     * 
     * Args:
     *   text: The text to be updated.
     *   targetId: The id of the element that will be updated.
     */
    function update(text, targetId) {  // eslint-disable-line no-unused-vars
      let result_element = document.getElementById(targetId);
      if(text[text.length-1] == "\n") {
        text += " ";
      }
      result_element.innerHTML = text.replace(new RegExp("&", "g"), "&").replace(new RegExp("<", "g"), "<"); /* Global RegExp */
      Prism.highlightElement(result_element);  // eslint-disable-line no-undef
    }

    /**
     * Scroll result to scroll coords of event - sync with textarea
     * 
     * Args:
     *   element: The element that is being scrolled.
     *   targetId: The id of the element you want to sync with.
     */
    function sync_scroll(element, targetId) {  // eslint-disable-line no-unused-vars
      let result_element = document.getElementById(targetId);
      result_element.scrollTop = element.scrollTop;
      result_element.scrollLeft = element.scrollLeft;
    }

    /**
     * When the tab key is pressed, the text before the cursor is stored in a variable, the text after
     * the cursor is stored in a variable, the cursor is moved forward by one character, the tab
     * character is added to the text, and the cursor is moved to the new position
     * 
     * Args:
     *   element: the textarea element
     *   event: The event that triggered the function.
     */
    function check_tab(element, event, targetId) {  // eslint-disable-line no-unused-vars
      let code = element.value;
      if(event.key == "Tab") {
        event.preventDefault();
        let before_tab = code.slice(0, element.selectionStart);
        let after_tab = code.slice(element.selectionEnd, element.value.length);
        let cursor_pos = element.selectionEnd + 1;
        element.value = before_tab + "\t" + after_tab;
        element.selectionStart = cursor_pos;
        element.selectionEnd = cursor_pos;
        update(element.value, targetId);
      }
    }
