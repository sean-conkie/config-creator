
/**
 * It adds a row to a table
 *
 * Args:
 *   data: The data returned from the API call.
 *   elementToAddId: The id of the table to add the row to
 *   action: The action that is being performed. This is used to determine what type of field is being
 * added.
 *   jobId: The id of the job that the task belongs to
 *   taskId: The id of the task that the field belongs to.
 */
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
      let positionType
      let deleteUrl
      if (['createColumn', 'editColumn', 'copyTable'].includes(action)) {
        rowId = 'id_field_' + rowData.id + '_row'
        deleteUrl = `/api/field/${rowData.id}/delete/`
        positionType = 'field'
      } else if (['createDrivingColumn'].includes(action)) {
        rowId = 'id_driving_column_' + rowData.id + '_row'
        deleteUrl = `/api/field/${rowData.id}/delete/`
      } else if (['createPartition'].includes(action)) {
        rowId = 'id_driving_column_' + rowData.id + '_row'
        deleteUrl = `/api/field/${rowData.id}/delete/`
      } else if (['createHistoryOrder'].includes(action)) {
        rowId = 'id_driving_column_' + rowData.id + '_row'
        deleteUrl = `/api/field/${rowData.id}/delete/`
        positionType = 'order'
      }

      const viewButton = createElement('button', null, ['btn', 'row-btn-secondary'], 0, null) // eslint-disable-line no-undef
      viewButton.setAttribute('title', 'View')
      viewButton.setAttribute('type', 'button')
      viewButton.setAttribute('aria-current', 'page')
      viewButton.setAttribute('data-bs-toggle', 'tooltip')
      viewButton.setAttribute('data-bs-placement', 'right')
      viewButton.setAttribute('data-action', 'viewColumn')
      viewButton.setAttribute('data-field-id', rowData.id)
      viewButton.setAttribute('data-job-id', jobId)
      viewButton.setAttribute('data-task-id', taskId)
      viewButton.setAttribute('data-target', elementToAddId)
      viewButton.setAttribute('data-delete-element-id', rowId)

      viewButton.appendChild(createElement('i', null, ['bi', 'bi-search'], 0, null)) // eslint-disable-line no-undef

      viewButton.addEventListener('click', function () {
        prepareFieldModal(this.dataset.action, this.dataset.fieldId, this.dataset.target, this.dataset.deleteElementId, this.dataset.jobId, this.dataset.taskId)
      })

      const deleteButton = createElement('button', null, ['btn', 'row-btn-danger', 'field-delete'], 0, null) // eslint-disable-line no-undef
      deleteButton.setAttribute('title', 'Delete')
      deleteButton.setAttribute('type', 'button')
      deleteButton.setAttribute('aria-current', 'page')
      deleteButton.setAttribute('data-bs-toggle', 'tooltip')
      deleteButton.setAttribute('data-bs-placement', 'right')
      deleteButton.setAttribute('data-delete-url', deleteUrl)
      deleteButton.setAttribute('data-delete-element-id', rowId)
      deleteButton.appendChild(createElement('i', null, ['bi', 'bi-trash3'], 0, null)) // eslint-disable-line no-undef
      deleteButton.addEventListener('click', function () {
        deleteModelObject(this.dataset.deleteUrl, this.dataset.deleteElementId) // eslint-disable-line no-undef
      })
      let transformation = null
      /* eslint-disable no-undef */
      if (content[i].transformation) {
        transformation = createElement('i', null, ['fa-solid', 'fa-shuffle'], 0, null)
        transformation.title = 'Contains transformation'
        transformation.setAttribute('aria-current', 'page')
        transformation.dataset.bsToggle = 'tooltip'
        transformation.dataset.bsPlacement = 'top'
      }

      let nullable = null
      if (!content[i].is_nullable) {
        nullable = createElement('i', null, ['bi', 'bi-asterisk'], 0, null)
        nullable.title = 'Required field'
        nullable.setAttribute('aria-current', 'page')
        nullable.dataset.bsToggle = 'tooltip'
        nullable.dataset.bsPlacement = 'top'
      }

      let primary = null
      if (content[i].is_primary_key) {
        primary = createElement('i', null, ['bi', 'bi-key'], 0, null)
        primary.title = 'Key field'
        primary.setAttribute('aria-current', 'page')
        primary.dataset.bsToggle = 'tooltip'
        primary.dataset.bsPlacement = 'top'
      }

      let rowContent = []

      const prefix = [
        createRowObject(['vertical-grip-col'], null, null, null, createElement('i', null, ['bi', 'bi-grip-vertical'], 0, null)),
        createRowObject(['vertical-grip-col', 'text-center'], null, null, null, primary),
        createRowObject(['vertical-grip-col', 'text-center'], null, null, null, null),
        createRowObject(['vertical-grip-col', 'text-center'], null, null, null, nullable),
        createRowObject(['vertical-grip-col', 'text-center'], null, null, null, transformation)
      ]

      const suffix = [
        createRowObject(['btn-column'], null, null, null, viewButton),
        createRowObject(['btn-column'], null, null, null, deleteButton),
        createRowObject(['vertical-grip-col'], null, null, null, createElement('i', null, ['bi', 'bi-grip-vertical'], 0, null))
      ]

      const sourceDiv = createElement('div')
      let sourceTableAlias = null
      let sourceColumn = null
      if (['createColumn', 'editColumn'].includes(action)) {
        sourceTableAlias = createElement('span', content[i].source_table_alias + '.')
        sourceColumn = createElement('strong', content[i].source_column)
        sourceDiv.appendChild(sourceTableAlias)
        sourceDiv.appendChild(sourceColumn)

        rowContent = rowContent.concat(prefix, [
          createRowObject(null, null, null, content[i].name, null),
          createRowObject(null, null, null, content[i].data_type, null),
          createRowObject(null, null, null, null, sourceDiv)
        ], suffix)
      } else if (['copyTable'].includes(action)) {
        sourceTableAlias = createElement('span', content[i].alias + '.')
        sourceColumn = createElement('strong', content[i].column_name)
        sourceDiv.appendChild(sourceTableAlias)
        sourceDiv.appendChild(sourceColumn)

        rowContent = rowContent.concat(prefix, [
          createRowObject(null, null, null, content[i].target_name, null),
          createRowObject(null, null, null, content[i].data_type, null),
          createRowObject(null, null, null, null, sourceDiv)
        ], suffix)
      } else if (['createDrivingColumn', 'createPartition'].includes(action)) {
        rowContent = [
          createRowObject(null, null, null, content[i].source_name + '.' + content[i].source_column, null),
          createRowObject(['btn-column'], null, null, null, deleteButton)
        ]
      } else {
        rowContent = [
          createRowObject(['vertical-grip-col'], null, null, null, createElement('i', null, ['bi', 'bi-grip-vertical'], 0, null)),
          createRowObject(null, null, null, content[i].source_name + '.' + content[i].source_column, null),
          createRowObject(['btn-column'], null, null, null, deleteButton),
          createRowObject(['vertical-grip-col'], null, null, null, createElement('i', null, ['bi', 'bi-grip-vertical'], 0, null))
        ]
      }
      let row
      if (positionType) {
        row = createRowObject(['align-middle'], rowId, rowContent, null, null, [['draggable', 'true'], ['ondragstart', 'start()'], ['ondragover', 'dragover()'], ['ondragend', `positionChange(this, ${positionType})`], ['data-field-id', rowData.id], ['data-position', content[i].position], ['data-task-id', taskId]])
      } else {
        row = createRowObject(['align-middle'], rowId, rowContent, null, null, [['data-field-id', rowData.id], ['data-position', content[i].position], ['data-task-id', taskId]])
      }

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
 * It sends a POST request to the server, and if the server responds with a 200 status code, it adds
 * the response to the table
 *
 * Args:
 *   taskId: The id of the task that is being created.
 */
function submitCopyTable (taskId) { // eslint-disable-line no-unused-vars
  const connectionId = document.getElementById('id_field_source_connection').value
  const dataset = document.getElementById('id_field_source_dataset').value
  const tableName = document.getElementById('id_field_source_table_name').value
  if (tableName !== '') {
    const url = `/api/task/${taskId}/connection/${connectionId}/dataset/${dataset}/table/${tableName}/copy/`

    const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef
    const spinnerId = 'id_copy_table_spinner'

    const parent = document.getElementById('id_source_to_target_table')
    parent.style.position = 'relative'
    parent.appendChild(createSpinner(spinnerId, 'large')) // eslint-disable-line no-undef
    parent.setAttribute('disabled', 'true')

    xhttp.responseType = 'json'
    xhttp.onload = function () {
      if (spinnerId) {
        const spinner = document.getElementById(spinnerId)
        if (parent && parent.nodeType) {
          parent.removeChild(spinner)
          parent.removeAttribute('disabled')
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
        addFieldToTable(data, 'id_source_to_target', 'copyTable', null, taskId) // eslint-disable-line no-undef
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
function positionChange (element, type) { // eslint-disable-line no-unused-vars
  let url
  if (type === 'field') {
    url = `/api/task/${element.dataset.taskId}/field/${element.dataset.fieldId}/position/${element.dataset.position}/update/`
  } else if (type === 'order') {
    url = `/api/task/${element.dataset.taskId}/history-order/${element.dataset.fieldId}/position/${element.dataset.position}/update/`
  }

  callModelApi(url, 'POST') // eslint-disable-line no-undef
}

/**
 * It gets the source data type, target data type, and column name from the form, and then sends an
 * AJAX request to the server to get the transformation code
 */
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
      document.getElementById('id_field_transformation').value = data.replace('"', '').replace('"', '')// eslint-disable-line no-undef
    } else {
      document.getElementById('id_field_transformation').value = ''
    }
    update(document.getElementById('id_field_transformation').value, document.getElementById('id_field_transformation').dataset.targetId) // eslint-disable-line no-undef
  }

  xhttp.open('GET', url, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send()
}

/**
 * It takes an array of elements and an action, and then it loops through the elements and performs the
 * action on each element
 *
 * Args:
 *   elements: The elements to be reset.
 *   action: 'reset' or 'edit'
 */
function resetFieldInput (elements, action) {
  const formElements = ['LABEL', 'INPUT', 'SELECT', 'TEXTAREA']
  document.getElementById('id_field_transformation').classList.remove('form-control')
  document.getElementById('id_field_transformation').value = ''
  update(document.getElementById('id_field_transformation').value, document.getElementById('id_field_transformation').dataset.targetId) // eslint-disable-line no-undef

  for (let i = 0; i < elements.length; i++) {
    if (action === 'reset') {
      if (formElements.includes(elements[i].tagName)) {
        elements[i].removeAttribute('hidden')
        elements[i].setAttribute('disabled', 'true')
        if (elements[i].tagName === 'INPUT') {
          if (elements[i].type === 'checkbox') {
            if (elements[i].checked === true) {
              elements[i].checked = false
            }
            elements[i].value = 'off'
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
      resetFieldInput(elements[i].children, action)
    }
  }

  document.getElementById('id_field_modal_edit_button').classList.add('visually-hidden')
  document.getElementById('id_field_modal_submit_button').classList.add('visually-hidden')
  document.getElementById('id_field_transformation_load').classList.add('visually-hidden')
  document.getElementById('id_id').setAttribute('hidden', 'true')
  document.getElementById('id_field_modal_action').setAttribute('hidden', 'true')
}

/**
 * It prepares the modal for the user to create, view, or edit a field
 *
 * Args:
 *   usage: This is the action that the modal will perform. It can be one of the following:
 *   fieldId: The id of the field to be edited.
 *   target: The element that will be updated with the new data.
 *   deleteElementId: The id of the element to be deleted.
 *   jobId: The id of the job that the field is associated with.
 *   taskId: The id of the task that the field is associated with.
 */
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

  const transformationLoadButton = document.getElementById('id_field_transformation_load')

  const title = document.getElementById('id_field_modal_title')

  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef
  xhttp.responseType = 'json'

  if (usage === 'createColumn') {
    resetFieldInput(modalElements, 'reset')
    submitButton.dataset.deleteElementId = undefined
    submitButton.dataset.fieldId = undefined
    title.textContent = 'Create New Column'
    resetFieldInput(modalElements, 'edit')
    submitButton.classList.remove('visually-hidden')
    transformationLoadButton.classList.remove('visually-hidden')

    document.getElementById('id_id').setAttribute('hidden', 'true')

    xhttp.onload = function () {
      document.getElementById('id_position').value = xhttp.response.result
    }

    xhttp.open('GET', `/api/task/${taskId}/position/`, true)
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
    xhttp.send()
  } else if (['createDrivingColumn', 'createPartition', 'createHistoryOrder'].includes(usage)) {
    resetFieldInput(modalElements, 'reset')
    resetFieldInput(modalElements, 'edit')
    if (usage === 'createDrivingColumn') {
      title.textContent = 'Add History Driving Column'
    } else if (usage === 'createPartition') {
      title.textContent = 'Add History Partition Column'
    } else if (usage === 'createHistoryOrder') {
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
    resetFieldInput(modalElements, 'reset')
    title.textContent = 'Column Details'
    editButton.classList.remove('visually-hidden')

    xhttp.onload = function () {
      const data = xhttp.response
      if (xhttp.status === 200) {
        const result = data.result
        document.getElementById('id_name').value = result.name
        if (result.is_primary_key === true) {
          document.getElementById('id_is_primary_key').checked = true
          document.getElementById('id_is_primary_key').value = 'on'
        }
        if (result.is_nullable === true) {
          document.getElementById('id_is_nullable').checked = true
          document.getElementById('id_is_nullable').value = 'on'
        }
        const dataTypeOptions = document.getElementById('id_data_type').children
        for (let x = 0; x < dataTypeOptions.length; x++) {
          if (dataTypeOptions[x].value === `${result.data_type_id}`) {
            dataTypeOptions[x].setAttribute('selected', 'true')
          }
        }

        document.getElementById('id_position').value = result.position
        document.getElementById('id_source_column').value = result.source_column
        document.getElementById('id_source_name').value = `${result.source_name} ${result.source_table_alias}`
        document.getElementById('id_source_data_type').value = result.source_data_type
        document.getElementById('id_field_transformation').value = result.transformation
        update(document.getElementById('id_field_transformation').value, document.getElementById('id_field_transformation').dataset.targetId) // eslint-disable-line no-undef
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
    resetFieldInput(modalElements, 'edit')
    title.textContent = 'Edit Column Details'
    submitButton.classList.remove('visually-hidden')
    transformationLoadButton.classList.remove('visually-hidden')

    document.getElementById('id_field_modal_action').value = usage

    if (usage === 'editDrivingColumn') {
      title.textContent = 'Edit History Driving Column'
      document.getElementById('id_name').setAttribute('disabled', 'true')
      document.getElementById('id_is_primary_key').setAttribute('disabled', 'true')
      document.getElementById('id_is_nullable').setAttribute('disabled', 'true')
      document.getElementById('id_data_type').setAttribute('disabled', 'true')
      document.getElementById('id_position').setAttribute('disabled', 'true')
      document.getElementById('id_source_data_type').setAttribute('disabled', 'true')
      document.getElementById('id_field_transformation').setAttribute('disabled', 'true')
      submitButton.classList.remove('visually-hidden')
    }
  }

  document.getElementById('id_field_modal_action').value = usage
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_field_modal')).show() // eslint-disable-line no-undef
}

/**
 * It sends a form to the server, and then adds the field to the table
 *
 * Args:
 *   target: The element that the new field will be added to.
 *   deleteElementId: The id of the element to delete.
 *   fieldId: The id of the field to update. If this is not provided, a new field will be created.
 *   jobId: The id of the job that the field belongs to.
 *   taskId: The id of the task that the field belongs to.
 */
function sendField (target, deleteElementId, fieldId, jobId, taskId) { // eslint-disable-line no-unused-vars
  document.getElementById('id_name').removeAttribute('disabled')
  document.getElementById('id_is_primary_key').removeAttribute('disabled')
  document.getElementById('id_is_nullable').removeAttribute('disabled')
  document.getElementById('id_data_type').removeAttribute('disabled')
  document.getElementById('id_position').removeAttribute('disabled')
  document.getElementById('id_source_data_type').removeAttribute('disabled')
  document.getElementById('id_field_transformation').removeAttribute('disabled')
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

      addFieldToTable(data, target, document.getElementById('id_field_modal_action').value, jobId, taskId) // eslint-disable-line no-undef
      bootstrap.Modal.getOrCreateInstance(document.getElementById('id_field_modal')).hide() // eslint-disable-line no-undef
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

/**
 * It takes a data type as a parameter, makes an AJAX request to the server, and then sets the selected
 * option in the data type dropdown to the data type returned by the server
 *
 * Args:
 *   dataType: The data type to map to a data type option.
 */
function dataTypeMap (dataType) { // eslint-disable-line no-unused-vars
  if (dataType && dataType !== '' && dataType !== 'undefined' && dataType !== 'null' && dataType !== undefined && dataType !== null) {
    const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef

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
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
    xhttp.send()
  }
}
