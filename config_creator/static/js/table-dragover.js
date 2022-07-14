let row
function start () { // eslint-disable-line no-unused-vars
  row = event.target // eslint-disable-line no-undef
}
function dragover () { // eslint-disable-line no-unused-vars
  const e = event // eslint-disable-line no-undef
  e.preventDefault()

  const children = Array.from(e.target.parentNode.parentNode.children)

  if (children.indexOf(e.target.parentNode) > children.indexOf(row)) {
    e.target.parentNode.after(row)
  } else {
    e.target.parentNode.before(row)
  }

  e.target.parentNode.dataset.position = children.indexOf(e.target.parentNode) + 1
}
