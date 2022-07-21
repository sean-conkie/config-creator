
function addFieldToTable (data, elementToAddId, action, jobId, taskId) {
  if ('result' in data) {
    const parent = document.getElementById(elementToAddId)
    const placeholder = parent.querySelector('.placeholder-row')
    if (placeholder) {
      placeholder.classList.add('delete-row')
    }

    const content = data.result.content

    for (let i = 0; i < content.length; i++) {
      const rowData = content[i]
      let rowId
      if (['createColumn', 'editColumn', 'copyTable'].includes(action)) {
        rowId = 'id_field_' + rowData.id + '_row'
      } else if (['historyDrivingColumn', 'editDrivingColumn'].includes(action)) {
        rowId = 'id_driving_column_' + rowData.id + '_row'
      }

      const viewButton = createElement('button', null, ['btn', 'btn-secondary'], 0, null) // eslint-disable-line no-undef
      viewButton.setAttribute('title', 'View')
      viewButton.setAttribute('aria-current', 'page')
      viewButton.setAttribute('data-bs-toggle', 'tooltip')
      viewButton.setAttribute('data-bs-placement', 'right')
      viewButton.setAttribute('data-action', 'viewColumn')
      viewButton.setAttribute('data-field-id', rowId)
      viewButton.setAttribute('data-job-id', jobId)
      viewButton.setAttribute('data-task-id', taskId)
      viewButton.setAttribute('data-target', elementToAddId)
      viewButton.setAttribute('data-delete-element-id', rowId)

      viewButton.appendChild(createElement('i', null, ['bi', 'bi-search'], 0, null)) // eslint-disable-line no-undef

      viewButton.addEventListener('click', function () {
        prepareFieldModal(this.dataset.action, this.dataset.fieldId, this.dataset.target, this.dataset.deleteElementId, this.dataset.jobId, this.dataset.taskId)
      })

      const deleteButton = createElement('button', null, ['btn', 'btn-danger', 'field-delete'], 0, null) // eslint-disable-line no-undef
      deleteButton.setAttribute('title', 'Delete')
      deleteButton.setAttribute('aria-current', 'page')
      deleteButton.setAttribute('data-bs-toggle', 'tooltip')
      deleteButton.setAttribute('data-bs-placement', 'right')
      deleteButton.setAttribute('data-delete-url', `/api/field/${rowData.id}/delete/`)
      deleteButton.setAttribute('data-delete-element-id', rowId)
      deleteButton.appendChild(createElement('i', null, ['bi', 'bi-trash'], 0, null)) // eslint-disable-line no-undef
      deleteButton.addEventListener('click', function () {
        deleteModelObject(this.dataset.deleteUrl, this.dataset.deleteElementId) // eslint-disable-line no-undef
      })
      let transformation = null
      /* eslint-disable no-undef */
      if (content[i].transformation) {
        transformation = createElement('i', null, ['fa-solid', 'fa-shuffle'], 0, null)
      }

      let nullable = null
      if (!content[i].is_nullable) {
        nullable = createElement('i', null, ['bi', 'bi-asterisk'], 0, null)
      }

      let primary = null
      if (content[i].is_primary_key) {
        primary = createElement('i', null, ['bi', 'bi-key'], 0, null)
      }

      let rowContent = []

      const prefix = [
        createRowObject(['vertical-grip-col'], null, null, null, createElement('i', null, ['bi', 'bi-grip-vertical'], 0, null)),
        createRowObject(null, null, null, null, primary),
        createRowObject(null, null, null, null, null),
        createRowObject(null, null, null, null, nullable),
        createRowObject(null, null, null, null, transformation)
      ]

      const suffix = [
        createRowObject(['btn-column'], null, null, null, viewButton),
        createRowObject(['btn-column'], null, null, null, deleteButton),
        createRowObject(['vertical-grip-col'], null, null, null, createElement('i', null, ['bi', 'bi-grip-vertical'], 0, null))
      ]

      if (['createColumn', 'editColumn'].includes(action)) {
        rowContent = rowContent.concat(prefix, [
          createRowObject(null, null, null, content[i].name, null),
          createRowObject(null, null, null, content[i].data_type, null),
          createRowObject(null, null, null, content[i].source_name + '.' + content[i].source_column, null)
        ], suffix)
      } else if (['copyTable'].includes(action)) {
        rowContent = rowContent.concat(prefix, [
          createRowObject(null, null, null, content[i].column_name, null),
          createRowObject(null, null, null, content[i].data_type, null),
          createRowObject(null, null, null, content[i].dataset + '.' + content[i].table_name + '.' + content[i].column_name, null)
        ], suffix)
      } else {
        rowContent = [
          createRowObject(['vertical-grip-col'], null, null, null, createElement('i', null, ['bi', 'bi-grip-vertical'], 0, null)),
          createRowObject(null, null, null, content[i].source_name + '.' + content[i].source_column, null),
          createRowObject(['btn-column'], null, null, null, viewButton),
          createRowObject(['btn-column'], null, null, null, deleteButton),
          createRowObject(['vertical-grip-col'], null, null, null, createElement('i', null, ['bi', 'bi-grip-vertical'], 0, null))
        ]
      }
      const row = createRowObject(['align-middle'], rowId, rowContent, null, null, [['draggable', 'true'], ['ondragstart', 'start()'], ['ondragover', 'dragover()'], ['ondragend', 'fieldPositionChange(this)'], ['data-field-id', rowData.id], ['data-position', content[i].position], ['data-task-id', taskId]])

      if ('position' in content[i]) {
        addRow([row], parent, content[i].position)
      } else {
        addRow([row], parent)
      }
      /* eslint-enable no-undef */
    }
  }
}

/**
 * It sends a POST request to the server, which then returns a JSON object containing the table's
 * schema
 */
function submitCopyTable () { // eslint-disable-line no-unused-vars
  const connectionId = document.getElementById('id_field_source_connection').value
  const dataset = document.getElementById('id_field_source_dataset').value
  const tableName = document.getElementById('id_field_source_table_name').value
  if (tableName !== '') {
    const url = `/api/task/{{task.id}}/connection/${connectionId}/dataset/${dataset}/table/${tableName}/copy/`

    const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef
    const spinnerId = 'id_copy_table_spinner'

    const parent = document.getElementById('id_copy_table')
    parent.appendChild(createSpinner(spinnerId)) // eslint-disable-line no-undef

    xhttp.responseType = 'json'
    xhttp.onload = function () {
      if (spinnerId) {
        const spinner = document.getElementById(spinnerId)
        if (parent && parent.nodeType) {
          parent.removeChild(spinner)
        }
      }
      data = xhttp.response // eslint-disable-line no-undef
      let message
      if (xhttp.status === 200) {
        if ('message' in data) { // eslint-disable-line no-undef
          message = {
            /* eslint-disable no-undef */
            desc: data.message,
            name: data.type
            /* eslint-enable no-undef */
          }
        } else {
          message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
        }
        addFieldToTable(data, 'id_source_to_target') // eslint-disable-line no-undef
      } else {
        message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
      }
      createToast(message.desc, message.name, true) // eslint-disable-line no-undef
    }

    xhttp.open('POST', url, true)
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
    xhttp.send()
  }
}

/**
 * It takes the position of the field in the table and updates the database with the new position
 *
 * Args:
 *   element: The element that was moved.
 */
function fieldPositionChange (element) { // eslint-disable-line no-unused-vars
  const position = element.dataset.position
  const url = `/api/task/${element.dataset.taskId}/field/${element.dataset.fieldId}/position/${position}/update/`
  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef
  xhttp.onload = function () {
    if (xhttp.status !== 200) {
      const message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
      createToast(`There has been an error updating the position of the column - ${message.desc}.  Please edit the field to change it's position.`, `Error - ${message.name}`, true) // eslint-disable-line no-undef
    }
  }
  xhttp.open('POST', url, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send()
}

function dataComparison () { // eslint-disable-line no-unused-vars
  const source = document.getElementById('id_source_data_type').value
  let target
  const options = document.getElementById('id_data_type').childNodes

  for (let i = 0; i < options.length; i++) {
    if (options[i].selected && options[i].value !== '') {
      target = options[i].textContent
    }
  }

  const column = document.getElementById('id_source_name').value + '.' + document.getElementById('id_source_column').value

  const url = `/api/data-type-comparison/${source}/${target}/${column}/`
  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef

  xhttp.responseType = 'text'
  xhttp.onload = function () {
    const data = xhttp.response
    if (xhttp.status === 200 && data) {
      document.getElementById('id_transformation').value = data.replace('"', '').replace('"', '')
    } else {
      document.getElementById('id_transformation').value = ''
    }
  }

  xhttp.open('GET', url, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send()
}

function resetInput (elements, action) {
  const formElements = ['LABEL', 'INPUT', 'SELECT', 'TEXTAREA']

  for (let i = 0; i < elements.length; i++) {
    if (action === 'reset') {
      if (formElements.includes(elements[i].tagName)) {
        elements[i].removeAttribute('hidden')
        elements[i].setAttribute('disabled', 'true')
        if (elements[i].tagName === 'INPUT') {
          if (elements[i].type === 'checkbox') {
            elements[i].removeAttribute('checked')
            elements[i].value = 'false'
          } else {
            elements[i].value = ''
          }

          if (elements[i].id === 'id_position') {
            elements[i].value = -1
          }
        } else if (elements[i].tagName === 'TEXTAREA') {
          elements[i].textContent = ''
        } else if (elements[i].tagName === 'SELECT') {
          const selectChildren = elements[i].children
          for (let x = 0; x < selectChildren.length; x++) {
            selectChildren[x].removeAttribute('selected')
            // if (selectChildren[x].value === '1') {
            //   selectChildren[x].setAttribute('selected', 'true')
            // }
          }
        }
      }
    } else if (action === 'edit') {
      if (formElements.includes(elements[i].tagName)) {
        elements[i].removeAttribute('hidden')
        elements[i].removeAttribute('disabled')
      }
    }

    if (elements[i].hasChildNodes()) {
      resetInput(elements[i].children, action)
    }
  }

  document.getElementById('id_field_modal_edit_button').classList.add('visually-hidden')
  document.getElementById('id_field_modal_submit_button').classList.add('visually-hidden')
  document.getElementById('id_id').setAttribute('hidden', 'true')
  document.getElementById('id_field_modal_action').setAttribute('hidden', 'true')
}

function prepareFieldModal (usage, fieldId, target, deleteElementId, jobId, taskId) {
  const modalElements = document.getElementById('id_field_modal').children
  const editButton = document.getElementById('id_field_modal_edit_button')
  if (usage === 'viewColumn') {
    editButton.dataset.usage = 'editColumn'
  } else if (usage === 'viewDrivingColumn') {
    editButton.dataset.usage = 'editDrivingColumn'
  }
  const submitButton = document.getElementById('id_field_modal_submit_button')
  submitButton.dataset.deleteElementId = (deleteElementId !== undefined) ? deleteElementId : submitButton.dataset.deleteElementId
  submitButton.dataset.target = (target !== undefined) ? target : submitButton.dataset.target
  submitButton.dataset.fieldId = (fieldId !== undefined) ? fieldId : submitButton.dataset.fieldId
  submitButton.dataset.jobId = (jobId !== undefined) ? jobId : submitButton.dataset.jobId
  submitButton.dataset.taskId = (taskId !== undefined) ? taskId : submitButton.dataset.taskId

  const title = document.getElementById('id_field_modal_title')

  if (usage === 'createColumn') {
    resetInput(modalElements, 'reset')
    title.textContent = 'Create New Column'
    resetInput(modalElements, 'edit')
    submitButton.classList.remove('visually-hidden')
    document.getElementById('id_id').setAttribute('hidden', 'true')
  } else if (['historyDrivingColumn', 'historyPartition', 'historyHistoryOrder'].includes(usage)) {
    resetInput(modalElements, 'reset')
    resetInput(modalElements, 'edit')
    if (usage === 'historyDrivingColumn') {
      title.textContent = 'Add History Driving Column'
    } else if (usage === 'historyPartition') {
      title.textContent = 'Add History Partition Column'
    } else if (usage === 'historyHistoryOrder') {
      title.textContent = 'Add History Order Column'
    }
    document.getElementById('id_name').setAttribute('disabled', 'true')
    document.getElementById('id_is_primary_key').setAttribute('disabled', 'true')
    document.getElementById('id_is_nullable').setAttribute('disabled', 'true')
    document.getElementById('id_data_type').setAttribute('disabled', 'true')
    document.getElementById('id_position').setAttribute('disabled', 'true')
    document.getElementById('id_source_data_type').setAttribute('disabled', 'true')
    document.getElementById('id_transformation').setAttribute('disabled', 'true')
    submitButton.classList.remove('visually-hidden')
  } else if (['viewColumn', 'viewDrivingColumn'].includes(usage)) {
    resetInput(modalElements, 'reset')
    title.textContent = 'Column Details'
    editButton.classList.remove('visually-hidden')

    const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef

    xhttp.responseType = 'json'
    xhttp.onload = function () {
      const data = xhttp.response
      if (xhttp.status === 200) {
        const result = data.result
        document.getElementById('id_name').value = result.name
        if (result.is_primary_key === true) {
          document.getElementById('id_is_primary_key').setAttribute('checked', 'true')
        }
        if (result.is_nullable === true) {
          document.getElementById('id_is_nullable').setAttribute('checked', 'true')
        }
        const dataTypeOptions = document.getElementById('id_data_type').children
        for (let x = 0; x < dataTypeOptions.length; x++) {
          if (dataTypeOptions[x].value === result.data_type_id) {
            dataTypeOptions[x].setAttribute('selected', 'true')
          }
        }

        document.getElementById('id_position').value = result.position
        document.getElementById('id_source_column').value = result.source_column
        document.getElementById('id_source_name').value = result.source_name
        document.getElementById('id_source_data_type').value = result.source_data_type
        document.getElementById('id_transformation').value = result.transformation
        document.getElementById('id_id').value = result.id
      } else {
        const message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
        createToast(message.desc, message.name, true) // eslint-disable-line no-undef
      }
    }

    xhttp.open('GET', `/api/field/${fieldId}/`, true)
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
    xhttp.send()

    if (usage === 'viewDrivingColumn') {
      title.textContent = 'History Driving Column'
    } else if (usage === 'viewPartition') {
      title.textContent = 'History Partition Column'
    } else if (usage === 'viewOrder') {
      title.textContent = 'History Order Column'
    }
  } else if (['editColumn', 'editDrivingColumn'].includes(usage)) {
    resetInput(modalElements, 'edit')
    title.textContent = 'Edit Column Details'
    submitButton.classList.remove('visually-hidden')

    if (usage === 'editDrivingColumn') {
      title.textContent = 'Edit History Driving Column'
      document.getElementById('id_name').setAttribute('disabled', 'true')
      document.getElementById('id_is_primary_key').setAttribute('disabled', 'true')
      document.getElementById('id_is_nullable').setAttribute('disabled', 'true')
      document.getElementById('id_data_type').setAttribute('disabled', 'true')
      document.getElementById('id_position').setAttribute('disabled', 'true')
      document.getElementById('id_source_data_type').setAttribute('disabled', 'true')
      document.getElementById('id_transformation').setAttribute('disabled', 'true')
      submitButton.classList.remove('visually-hidden')
    }
  }

  document.getElementById('id_field_modal_action').value = usage
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_field_modal')).show() // eslint-disable-line no-undef
}

function sendField (target, deleteElementId, fieldId, jobId, taskId) { // eslint-disable-line no-unused-vars
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_field_modal')).hide() // eslint-disable-line no-undef
  document.getElementById('id_name').removeAttribute('disabled')
  document.getElementById('id_is_primary_key').removeAttribute('disabled')
  document.getElementById('id_is_nullable').removeAttribute('disabled')
  document.getElementById('id_data_type').removeAttribute('disabled')
  document.getElementById('id_position').removeAttribute('disabled')
  document.getElementById('id_source_data_type').removeAttribute('disabled')
  document.getElementById('id_transformation').removeAttribute('disabled')
  const form = document.getElementById('id_field_form')
  const formData = new FormData(form) // eslint-disable-line no-undef
  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef

  xhttp.responseType = 'json'
  xhttp.onload = function () {
    const data = xhttp.response
    if ((xhttp.status === 200 || xhttp.status === 404) && 'message' in data) {
      createToast(data.message, data.type, true) // eslint-disable-line no-undef
      if (deleteElementId !== undefined && deleteElementId !== 'undefined') {
        const element = document.getElementById(deleteElementId)
        if (element.tagName === 'TR') {
          element.classList.add('delete-row')
        } else {
          element.parentNode.removeChild(element)
        }
      }

      addFieldToTable(data, target, document.getElementById('id_field_modal_action').value, fieldId, jobId, taskId) // eslint-disable-line no-undef
    } else {
      const message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
      createToast(message.desc, message.name, true) // eslint-disable-line no-undef
    }
  }

  let url
  if (fieldId && fieldId !== '' && fieldId !== undefined && fieldId !== 'undefined') {
    url = `/api/task/${taskId}/field/${fieldId}/update/`
  } else {
    url = `/api/task/${taskId}/field/add/`
  }

  xhttp.open('POST', url, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send(formData)

  const submitButton = document.getElementById('id_field_modal_submit_button')
  submitButton.dataset.deleteElementId = undefined
  submitButton.dataset.target = undefined
  submitButton.dataset.fieldId = undefined
  submitButton.dataset.jobId = undefined
  submitButton.dataset.taskId = undefined
}

function dataTypeMap(dataType) {
  if (dataType && dataType !== '' && dataType !== 'undefined' && dataType !== 'null' && dataType !== undefined && dataType !== null) {
    const xhttp = new XMLHttpRequest()

    xhttp.responseType = 'json'
    xhttp.onload = function () {
      
      const data = xhttp.response
      if (xhttp.status === 200) {
        const dataTypeOptions = document.getElementById('id_data_type').children

        for (let i = 0; i < dataTypeOptions.length; i++) {
          if (dataTypeOptions[i].textContent === data) {
            dataTypeOptions[i].setAttribute('selected', 'true')
          } else {
            dataTypeOptions[i].removeAttribute('selected')
          }
        }
      }
    }
    
    xhttp.open('GET', `/api/data-type-map/${dataType}/`, true)
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
    xhttp.send()
  }
}