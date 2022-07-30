
function resetConditionInput (elements) {
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
      resetConditionInput(elements[i].children)
    }
  }
}

/**
 * It resets the condition modal's input fields, sets the modal's submit button's data attributes, and
 * then shows the modal
 *
 * Args:
 *   jobId: The id of the job that the task belongs to.
 *   taskId: The id of the task that the condition is being added to.
 *   joinId: The id of the join that the condition is being added to.
 *   targetId: The id of the element that the condition is being applied to.
 */
function prepareConditionModal (jobId, taskId, joinId, targetId) { // eslint-disable-line no-unused-vars
  resetConditionInput(document.getElementById('id_condition_modal').children)
  document.getElementById('id_condition_modal_submit_button').setAttribute('data-job-id', jobId)
  document.getElementById('id_condition_modal_submit_button').setAttribute('data-task-id', taskId)
  document.getElementById('id_condition_modal_submit_button').setAttribute('data-join-id', joinId)
  document.getElementById('id_condition_modal_submit_button').setAttribute('data-target-id', targetId)
  document.getElementById('id_condition_modal_submit_button').setAttribute('data-persist', true)
  document.getElementById('id_condition_modal_submit_and_close_button').setAttribute('data-job-id', jobId)
  document.getElementById('id_condition_modal_submit_and_close_button').setAttribute('data-task-id', taskId)
  document.getElementById('id_condition_modal_submit_and_close_button').setAttribute('data-join-id', joinId)
  document.getElementById('id_condition_modal_submit_and_close_button').setAttribute('data-target-id', targetId)
  document.getElementById('id_condition_modal_submit_and_close_button').setAttribute('data-persist', false)
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_condition_modal')).show() // eslint-disable-line no-undef
}

/**
 * It adds a row to the table for each condition object returned by the API
 *
 * Args:
 *   data: The data returned from the API call.
 *   addToModal: If true, the condition will be added to the modal. If false, it will be added to the
 * page.
 *   jobId: The id of the job that the condition is being added to.
 *   taskId: The id of the task that the condition is being added to.
 *   targetId: The id of the table to add the rows to.
 */
function addConditionObject (data, addToModal, jobId, taskId, targetId) {
  if ('result' in data) {
    const parent = document.getElementById(targetId)
    const placeholder = parent.querySelector('.placeholder-row')
    if (placeholder) {
      placeholder.classList.add('delete-row')
    }

    const content = data.result.content

    for (let i = 0; i < content.length; i++) {
      const rowData = content[i]

      let left = null
      let right = null
      if (rowData.left.source_column) {
        left = `${rowData.left.source_table_alias}.${rowData.left.source_column}`
      } else {
        left = rowData.left.transformation
      }

      if (rowData.right.source_column) {
        right = `${rowData.right.source_table_alias}.${rowData.right.source_column}`
      } else {
        right = rowData.right.transformation
      }

      const rowContent = [
        createRowObject(null, null, null, rowData.logic_operator, null, null), // eslint-disable-line no-undef
        createRowObject(null, null, null, left, null, null), // eslint-disable-line no-undef
        createRowObject(null, null, null, rowData.operator, null, null), // eslint-disable-line no-undef
        createRowObject(null, null, null, right, null, null) // eslint-disable-line no-undef
      ]

      if (addToModal) {
        addRow([createRowObject(null, null, rowContent, null, null, null)], document.getElementById('id_condition_modal_tbody'), 1) // eslint-disable-line no-undef
      }

      const deleteButton = createElement('button', null, ['btn', 'btn-danger', 'field-delete'], 0, null) // eslint-disable-line no-undef
      deleteButton.setAttribute('title', 'Delete')
      deleteButton.setAttribute('type', 'button')
      deleteButton.setAttribute('aria-current', 'page')
      deleteButton.setAttribute('data-bs-toggle', 'tooltip')
      deleteButton.setAttribute('data-bs-placement', 'right')
      deleteButton.setAttribute('data-delete-url', `/api/condition/${rowData.id}/delete/`)
      deleteButton.setAttribute('data-delete-element-id', `id_join_condition_${rowData.id}_row`)
      deleteButton.appendChild(createElement('i', null, ['bi', 'bi-trash'], 0, null)) // eslint-disable-line no-undef
      deleteButton.addEventListener('click', function () {
        deleteModelObject(this.dataset.deleteUrl, this.dataset.deleteElementId) // eslint-disable-line no-undef
      })

      rowContent.push(createRowObject(['btn-column'], null, null, null, deleteButton)) // eslint-disable-line no-undef

      addRow([createRowObject(null, `id_join_condition_${rowData.id}_row`, rowContent, null, null, null)], parent, null) // eslint-disable-line no-undef
    }
  }
}

/**
 * It sends a POST request to the server with the form data from the condition modal, and then adds the
 * condition to the DOM
 *
 * Args:
 *   persist: boolean, whether or not to persist the modal
 *   jobId: The id of the job that the task belongs to.
 *   taskId: The id of the task that the condition is being added to.
 *   joinId: The id of the join object.
 *   targetId: The id of the element that will be the parent of the new condition.
 *   spinnerElementId: The id of the element that will have the spinner added to it.
 */
function sendCondition (persist, jobId, taskId, joinId, targetId, spinnerElementId) { // eslint-disable-line no-unused-vars
  let spinnerId = null
  const addToModal = persist
  if (spinnerElementId) {
    const parent = document.getElementById(spinnerElementId)
    spinnerId = spinnerElementId + '_spinner'
    parent.appendChild(createSpinner(spinnerId)) // eslint-disable-line no-undef
    parent.setAttribute('disabled', 'true')
  }

  const form = document.getElementById('id_condition_form')
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

      addConditionObject(data, addToModal, jobId, taskId, targetId)
      if (addToModal === false) {
        bootstrap.Modal.getOrCreateInstance(document.getElementById('id_condition_modal')).hide() // eslint-disable-line no-undef
        resetConditionInput(document.getElementById('id_condition_modal').children)
      }
    } else {
      const message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
      createToast(message.desc, message.name, true) // eslint-disable-line no-undef
    }
  }

  let url
  if (joinId !== 'null' && joinId !== 'undefined') {
    url = `/api/job/${jobId}/task/${taskId}/join/${joinId}/condition/add/`
  } else {
    url = `/api/job/${jobId}/task/${taskId}/condition/add/`
  }

  xhttp.open('POST', url, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send(formData)
}
