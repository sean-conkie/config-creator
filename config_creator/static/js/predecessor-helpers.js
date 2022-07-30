

function addPredecessorObject (data, jobId, taskId, targetId) {
  if ('result' in data) {
    const parent = document.getElementById(targetId)
    const placeholder = parent.querySelector('.placeholder-row')
    if (placeholder) {
      placeholder.classList.add('delete-row')
    }

    const content = data.result.content

    for (let i = 0; i < content.length; i++) {
      const rowData = content[i]

      const part1 = (rowData.upper_bound) ? 'between' : 'greater than or equal to'
      const part2 = (rowData.upper_bound) ? ` and ${rowData.lower_bound} plus ${rowData.upper_bound}` : ''
      const deltaDescription = `select records where '${rowData.field.source_name}.${rowData.field.source_column}' is ${part1} ${rowData.lower_bound}${part2}`
      const rowContent = [
        createRowObject(null, null, null, deltaDescription, null, null) // eslint-disable-line no-undef
      ]

      const deleteButton = createElement('button', null, ['btn', 'btn-danger', 'field-delete'], 0, null) // eslint-disable-line no-undef
      deleteButton.setAttribute('title', 'Delete')
      deleteButton.setAttribute('type', 'button')
      deleteButton.setAttribute('aria-current', 'page')
      deleteButton.setAttribute('data-bs-toggle', 'tooltip')
      deleteButton.setAttribute('data-bs-placement', 'right')
      deleteButton.setAttribute('data-delta-id', rowData.id)
      deleteButton.setAttribute('data-task-id', taskId)
      deleteButton.setAttribute('data-job-id', jobId)
      deleteButton.setAttribute('data-target-id', 'id_delta_row')
      deleteButton.appendChild(createElement('i', null, ['bi', 'bi-trash'], 0, null)) // eslint-disable-line no-undef
      deleteButton.addEventListener('click', function () {
        deleteDelta(this.dataset.jobId, this.dataset.taskId, this.dataset.deltaId) // eslint-disable-line no-undef
      })

      rowContent.push(createRowObject(['btn-column'], null, null, null, deleteButton)) // eslint-disable-line no-undef

      addRow([createRowObject(null, 'id_delta_row', rowContent, null, null, null)], parent, null) // eslint-disable-line no-undef
    }
  }
}

/**
 * It removes all the values from the form elements and resets the form to its default state
 * 
 * Args:
 *   elements: The elements to be reset.
 */
function resetPredecessorInput (elements) {
  const formElements = ['LABEL', 'INPUT', 'SELECT', 'TEXTAREA']
  
  for (let i = 0; i < elements.length; i++) {
    if (formElements.includes(elements[i].tagName)) {
      if (elements[i].tagName === 'INPUT') {
        if (elements[i].type === 'checkbox') {
          if (elements[i].checked === 'true') {
            elements[i].setAttribute('checked', 'false')
          }
          elements[i].value = 'off'
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
      resetPredecessorInput(elements[i].children)
    }
  }
}

function preparePredecessorModal () { // eslint-disable-line no-unused-vars
  resetPredecessorInput(document.getElementById('id_predecessor_form').children)
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_predecessor_modal')).show() // eslint-disable-line no-undef
}


function sendPredecessor (jobId, taskId, targetId, spinnerElementId) { // eslint-disable-line no-unused-vars
  let spinnerId = null
  if (spinnerElementId) {
    const parent = document.getElementById(spinnerElementId)
    parent.style.position = 'relative'
    spinnerId = spinnerElementId + '_spinner'
    parent.appendChild(createSpinner(spinnerId, 'large')) // eslint-disable-line no-undef
    parent.setAttribute('disabled', 'true')
  }

  const form = document.getElementById('id_predecessor_form')
  const formData = new FormData(form) // eslint-disable-line no-undef
  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef

  xhttp.responseType = 'json'
  xhttp.onload = function () {
    if (spinnerId) {
      const spinner = document.getElementById(spinnerId)
      const parent = spinner.parentNode
      /* eslint-disable no-undef */
      if (parent && parent.nodeType) {
        parent.removeChild(spinner)
        parent.removeAttribute('disabled')
      }
      /* eslint-enable no-undef */
    }

    const data = xhttp.response
    if ((xhttp.status === 200 || xhttp.status === 404) && 'message' in data) {
      createToast(data.message, data.type, true) // eslint-disable-line no-undef

      addPredecessorObject(data, jobId, taskId, targetId)
      bootstrap.Modal.getOrCreateInstance(document.getElementById('id_predecessor_modal')).hide() // eslint-disable-line no-undef
    } else {
      const message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
      createToast(message.desc, message.name, true) // eslint-disable-line no-undef
    }
  }

  xhttp.open('POST', `/api/job/${jobId}/task/${taskId}/predecessor/add/`, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send(formData)
}


function deletePredecessor (jobId, taskId, predecessorId) { // eslint-disable-line no-unused-vars
  document.getElementById('id_predecessor_table').style.position = 'relative'
  deleteModelObject(`/api/job/${jobId}/task/${taskId}/predecessor/${predecessorId}/update/`, `id_predecessor_${predecessorId}_row`, 'id_predecessor_tbody', 'large') // eslint-disable-line no-undef
}
