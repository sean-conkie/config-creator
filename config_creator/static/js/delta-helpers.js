
/**
 * It adds a row to the table for each delta object returned by the API
 *
 * Args:
 *   data: the data returned from the API call
 *   jobId: The ID of the job
 *   taskId: The ID of the task that the delta is being added to.
 *   targetId: The id of the table to add the row to.
 */
function addDeltaObject (data, jobId, taskId, targetId) {
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
      resetDeltaInput(elements[i].children)
    }
  }
}

/**
 * It resets the input fields in the modal and then shows the modal
 */
function prepareDeltaModal () { // eslint-disable-line no-unused-vars
  resetDeltaInput(document.getElementById('id_delta_modal').children)
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_delta_modal')).show() // eslint-disable-line no-undef
}

/**
 * It sends a POST request to the server with the data from the form, and then it adds the delta object
 * to the page
 *
 * Args:
 *   jobId: The ID of the job that the task belongs to.
 *   taskId: The id of the task that the delta is being added to.
 *   targetId: The id of the element that will be updated with the new delta object.
 *   spinnerElementId: The id of the element that will have the spinner added to it.
 */
function sendDeltaCondition (jobId, taskId, targetId, spinnerElementId) { // eslint-disable-line no-unused-vars
  let spinnerId = null
  if (spinnerElementId) {
    const parent = document.getElementById(spinnerElementId)
    spinnerId = spinnerElementId + '_spinner'
    parent.appendChild(createSpinner(spinnerId)) // eslint-disable-line no-undef
    parent.setAttribute('disabled', 'true')
  }

  const form = document.getElementById('id_delta_form')
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

      addDeltaObject(data, jobId, taskId, targetId)
      resetDeltaInput(document.getElementById('id_delta_modal').children) // eslint-disable-line no-undef
      document.getElementById('id_add_delta_button').classList.add('visually-hidden')
      bootstrap.Modal.getOrCreateInstance(document.getElementById('id_delta_modal')).hide() // eslint-disable-line no-undef
    } else {
      const message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
      createToast(message.desc, message.name, true) // eslint-disable-line no-undef
    }
  }

  xhttp.open('POST', `/api/job/${jobId}/task/${taskId}/delta/add/`, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send(formData)
}

/**
 * It deletes a delta from the database and the DOM
 *
 * Args:
 *   jobId: the id of the job
 *   taskId: the id of the task that the delta is associated with
 *   deltaId: the id of the delta to delete
 */
function deleteDelta (jobId, taskId, deltaId) { // eslint-disable-line no-unused-vars
  document.getElementById('id_delta_tbody').style.position = 'relative'
  deleteModelObject(`/api/job/${jobId}/task/${taskId}/delta/${deltaId}/update/`, 'id_delta_row', 'id_delta_tbody', 'large') // eslint-disable-line no-undef
  document.getElementById('id_add_delta_button').classList.remove('visually-hidden')
}
