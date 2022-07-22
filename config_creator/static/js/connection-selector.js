
/**
 * It creates an element of the type you specify, and adds the content, classes, layer, and id you
 * specify
 *
 * Args:
 *   type: the type of element to create, e.g. 'div'
 *   content: The text content of the element.
 *   classList: an array of class names to add to the element
 *   layer: the layer of the element, which is used to calculate the margin-left of the element.
 *   id: The id of the element.
 *
 * Returns:
 *   A function that creates an element.
 */
function createElement (type, content, classList, layer, id) {
  const outer = document.createElement(type)
  if (content) {
    outer.textContent = content
  }

  if (classList) {
    for (let i = 0; i < classList.length; i++) {
      outer.classList.add(classList[i])
    }
  }

  if (layer) {
    outer.style.marginLeft = (layer * 20) + 'px'
  }

  if (id) {
    outer.setAttribute('id', id)
  }

  return outer
}

/**
 * It creates a row element for a column in a table
 *
 * Args:
 *   object: the object that contains the data for the column
 *   layer: the layer of the tree table that the element is being created for
 *
 * Returns:
 *   A row element with the column name, data type, and mode.
 */
function createColumnElement (object, layer) {
  const row = createElement('tr', null, null, null, null)
  const columnName = createElement('td', object.column_name, ['tree-table-select'], null, null)
  columnName.setAttribute('onclick', 'selectElement(this)')
  columnName.setAttribute('data-column-name', object.column_name)
  columnName.setAttribute('data-column-full', object.dataset + '.' + object.table_name + '.' + object.column_name)
  columnName.setAttribute('data-table-name', object.table_name)
  columnName.setAttribute('data-table-full', object.dataset + '.' + object.table_name)
  columnName.setAttribute('data-dataset-name', object.dataset)
  columnName.setAttribute('data-data-type', object.data_type)
  const id = 'id_connection_' + object.connection_id + '_dataset_' + object.dataset + '_' + object.table_name + '_' + object.column_name
  columnName.setAttribute('id', id)
  const dataType = createElement('td', object.data_type, null, null, null)
  let mode
  if (object.is_nullable) {
    mode = createElement('td', 'NULLABLE', null, null, null)
  } else {
    mode = createElement('td', 'REQUIRED', null, null, null)
  }

  row.appendChild(columnName)
  row.appendChild(dataType)
  row.appendChild(mode)
  return row
}

/**
 * It creates a table element.
 *
 * Args:
 *   object: the object to be parsed
 *   layer: The layer of the element. This is used to calculate the indentation of the element.
 *
 * Returns:
 *   A function that takes an object and a layer as parameters and returns an element.
 */
function createTableElement (object, layer) {
  let element
  if (returnType.selector === 'table') {
    element = createElement('div', null, ['tree-table-select'], layer * 10, null)
  } else {
    element = createElement('details', null, ['tree-table'], layer * 10, null)
  }

  if ({}.propertyIsEnumerable.call(object, 'name')) {
    const id = 'id_connection_' + object.connection_id + '_dataset_' + object.dataset + '_' + object.name
    element.setAttribute('id', id)

    if (returnType.selector === 'table') {
      element.setAttribute('onclick', 'selectElement(this)')
      element.insertAdjacentText('beforeend', ' ' + object.name)
      element.setAttribute('data-table-name', object.name)
      element.setAttribute('data-table-full', object.dataset + '.' + object.name)
      element.setAttribute('data-dataset-name', object.dataset)
      element.setAttribute('data-connection-id', object.connection_id)
    } else {
      const summary = createElement('summary', null, ['tree-table-summary'], null, null)
      summary.appendChild(createElement('i', null, ['fa-solid', 'fa-table'], null, null))
      summary.insertAdjacentText('beforeend', ' ' + object.name)
      element.appendChild(summary)
      const layerInner = layer + 1

      const table = createElement('table', null, ['table', 'table-hover'], layerInner, null)

      if ({}.propertyIsEnumerable.call(object, 'content')) {
        const child = parseObject(object.content, layerInner)
        if (child) {
          table.appendChild(child)
        }
      }

      element.appendChild(table)
    }
  }
  return element
}

/**
 * It creates a dataset element
 *
 * Args:
 *   object: The object to be parsed.
 *   layer: The layer of the element in the tree.
 *
 * Returns:
 *   A dataset element
 */
function createDatasetElement (object, layer) {
  let element
  if (returnType.selector === 'dataset') {
    element = createElement('div', null, ['tree-dataset-select'], layer * 10, null)
  } else {
    element = createElement('details', null, ['tree-dataset'], layer * 10, null)
  }

  if ({}.propertyIsEnumerable.call(object, 'name')) {
    const id = 'id_connection_' + object.connection_id + '_dataset_' + object.name
    element.setAttribute('id', id)

    if (returnType.selector === 'dataset') {
      element.setAttribute('onclick', 'selectElement(this)')
      element.insertAdjacentText('beforeend', ' ' + object.name)
      element.setAttribute('data-dataset-name', object.name)
      element.setAttribute('data-connection-id', object.connection_id)
    } else {
      const summary = createElement('summary', null, ['tree-dataset-summary'], null, null)
      summary.appendChild(createElement('i', null, ['fa-solid', 'fa-database'], null, null))
      summary.insertAdjacentText('beforeend', ' ' + object.name)
      element.appendChild(summary)
      element.setAttribute('onclick', 'getData(' + object.connection_id + ", '" + object.name + "', '" + id + "')")

      if ({}.propertyIsEnumerable.call(object, 'content')) {
        const child = parseObject(object.content, layer + 1)
        if (child) {
          element.appendChild(child)
        }
      }
    }
  }

  return element
}

/**
 * It creates a <details> element with a <summary> element inside it, and then it appends the <summary>
 * element to the <details> element
 *
 * Args:
 *   object: The object to be parsed.
 *   layer: The current layer of the tree.
 *
 * Returns:
 *   A connection element
 */
function createConnectionElement (object, layer) {
  const detail = createElement('details', null, ['tree-connection'], layer, null)
  detail.setAttribute('id', 'id_connection_' + object.id)
  detail.setAttribute('onclick', 'getData(' + object.id + ", null, 'id_connection_" + object.id + "')")

  if ({}.propertyIsEnumerable.call(object, 'name')) {
    const summary = createElement('summary', null, ['tree-connection-summary'], null, null)
    summary.appendChild(createElement('i', null, ['fa-solid', 'fa-server'], null, null))
    summary.insertAdjacentText('beforeend', ' ' + object.name)
    detail.appendChild(summary)
  }

  if ({}.propertyIsEnumerable.call(object, 'content')) {
    const child = parseObject(object.content, layer + 1)
    if (child) {
      detail.appendChild(child)
    }
  }

  return detail
}

/**
 * It creates a `<details>` element with a `<summary>` element containing the name of the connection
 * type, and a child element containing the content of the connection type
 *
 * Args:
 *   object: The object to parse
 *   layer: The current layer of the tree.
 *
 * Returns:
 *   A <details> element with a <summary> element as a child.
 */
function createConnectionTypeElement (object, layer) {
  const detail = createElement('details', null, null, layer, null)
  if ({}.propertyIsEnumerable.call(object, 'name')) {
    detail.appendChild(createElement('summary', object.name, ['tree-connection-type'], null, null))
  }

  if ({}.propertyIsEnumerable.call(object, 'name')) {
    const child = parseObject(object.content, layer + 1)
    if (child) {
      detail.appendChild(child)
    }
  }

  return detail
}

/**
 * It takes an array of objects and a layer number, and returns a DOM element
 *
 * Args:
 *   arr: The array of objects to be parsed
 *   layer: The layer of the object.
 *
 * Returns:
 *   A function that takes in an array and a layer and returns an element.
 */
function parseObject (arr, layer) {
  if (arr.length === 0) {
    return createElement('div', null, ['modal-container'], null, null)
  }
  let element
  if (arr[0].type === 'column') {
    element = createElement('tbody', null, null, null, null)
  } else if (arr[0].type === 'table') {
    element = createElement('div', null, ['modal-container', 'bg-light'], null, null)
  } else {
    element = createElement('div', null, ['modal-container'], null, null)
  }
  for (let i = 0; i < arr.length; i++) {
    if ({}.propertyIsEnumerable.call(arr[i], 'type')) {
      let html
      if (arr[i].type === 'connection-type') {
        html = createConnectionTypeElement(arr[i], layer)
        if (i === 0) {
          html.setAttribute('open', 'true')
        }
      } else if (arr[i].type === 'connection') {
        html = createConnectionElement(arr[i], layer)
      } else if (arr[i].type === 'dataset') {
        html = createDatasetElement(arr[i], layer)
      } else if (arr[i].type === 'table' && ['column', 'table'].includes(returnType.selector)) {
        html = createTableElement(arr[i], layer)
      } else if (arr[i].type === 'column' && returnType.selector === 'column') {
        html = createColumnElement(arr[i], layer)
      }

      if (typeof html !== 'undefined') {
        element.appendChild(html)
      }
    }
  }
  return element
}

/**
 * It takes a URL and a modal ID, creates a spinner, makes an AJAX call to the URL, parses the
 * response, and displays the result in the modal
 *
 * Args:
 *   url: The URL to call.
 *   modalId: The id of the modal to display the results in.
 */
function callConnectionApi (url, modalId) {
  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef
  const parent = document.getElementById(modalId)
  if (parent.childElementCount > 0) {
    parent.children[0].appendChild(createSpinner(modalId + '_spinner')) // eslint-disable-line no-undef
  } else {
    parent.appendChild(createSpinner(modalId + '_spinner')) // eslint-disable-line no-undef
  }
  xhttp.onload = function () {
    if (xhttp.status === 200) {
      const parent = document.getElementById(modalId)
      if (parent && parent.nodeType) {
        for (let i = 0; i < parent.childNodes.length; i++) {
          if (parent.childNodes[i].tagName !== 'SUMMARY') {
            parent.removeChild(parent.childNodes[i])
          }
        }

        const data = JSON.parse(this.responseText)
        if ({}.propertyIsEnumerable.call(data, 'result')) {
          const html = parseObject(data.result, 1, null)
          if (html && html.nodeType) {
            parent.appendChild(html)
          }
        }
      }
    } else {
      /* eslint-disable no-undef */
      const message = HttpStatusEnum.get(xhttp.status)
      createToast(message.desc, message.name, true)
      /* eslint-enable no-undef */
    }

    const spinner = document.getElementById(modalId + '_spinner')
    spinner.parentNode.removeChild(spinner)
  }
  xhttp.open('GET', url, true)
  xhttp.send()
}

/**
 * It takes three parameters, and then calls the `callConnectionApi` function with the first two
 * parameters, and the third parameter as the element ID
 *
 * Args:
 *   id: The id of the schema
 *   name: The name of the schema.
 *   elementId: The id of the element that will be replaced with the data.
 */
function getData (id, name, elementId) { // eslint-disable-line no-unused-vars
  let url = '/api/schema/'
  if (name) {
    url = url + id + '/' + name + '/'
  } else {
    url = url + id + '/'
  }

  callConnectionApi(url, elementId)

  document.getElementById(elementId).removeAttribute('onclick')
}

/**
 * It displays a message to the user asking if they want to select the element they clicked on, and
 * then it displays a submit button that, when clicked, will submit the selection
 *
 * Args:
 *   element: The element that was clicked on.
 */
function selectElement (element) { // eslint-disable-line no-unused-vars
  const selector = returnType.selector
  let message
  if (selector === 'column') {
    message = "Would you like to select column '" + element.dataset.columnFull + "'?"
  } else if (selector === 'table') {
    message = "Would you like to select table '" + element.dataset.tableFull + "'?"
  } else {
    message = "Would you like to select dataset '" + element.dataset.datasetName + "'?"
  }

  document.getElementById('id_selection').textContent = message

  const submitButton = document.getElementById('id_submit_button')
  submitButton.setAttribute('onclick', "submitSelection('" + element.id + "');")
  submitButton.classList.remove('visually-hidden')
}

/**
 * It takes an id, finds the element with that id, and then sets the value of the target element to the
 * value of the dataset of the element with the id
 *
 * Args:
 *   id: The id of the element that was clicked.
 */
function submitSelection (id) { // eslint-disable-line no-unused-vars
  const selector = returnType.selector
  const element = document.getElementById(id)
  if (selector === 'column' && returnType.column.target) {
    document.getElementById(returnType.column.target).value = element.dataset[returnType.column.type]
    document.getElementById(returnType.column.target).dispatchEvent(new Event('input'))
    if (returnType.datatype.target) {
      document.getElementById(returnType.datatype.target).value = element.dataset[returnType.datatype.type]
      document.getElementById(returnType.datatype.target).dispatchEvent(new Event('input'))
    }
  }
  if ((selector === 'column' || selector === 'table') && returnType.table.target) {
    document.getElementById(returnType.table.target).value = element.dataset[returnType.table.type]
    document.getElementById(returnType.table.target).dispatchEvent(new Event('input'))
  }
  if (returnType.dataset.target) {
    document.getElementById(returnType.dataset.target).value = element.dataset[returnType.dataset.type]
    document.getElementById(returnType.dataset.target).dispatchEvent(new Event('input'))
  }
  if (returnType.connection.target) {
    document.getElementById(returnType.connection.target).value = element.dataset[returnType.connection.type]
    document.getElementById(returnType.connection.target).dispatchEvent(new Event('input'))
  }
  bootstrap.Modal.getInstance(document.getElementById('connection-modal')).hide() // eslint-disable-line no-undef
}

function setReturnType (selector, columnTarget, columnType, dataTypeTarget, tableTarget, tableType, datasetTarget, connectionTarget, reLoadModal) { // eslint-disable-line no-unused-vars
  let datasetType = null
  let connectionType = null
  let dataType = null
  if (datasetTarget) {
    datasetType = 'datasetName'
  }
  if (connectionTarget) {
    connectionType = 'connectionId'
  }
  if (dataTypeTarget) {
    dataType = 'dataType'
  }

  returnType = {
    selector,
    column: {
      target: columnTarget,
      type: columnType
    },
    datatype: {
      target: dataTypeTarget,
      type: dataType
    },
    table: {
      target: tableTarget,
      type: tableType
    },
    dataset: {
      target: datasetTarget,
      type: datasetType
    },
    connection: {
      target: connectionTarget,
      type: connectionType
    }
  }

  if (reLoadModal) {
    const modalId = 'id-modal-content'
    document.getElementById(modalId).textContent = ''
    callConnectionApi('/api/schema/', modalId)
  }
  bootstrap.Modal.getOrCreateInstance(document.getElementById('connection-modal')).show() // eslint-disable-line no-undef
}

let returnType = {
  selector: 'column',
  column: {
    target: 'id_source_column',
    type: 'columnName'
  },
  datatype: {
    target: 'id_source_data_type',
    type: 'dataType'
  },
  table: {
    target: 'id_source_name',
    type: 'tableFull'
  },
  dataset: {
    target: null,
    type: null
  },
  connection: {
    target: null,
    type: null
  }
}

callConnectionApi('/api/schema/', 'id-modal-content')

const myModalEl = document.getElementById('connection-modal')
myModalEl.addEventListener('hidden.bs.modal', function (event) {
  document.getElementById('id_selection').textContent = ''
  document.getElementById('id_submit_button').removeAttribute('onclick')
  document.getElementById('id_submit_button').classList.add('visually-hidden')
  const details = document.getElementsByTagName('details')
  for (let i = 0; i < details.length; i++) {
    details[i].removeAttribute('open')
  }
})
