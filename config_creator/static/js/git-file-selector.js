
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
  const detail = createElement('details', null, ['tree-dir'], layer, null) // eslint-disable-line no-undef

  if ({}.propertyIsEnumerable.call(object, 'name')) {
    const summary = createElement('summary', null, ['tree-dir-summary'], null, null) // eslint-disable-line no-undef
    summary.appendChild(createElement('i', null, ['fa-solid', 'fa-folder-open'], null, null)) // eslint-disable-line no-undef
    summary.insertAdjacentText('beforeend', '\xa0' + object.name)
    detail.appendChild(summary)
  }

  if ({}.propertyIsEnumerable.call(object, 'files')) {
    const child = parseGitObject(object.files, layer + 1)
    if (child) {
      detail.appendChild(child)
    }
  }

  return detail
}

/**
 * It takes an array of objects, and returns a DOM element
 * 
 * Args:
 *   arr: The array of objects to be parsed
 *   layer: the layer of the element in the tree
 * 
 * Returns:
 *   A div element with the class 'modal-container'
 */
function parseGitObject (arr, layer) {
  if (arr.length === 0) {
    return createElement('div', null, ['modal-container'], null, null) // eslint-disable-line no-undef
  }
  const element = createElement('div', null, ['modal-container'], null, null) // eslint-disable-line no-undef
  for (let i = 0; i < arr.length; i++) {
    if ({}.propertyIsEnumerable.call(arr[i], 'type')) {
      let html
      if (arr[i].type === 'dir') {
        html = createGitDirectory(arr[i], layer)
      } else if (arr[i].type === 'file' && /(?:\.([^.]+))?$/.exec(arr[i].name)[1] === 'json') {
        html = createElement('div', null, ['tree-file-json']) // eslint-disable-line no-undef
        let fileIcon = createElement('i', null, ['fa-solid', 'fa-file-code'], layer, null) // eslint-disable-line no-undef
        html.appendChild(fileIcon)
        html.insertAdjacentText('beforeend', '\xa0' + arr[i].name)
        html.dataset['filePath'] = arr[i].path
        html.dataset['fileName'] = arr[i].name
        html.addEventListener('click', function () {
          selectGitElement(this)
        })
      } else if (arr[i].type === 'file') {
        html = createElement('div', null, ['tree-file']) // eslint-disable-line no-undef
        let fileIcon = createElement('i', null, ['fa-solid', 'fa-file-circle-xmark'], layer, null) // eslint-disable-line no-undef
        html.appendChild(fileIcon)
        html.insertAdjacentText('beforeend', '\xa0' + arr[i].name)
        html.addEventListener('click', function () {
          unSelectGitElement()
        })
      }

      if (typeof html !== 'undefined') {
        element.appendChild(html)
      }
    }
  }
  return element
}

/**
 * It takes an object with a `current` property and a bunch of other properties, and it creates a
 * `<select>` element with an `<option>` for each of the other properties, and it sets the `value`
 * attribute of the `<option>` to the name of the property, and it sets the `selected` attribute of the
 * `<option>` to `true` if the name of the property is the same as the value of the `current` property
 * 
 * Args:
 *   obj: The object that contains the branch information.
 */
function parseBranches(obj) {
  const keys = Object.keys(obj)
  const current = obj.current
  const select = document.getElementById('id_branch')
  select.textContent = ''

  for (let i = 0; i < keys.length; i ++) {
    if (keys[i] !== 'current') {
      const option = createElement('option', keys[i])
      option.value = keys[i]
      if (keys[i] === obj.current) {
        option.setAttribute('selected', 'true')
      }
      select.appendChild(option)
    }
  }

  document.getElementById('id_branch_wrapper').classList.remove('visually-hidden')
}

/**
 * It gets the value of the branch input field, and then calls the getGitData function with the id and
 * branch as arguments
 * 
 * Args:
 *   id: The id of the element that will be populated with the data
 */
function submitBranch(id) {
  const branch = document.getElementById('id_branch').value.replace(/\//g, '%2F')
  document.getElementById('id_branch_wrapper').classList.add('visually-hidden')
  getGitData(id, branch)
  unSelectGitElement()
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

          document.getElementById('id_submit_branch').dataset['repoId'] = id

          parseBranches(data.result.branches)
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
function openGitModal (id) { // eslint-disable-line no-unused-vars
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_git_file_select_modal')).show() // eslint-disable-line no-undef
  getGitData(id)
}

/**
 * It displays a message to the user asking if they want to select the element they clicked on, and
 * then it displays a submit button that, when clicked, will submit the selection
 *
 * Args:
 *   element: The element that was clicked on.
 */
function selectGitElement (element) { // eslint-disable-line no-unused-vars
  const path = element.dataset.filePath.replace(/\//g, '%2F')
  const name = element.dataset.fileName
  message = `Would you like to load '${name}'?`

  document.getElementById('id_selection').textContent = message

  const submitButton = createElement('a', 'Load', ['btn', 'btn-primary'], null,'id_git_file_select_modal_submit_button')
  submitButton.setAttribute('href',`/file/${path}/upload/`)
  document.getElementById('id_selection_wrapper').appendChild(submitButton)
}

/**
 * It removes the submit button from the modal
 */
function unSelectGitElement () {
  document.getElementById('id_selection').textContent = ''
  const submitButton = document.getElementById('id_git_file_select_modal_submit_button')
  submitButton.parentNode.removeChild(submitButton)
}

