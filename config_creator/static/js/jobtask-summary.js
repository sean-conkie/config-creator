/**
 * It makes an AJAX call to the server, and when the server responds, it populates the modal with the
 * data it received
 *
 * Args:
 *   id: The id of the task to load the summary for.
 */
function jobTaskSummaryModalLoad (id) { // eslint-disable-line no-unused-vars
  document.getElementById('id_task_summary_modal_content_container').classList.add('visually-hidden')
  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef

  const parent = document.getElementById('id_task_summary_modal_content')
  const spinnerId = 'id_task_summary_modal_content_spinner'
  parent.appendChild(createSpinner(spinnerId, 'large')) // eslint-disable-line no-undef

  xhttp.responseType = 'json'
  xhttp.onload = function () {
    const data = xhttp.response
    if (xhttp.status === 200) {
      populateJobTaskSummaryModal(data.result)
    } else {
      const message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
      createToast(message.desc, message.name, true) // eslint-disable-line no-undef
    }

    if (spinnerId) {
      const spinner = document.getElementById(spinnerId)
      if (parent && parent.nodeType) {
        parent.removeChild(spinner)
      }
    }
  }
  xhttp.open('GET', `/api/task/${id}/summary/`, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send()

  taskSummaryPopulate = false // eslint-disable-line no-unused-vars, no-undef
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_task_summary_modal')).show() // eslint-disable-line no-undef
}

function populateJobTaskSummaryModal (data) {
  const summary = data.summary
  document.getElementById('id_summary_description').textContent = summary.description

  /* eslint-disable no-undef */
  const metaData = document.getElementById('id_summary_table_metadata')
  const p1 = createElement('p')
  p1.appendChild(createElement('strong', 'Grain: '))
  p1.appendChild(createElement('span', summary.grain.join(', ')))
  const p2 = createElement('p')
  p2.appendChild(createElement('strong', 'Table Type: '))
  p2.appendChild(createElement('span', summary.table_type))
  /* eslint-enable no-undef */
  metaData.appendChild(p1)
  metaData.appendChild(p2)

  document.getElementById('id_summary_joins').textContent = ''
  const joinList = createElement('ul', null, ['list-group', 'list-group-flush']) // eslint-disable-line no-undef
  for (let j = 0; j < summary.joins.length; j++) {
    joinList.appendChild(createElement('li', summary.joins[j], ['list-group-item', 'list-group-item-action'])) // eslint-disable-line no-undef
  }
  document.getElementById('id_summary_joins').appendChild(joinList)

  document.getElementById('id_summary_where').textContent = ''
  const whereList = createElement('ul', null, ['list-group', 'list-group-flush']) // eslint-disable-line no-undef
  for (let w = 0; w < summary.where.length; w++) {
    whereList.appendChild(createElement('li', summary.where[w], ['list-group-item', 'list-group-item-action'])) // eslint-disable-line no-undef
  }

  document.getElementById('id_summary_where').appendChild(whereList)

  const historyList = createElement('ul', null, ['list-group', 'list-group-flush']) // eslint-disable-line no-undef
  if ({}.propertyIsEnumerable.call(summary, 'history_partition')) {
    historyList.appendChild(createElement('li', `Partition by ${summary.history_partition.join(', ')}`, ['list-group-item', 'list-group-item-action'])) // eslint-disable-line no-undef
    if ({}.propertyIsEnumerable.call(summary, 'history_order')) {
      historyList.appendChild(createElement('li', `Order by ${summary.history_order.join(', ')}`, ['list-group-item', 'list-group-item-action'])) // eslint-disable-line no-undef
    }
    document.getElementById('id_summary_history_criteria').appendChild(historyList)
  } else {
    document.getElementById('id_summary_history_criteria').textContent = ''
    document.getElementById('id_summary_history_criteria').appendChild(createElement('span', 'N/A')) // eslint-disable-line no-undef
  }
  let row
  for (let s = 0; s < summary.schema.length; s++) {
    const rowContent = [
      /* eslint-disable no-undef */
      createRowObject(null, null, null, summary.schema[s][0]),
      createRowObject(null, null, null, summary.schema[s][1]),
      createRowObject(null, null, null, summary.schema[s][2]),
      createRowObject(null, null, null, summary.schema[s][3]),
      createRowObject(null, null, null, summary.schema[s][4])
      /* eslint-enable no-undef */
    ]

    row = createRowObject(null, null, rowContent) // eslint-disable-line no-undef
    addRow([row], document.getElementById('id_summary_schema_tbody')) // eslint-disable-line no-undef
  }

  if (summary.schema.length === 0) {
    row = createRowObject(null, null, [createRowObject(['text-center'], null, null, 'No schema', null, [['colspan', '5']])]) // eslint-disable-line no-undef
    addRow([row], document.getElementById('id_summary_schema_tbody')) // eslint-disable-line no-undef
  }

  for (let c = 0; c < summary.column.length; c++) {
    const rowContent = [
      createRowObject(null, null, null, summary.column[c].column), // eslint-disable-line no-undef
      createRowObject(null, null, null, summary.column[c].transformation) // eslint-disable-line no-undef
    ]

    row = createRowObject(null, null, rowContent) // eslint-disable-line no-undef
    addRow([row], document.getElementById('id_summary_column_tbody')) // eslint-disable-line no-undef
  }

  if (summary.column.length === 0) {
    row = createRowObject(null, null, [createRowObject(['text-center'], null, null, 'No column transformations', null, [['colspan', '2']])]) // eslint-disable-line no-undef
    addRow([row], document.getElementById('id_summary_column_tbody')) // eslint-disable-line no-undef
  }

  document.getElementById('id_copy_summary_button').dataset.template = data.template
  document.getElementById('id_task_summary_modal_content_container').classList.remove('visually-hidden')
}
