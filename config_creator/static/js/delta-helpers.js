
function resetDeltaInput (elements) {
  const formElements = ['LABEL', 'INPUT', 'SELECT', 'TEXTAREA']
  document.getElementById('id_delta_transformation').classList.remove('form-control')
  document.getElementById('id_delta_transformation').value = ''
  update(document.getElementById('id_delta_transformation').value, document.getElementById('id_delta_transformation').dataset.targetId) // eslint-disable-line no-undef
  document.getElementById('id_delta_lower_bound').classList.remove('form-control')
  document.getElementById('id_delta_lower_bound').value = ''
  update(document.getElementById('id_delta_lower_bound').value, document.getElementById('id_delta_lower_bound').dataset.targetId) // eslint-disable-line no-undef
  for (let i = 0; i < elements.length; i++) {
    if (formElements.includes(elements[i].tagName)) {
      if (elements[i].tagName === 'INPUT') {
        if (elements[i].type === 'checkbox') {
          elements[i].removeAttribute('checked')
          elements[i].value = 'false'
        } else {
          elements[i].value = ''
        }
      } else if (elements[i].tagName === 'TEXTAREA') {
        elements[i].textContent = ''
      } else if (elements[i].tagName === 'SELECT') {
        const selectChildren = elements[i].children
        for (let x = 0; x < selectChildren.length; x++) {
          selectChildren[x].removeAttribute('selected')
        }
      }
    }

    if (elements[i].hasChildNodes()) {
      resetDeltaInput(elements[i].children)
    }
  }
}

function prepareDeltaModal () { // eslint-disable-line no-unused-vars
  resetDeltaInput(document.getElementById('id_delta_modal').children)
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_delta_modal')).show() // eslint-disable-line no-undef
}
