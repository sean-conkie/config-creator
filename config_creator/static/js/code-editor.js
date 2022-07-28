
/**
     * `update(text, targetId)` is a function that takes in a string of text and a targetId, and
     * updates the HTML element with the targetId with the text
     *
     * Args:
     *   text: The text to be updated.
     *   targetId: The id of the element that will be updated.
     */
function update (text, targetId) { // eslint-disable-line no-unused-vars
  const resultElement = document.getElementById(targetId)
  if (text[text.length - 1] === '\n') {
    text += ' '
  }
  resultElement.innerHTML = text.replace(/&/g, '&').replace(/</g, '<')
  Prism.highlightElement(resultElement) // eslint-disable-line no-undef
}

/**
     * Scroll result to scroll coords of event - sync with textarea
     *
     * Args:
     *   element: The element that is being scrolled.
     *   targetId: The id of the element you want to sync with.
     */
function syncScroll (element, targetId) { // eslint-disable-line no-unused-vars
  const resultElement = document.getElementById(targetId)
  resultElement.scrollTop = element.scrollTop
  resultElement.scrollLeft = element.scrollLeft
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
function checkTab (element, event, targetId) { // eslint-disable-line no-unused-vars
  const code = element.value
  if (event.key === 'Tab') {
    event.preventDefault()
    const beforeTab = code.slice(0, element.selectionStart)
    const afterTab = code.slice(element.selectionEnd, element.value.length)
    const cursorPos = element.selectionEnd + 1
    element.value = beforeTab + '\t' + afterTab
    element.selectionStart = cursorPos
    element.selectionEnd = cursorPos
    update(element.value, targetId)
  }
}
