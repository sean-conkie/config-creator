

/**
 * It creates a `<details>` element with a `<summary>` element inside it, and then it appends the
 * result of calling `parseObject()` on the `content` property of the object passed to it as the second
 * argument
 * 
 * Args:
 *   object: The object to be parsed.
 *   layer: The current layer of the tree.
 * 
 * Returns:
 *   A <details> element with a <summary> element as a child.
 */
function createGitDirectory (object, layer) {
  const detail = createElement('details', null, ['tree-dir'], layer, null)

  if ({}.propertyIsEnumerable.call(object, 'name')) {
    const summary = createElement('summary', null, ['tree-dir-summary'], null, null)
    summary.appendChild(createElement('i', null, ['fa-solid', 'fa-folder-open'], null, null))
    summary.insertAdjacentText('beforeend', ' ' + object.name)
    detail.appendChild(summary)
  }

  if ({}.propertyIsEnumerable.call(object, 'content')) {
    const child = parseGitObject(object.content, layer + 1)
    if (child) {
      detail.appendChild(child)
    }
  }

  return detail
}


function parseGitObject (arr, layer) {
  if (arr.length === 0) {
    return createElement('div', null, ['modal-container'], null, null)
  }
  let element = createElement('div', null, ['modal-container'], null, null)
  for (let i = 0; i < arr.length; i++) {
    if ({}.propertyIsEnumerable.call(arr[i], 'type')) {
      let html
      if (arr[i].type === 'dir') {
        html = createGitDirectory(arr[i], layer)
      } else if (arr[i].type === 'file' && /(?:\.([^.]+))?$/.exec(arr[i].name)[1] == 'json') {
        html = createElement('div', null, ['tree-file-json'])
        html.appendChild(createElement('i', null, ['fa-solid', 'fa-file-code'], null, null).insertAdjacentText('beforeend', ' ' + arr[i].name))
      } else if (arr[i].type === 'file') {
        html = createElement('div', null, ['tree-file'])
        html.appendChild(createElement('i', null, ['fa-solid', 'fa-file-cirlce-xmark'], null, null).insertAdjacentText('beforeend', ' ' + arr[i].name))
      }

      if (typeof html !== 'undefined') {
        element.appendChild(html)
      }
    }
  }
  return element
}

/**
 * It gets the data from the API and displays it in the modal
 * 
 * Args:
 *   id: The id of the repository.
 *   branch: The branch to get the data from.
 */
function getGitData (id, branch) { // eslint-disable-line no-unused-vars
  let url = `/api/repositories/${id}/pull/`

  if (branch) {
    url = `${url}${branch}/`
  }

  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef
  const parent = document.getElementById('id_git_file_select_modal_content')
  parent.appendChild(createSpinner('id_git_file_select_modal_content_spinner', 'large')) // eslint-disable-line no-undef

  xhttp.onload = function () {
    if (xhttp.status === 200) {
      const parent = document.getElementById('id_git_file_select_modal_content')
      if (parent && parent.nodeType) {
        for (let i = 0; i < parent.childNodes.length; i++) {
          if (parent.childNodes[i].tagName !== 'SUMMARY') {
            parent.removeChild(parent.childNodes[i])
          }
        }

        const data = JSON.parse(this.responseText)
        if ({}.propertyIsEnumerable.call(data, 'result')) {
          const html = parseGitObject(data.result.files, 1)
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

    const spinner = document.getElementById('id_git_file_select_modal_content_spinner')
    spinner.parentNode.removeChild(spinner)
  }
  xhttp.open('GET', url, true)
  xhttp.send()
}

/**
 * It opens a modal and then calls a function to get data from the server
 * 
 * Args:
 *   id: The id of the element that will be used to open the modal.
 */
function openGitModal(id) {
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_git_file_select_modal')).show()
  getGitData(id)
}


/**
 * It displays a message to the user asking if they want to select the element they clicked on, and
 * then it displays a submit button that, when clicked, will submit the selection
 *
 * Args:
 *   element: The element that was clicked on.
 */
function selectElement (element) { // eslint-disable-line no-unused-vars
  const selector = returnType.selector // eslint-disable-line no-undef
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
  /* eslint-disable no-undef */
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
    const targetName = document.getElementById('id_name')
    if (targetName !== null) {
      targetName.value = (targetName.value === '') ? element.dataset.targetName : targetName.value
    }
  }
  if (returnType.dataset.target) {
    document.getElementById(returnType.dataset.target).value = element.dataset[returnType.dataset.type]
    document.getElementById(returnType.dataset.target).dispatchEvent(new Event('input'))
  }
  if (returnType.connection.target) {
    document.getElementById(returnType.connection.target).value = element.dataset[returnType.connection.type]
    document.getElementById(returnType.connection.target).dispatchEvent(new Event('input'))
  }
  if (returnType.modal) {
    bootstrap.Modal.getOrCreateInstance(document.getElementById(returnType.modal)).show()
  }
  bootstrap.Modal.getInstance(document.getElementById('connection-modal')).hide()
  /* eslint-enable no-undef */
}
