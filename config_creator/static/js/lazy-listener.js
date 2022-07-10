
function addListener (value, key, map) {
  document.getElementById(key).addEventListener(value.type, function () {
    eval(value.function)
  })
}
