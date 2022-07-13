
/**
 * It adds an event listener to an element with the id of the key, and when the event is triggered, it
 * runs the function in the value
 *
 * Args:
 *   value: The value of the key in the map.
 *   key: The id of the element you want to add the event listener to.
 *   map: The map of event listeners.
 */
function addListener (value, key, map) { // eslint-disable-line no-unused-vars
  document.getElementById(key).addEventListener(value.type, function () {
    eval(value.function) // eslint-disable-line no-eval
  })
}
