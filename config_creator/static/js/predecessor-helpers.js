
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

      const targetRowId = `id_predecessor_${rowData.id}_row`

      const deleteButton = createElement('button', null, ['btn', 'row-btn-danger', 'field-delete'], 0, null) // eslint-disable-line no-undef
      deleteButton.setAttribute('title', 'Delete')
      deleteButton.setAttribute('type', 'button')
      deleteButton.setAttribute('aria-current', 'page')
      deleteButton.setAttribute('data-bs-toggle', 'tooltip')
      deleteButton.setAttribute('data-bs-placement', 'right')
      deleteButton.setAttribute('data-predecessor-id', rowData.id)
      deleteButton.setAttribute('data-task-id', taskId)
      deleteButton.setAttribute('data-job-id', jobId)
      deleteButton.setAttribute('data-target-id', targetRowId)
      /* eslint-disable no-undef */
      deleteButton.appendChild(createElement('i', null, ['bi', 'bi-trash3'], 0, null))
      deleteButton.addEventListener('click', function () {
        deletePredecessor(this.dataset.jobId, this.dataset.taskId, this.dataset.predecessorId)
      })

      const rowContent = [
        createRowObject(null, null, null, rowData.predecessor.name, null),
        createRowObject(null, null, null, rowData.predecessor.type, null),
        createRowObject(null, null, null, rowData.predecessor.description, null),
        createRowObject(null, null, null, rowData.predecessor.lastupdate, null),
        createRowObject(['btn-column'], null, null, null, deleteButton)
      ]

      addRow([createRowObject(null, targetRowId, rowContent, null, null, null)], parent, null)
      /* eslint-enable no-undef */
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

function preparePredecessorModal (jobId, taskId) { // eslint-disable-line no-unused-vars
  resetPredecessorInput(document.getElementById('id_predecessor_form').children)
  const select = document.getElementById('id_predecessor')
  const url = `/api/job/${jobId}/task/${taskId}/predecessor/tasks/`
  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef

  const options = select.children

  for (let c = 0; c < options.length; c++) {
    if (options[c].value !== '---------') {
      select.removeChild(options[c])
    }
  }

  xhttp.responseType = 'json'
  xhttp.onload = function () {
    const result = xhttp.response.result
    for (let i = 0; i < result.length; i++) {
      const option = createElement('option') // eslint-disable-line no-undef
      option.value = result[i].key
      option.textContent = result[i].value
      select.appendChild(option)
    }
  }

  xhttp.open('GET', url, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send()

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
