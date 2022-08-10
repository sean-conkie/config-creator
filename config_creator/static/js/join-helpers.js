
/**
 * It takes an array of elements, and if the element is a form element, it resets it
 *
 * Args:
 *   elements: The elements to be reset.
 */
function resetJoinInput (elements) {
  const formElements = ['LABEL', 'INPUT', 'SELECT', 'TEXTAREA']
  document.getElementById('id_join_modal_submit_button').removeAttribute('data-join-id')

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
      resetJoinInput(elements[i].children)
    }
  }
}

/**
 * It prepares the modal for the user to add or edit a join
 *
 * Args:
 *   jobId: The id of the job that the task belongs to.
 *   taskId: The id of the task that the join is being added to.
 *   joinId: The id of the join to be edited. If this is null, then the modal is being used to create a
 * new join.
 */
function prepareJoinModal (jobId, taskId, joinId) { // eslint-disable-line no-unused-vars
  resetJoinInput(document.getElementById('id_join_modal').children)
  if (joinId) {
    document.getElementById('id_join_modal_submit_button').setAttribute('data-join-id', joinId)

    const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef

    xhttp.responseType = 'json'
    xhttp.onload = function () {
      const data = xhttp.response
      if (xhttp.status === 200) {
        const result = data.result

        const joinTypeOptions = document.getElementById('id_type').children
        for (let x = 0; x < joinTypeOptions.length; x++) {
          if (joinTypeOptions[x].value === result.type_id) {
            joinTypeOptions[x].setAttribute('selected', 'true')
          }
        }

        document.getElementById('id_left').value = result.left_table
        document.getElementById('id_right').value = result.right_table
      } else {
        const message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
        createToast(message.desc, message.name, true) // eslint-disable-line no-undef
      }
    }

    xhttp.open('GET', `/api/job/${jobId}/task/${taskId}/join/`, true)
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
    xhttp.send()
  }
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_join_modal')).show() // eslint-disable-line no-undef
}

/**
 * It sends a POST request to the server with the form data, and then it either creates a toast with
 * the response message or it adds the join object to the page
 *
 * Args:
 *   jobId: The id of the job
 *   taskId: The id of the task that the join is being added to.
 *   joinId: The id of the join object. If it's null, then it's a new join object.
 */
function sendJoin (jobId, taskId, joinId) { // eslint-disable-line no-unused-vars
  const form = document.getElementById('id_join_form')
  const formData = new FormData(form) // eslint-disable-line no-undef
  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef

  xhttp.responseType = 'json'
  xhttp.onload = function () {
    const data = xhttp.response
    if ((xhttp.status === 200 || xhttp.status === 404) && 'message' in data) {
      createToast(data.message, data.type, true) // eslint-disable-line no-undef

      addJoinObject(data, jobId, taskId) // eslint-disable-line no-undef
      bootstrap.Modal.getOrCreateInstance(document.getElementById('id_join_modal')).hide() // eslint-disable-line no-undef
    } else {
      const message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
      createToast(message.desc, message.name, true) // eslint-disable-line no-undef
    }
  }

  let url
  if (joinId) {
    url = `/api/job/${jobId}/task/${taskId}/join/${joinId}/update/`
  } else {
    url = `/api/job/${jobId}/task/${taskId}/join/add/`
  }

  xhttp.open('POST', url, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send(formData)
}

/**
 * It deletes a join object
 *
 * Args:
 *   jobId: The id of the job that the task is in.
 *   taskId: The id of the task that the join is being deleted from.
 *   joinId: The id of the join object to delete
 */
function deleteJoin (jobId, taskId, joinId) { // eslint-disable-line no-unused-vars
  document.getElementById(`id_join_container_${joinId}`).style.position = 'relative'
  deleteModelObject(`/api/job/${jobId}/task/${taskId}/join/${joinId}/update/`, `id_join_container_${joinId}`, `id_join_container_${joinId}`, 'large') // eslint-disable-line no-undef
}

/**
 * It takes the data returned from the API call, and creates a bunch of HTML elements to display the
 * data
 *
 * Args:
 *   data: The data returned from the API call
 *   jobId: The id of the job
 *   taskId: The id of the task that the join is being added to.
 */
function addJoinObject (data, jobId, taskId) {
  if ('result' in data) {
    const parent = document.getElementById('id_join_container_parent')

    const content = data.result.content

    for (let i = 0; i < content.length; i++) {
      const rowData = content[i]
      /* eslint-disable no-undef */
      const joinContainer = createElement('div', null, ['container', 'py-3', 'px-3', 'bg-light', 'rounded'], 0, `id_join_container_${rowData.id}`)
      const header = createElement('div', null, ['row', 'g-3', 'py-1'], 0, null)
      const headerCol = createElement('div', null, ['col-md-12', 'col-lg-12'], 0, null)
      const headerTest = createElement('h5', `${rowData.type} ${rowData.left_table} to ${rowData.right_table}`, null, 0, null)

      /* eslint-enable no-undef */

      headerCol.append(headerTest)
      header.append(headerCol)
      joinContainer.append(header)

      /* eslint-disable no-undef */
      const body = createElement('div', null, ['row', 'g-3', 'py-1'], 0, null)
      const bodyCol1 = createElement('div', null, ['col-md-1', 'col-lg-1'], 0, null)
      const bodyCol1Text = createElement('p', 'on', ['lead'], 0, null)

      /* eslint-enable no-undef */
      bodyCol1.append(bodyCol1Text)
      body.append(bodyCol1)

      /* eslint-disable no-undef */
      const bodyCol2 = createElement('div', null, ['col-md-11', 'col-lg-11'], 0, null)
      const table = createElement('table', null, ['table', 'table-hover'], 0, null)
      const tableHeader = createElement('thead', null, null, 0, null)
      const tableHeaderRow = createElement('tr', null, null, 0, null)
      for (let t = 0; t < 6; t++) {
        const th = createElement('th', null, null, 0, null)
        th.setAttribute('scope', 'col')

        /* eslint-enable no-undef */

        tableHeaderRow.append(th)
      }
      tableHeader.append(tableHeaderRow)
      table.append(tableHeader)

      /* eslint-disable no-undef */
      const tableBody = createElement('tbody', null, ['text-center', 'align-middle'], 0, null)
      const conditions = rowData.conditions
      for (let c = 0; c < conditions.length; c++) {
        const tr = createElement('tr', null, null, 0, null)
        const conditionId = conditions[c].id
        const rowId = `id_join_condition_${conditionId}_row`

        tr.setAttribute('id', rowId)
        const col1 = createElement('td', null, null, 0, null)
        col1.textContent = conditions[c].logic_operator
        const col2 = createElement('td', null, null, 0, null)
        col2.textContent = conditions[c].left
        const col3 = createElement('td', null, null, 0, null)
        col3.textContent = conditions[c].operator
        const col4 = createElement('td', null, null, 0, null)
        col4.textContent = conditions[c].right
        const col5 = createElement('td', null, ['btn-column'], 0, null)
        const viewButton = createElement('button', null, ['btn', 'btn-secondary'], 0, null)
        viewButton.setAttribute('title', 'View')
        viewButton.setAttribute('type', 'button')
        viewButton.setAttribute('id', `id_join_condition_${conditionId}_view`)
        viewButton.setAttribute('aria-current', 'page')
        viewButton.setAttribute('data-bs-toggle', 'tooltip')
        viewButton.setAttribute('data-bs-placement', 'right')
        viewButton.setAttribute('data-condition-id', conditionId)
        viewButton.appendChild(createElement('i', null, ['bi', 'bi-search'], 0, null))
        col5.append(viewButton)
        const col6 = createElement('td', null, ['btn-column'], 0, null)
        const deleteButton = createElement('button', null, ['btn', 'btn-danger', 'condition-delete'], 0, null)
        deleteButton.setAttribute('title', 'Delete')
        deleteButton.setAttribute('type', 'button')
        deleteButton.setAttribute('id', `id_join_condition_${conditionId}_delete`)
        deleteButton.setAttribute('aria-current', 'page')
        deleteButton.setAttribute('data-bs-toggle', 'tooltip')
        deleteButton.setAttribute('data-bs-placement', 'right')
        deleteButton.setAttribute('data-delete-url', `/api/condition/${conditionId}/delete/`)
        deleteButton.setAttribute('data-delete-element-id', rowId)
        deleteButton.appendChild(createElement('i', null, ['bi', 'bi-trash'], 0, null))
        col6.append(deleteButton)

        tr.append(col1)
        tr.append(col2)
        tr.append(col3)
        tr.append(col4)
        tr.append(col5)
        tr.append(col6)
        tableBody.append(tr)
      }
      table.append(tableBody)
      bodyCol2.append(table)
      body.append(bodyCol2)

      const buttonRow = createElement('div', null, ['row', 'g-3', 'py-1'], 0, null)
      const addCol = createElement('div', null, ['col-md-2', 'col-lg-2'], 0, null)
      const deleteCol = createElement('div', null, ['col-md-2', 'col-lg-2'], 0, null)
      const addConditionButton = createElement('button', null, ['w-100', 'btn', 'btn-info'], 0, null)
      addConditionButton.setAttribute('type', 'button')
      addConditionButton.appendChild(createElement('i', null, ['bi', 'bi-plus'], 0, null))
      addConditionButton.appendChild(createElement('span', ' Add Condition'))
      addConditionButton.addEventListener('click', function () {
        prepareConditionModal(this.dataset.jobId, this.dataset.taskId, this.dataset.joinId, this.dataset.targetId)
      })

      const deleteJoinButton = createElement('button', null, ['w-100', 'btn', 'btn-danger', 'join-delete'], 0, null)
      deleteJoinButton.setAttribute('type', 'button')
      deleteJoinButton.setAttribute('id', `id_delete_join_${rowData.id}`)
      deleteJoinButton.setAttribute('data-job-id', jobId)
      deleteJoinButton.setAttribute('data-task-id', taskId)
      deleteJoinButton.setAttribute('data-join-id', rowData.id)
      deleteJoinButton.appendChild(createElement('i', null, ['bi', 'bi-trash3'], 0, null))
      deleteJoinButton.appendChild(createElement('span', ' Delete Join'))
      /* eslint-enable no-undef */
      deleteJoinButton.addEventListener('click', function () {
        deleteJoin(this.dataset.jobId, this.dataset.taskId, this.dataset.joinId)
      })

      addCol.append(addConditionButton)
      deleteCol.append(deleteJoinButton)
      buttonRow.append(addCol)
      buttonRow.append(deleteCol)
      body.append(buttonRow)
      joinContainer.append(body)
      parent.append(joinContainer)
    }
  }
}
