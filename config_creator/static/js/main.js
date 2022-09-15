/* Creating a map of HTTP status codes and their descriptions. */
const HttpStatusEnum = new Map()
  .set(100, {
    name: 'Continue',
    desc: 'The server has received the request headers, and the client should proceed to send the request body'
  })
  .set(101, {
    name: 'Switching Protocols',
    desc: 'The requester has asked the server to switch protocols'
  })
  .set(103, {
    name: 'Checkpoint',
    desc: 'Used in the resumable requests proposal to resume aborted PUT or POST requests'
  })
  .set(200, {
    name: 'OK',
    desc: 'The request is OK'
  })
  .set(201, {
    name: 'Created',
    desc: 'The request has been fulfilled'
  })
  .set(202, {
    name: 'Accepted',
    desc: 'The request has been accepted for processing'
  })
  .set(203, {
    name: 'Non-Authoritative Information',
    desc: 'The request has been successfully processed'
  })
  .set(204, {
    name: 'No Content',
    desc: 'The request has been successfully processed'
  })
  .set(205, {
    name: 'Reset Content',
    desc: 'The request has been successfully processed'
  })
  .set(206, {
    name: 'Partial Content',
    desc: 'The server is delivering only part of the resource due to a range header sent by the client'
  })
  .set(300, {
    name: 'Multiple Choices',
    desc: 'Indicates multiple options for the resource'
  })
  .set(301, {
    name: 'Moved Permanently',
    desc: 'This and all future requests should be directed to the given URI.'
  })
  .set(302, {
    name: 'Found',
    desc: 'This and all future requests should be directed to the given URI.'
  })
  .set(303, {
    name: 'See Other',
    desc: 'The response to the request can be found under another URI using the GET method.'
  })
  .set(304, {
    name: 'Not Modified',
    desc: 'The resource has not been modified'
  })
  .set(305, {
    name: 'Use Proxy',
    desc: 'The requested resource is available only through a proxy'
  })
  .set(306, {
    name: 'Switch Proxy',
    desc: 'Subsequent requests should use the specified proxy.'
  })
  .set(307, {
    name: 'Temporary Redirect',
    desc: 'The request should be repeated with another URI'
  })
  .set(308, {
    name: 'Permanent Redirect',
    desc: 'This and all future requests should be directed to the given URI.'
  })
  .set(400, {
    name: 'Bad Request',
    desc: 'The request cannot be fulfilled due to bad syntax'
  })
  .set(401, {
    name: 'Unauthorized',
    desc: 'The request was a legal request'
  })
  .set(402, {
    name: 'Payment Required',
    desc: 'Reserved for future use'
  })
  .set(403, {
    name: 'Forbidden',
    desc: 'The request was a legal request'
  })
  .set(404, {
    name: 'Not Found',
    desc: 'The requested page could not be found but may be available again in the future'
  })
  .set(405, {
    name: 'Method Not Allowed',
    desc: 'A request was made of a page using a request method not supported by that page'
  })
  .set(406, {
    name: 'Not Acceptable',
    desc: 'The server can only generate a response that is not accepted by the client'
  })
  .set(407, {
    name: 'Proxy Authentication Required',
    desc: 'The client must first authenticate itself with the proxy'
  })
  .set(408, {
    name: 'Request',
    desc: ' Timeout\tThe server timed out waiting for the request'
  })
  .set(409, {
    name: 'Conflict',
    desc: 'The request could not be completed because of a conflict in the request'
  })
  .set(410, {
    name: 'Gone',
    desc: 'The requested page is no longer available'
  })
  .set(411, {
    name: 'Length Required',
    desc: 'The "Content-Length" is not defined. The server will not accept the request without it'
  })
  .set(412, {
    name: 'Precondition',
    desc: ' Failed. The precondition given in the request evaluated to false by the server'
  })
  .set(413, {
    name: 'Request Entity Too Large',
    desc: 'The server will not accept the request'
  })
  .set(414, {
    name: 'Request-URI Too Long',
    desc: 'The server will not accept the request'
  })
  .set(415, {
    name: 'Unsupported Media Type',
    desc: 'The server will not accept the request'
  })
  .set(416, {
    name: 'Requested Range Not Satisfiable',
    desc: 'The client has asked for a portion of the file'
  })
  .set(417, {
    name: 'Expectation Failed',
    desc: 'The server cannot meet the requirements of the Expect request-header field'
  })
  .set(500, {
    name: 'Internal Server Error',
    desc: 'An error occured processing your request.'
  })
  .set(501, {
    name: 'Not Implemented',
    desc: 'The server does not recognize the request method'
  })
  .set(502, {
    name: 'Bad Gateway',
    desc: 'The server was acting as a gateway or proxy and received an invalid response from the upstream server'
  })
  .set(503, {
    name: 'Service Unavailable',
    desc: 'The server is currently unavailable (overloaded or down)'
  })
  .set(504, {
    name: 'Gateway Timeout',
    desc: 'The server was acting as a gateway or proxy and did not receive a timely response from the upstream server'
  })
  .set(505, {
    name: 'HTTP Version Not Supported',
    desc: 'The server does not support the HTTP protocol version used in the request'
  })
  .set(511, {
    name: 'Network Authentication Required',
    desc: 'The client needs to auth'
  })

/* Adding the class form-control to all the input elements in the document. */
const inputs = document.getElementsByTagName('input')
for (let i = 0; i < inputs.length; i++) {
  if (inputs[i].type === 'checkbox') {
    inputs[i].classList.add('form-check-input')
  } else {
    inputs[i].classList.add('form-control')
  }
}

/* Adding the class "form-control" to all the labels in the form. */
const textarea = document.getElementsByTagName('textarea')
for (let j = 0; j < textarea.length; j++) {
  textarea[j].classList.add('form-control')
}

/* Adding the class form-label to all the label elements in the document. */
const labels = document.getElementsByTagName('label')
for (let k = 0; k < labels.length; k++) {
  labels[k].classList.add('form-label')
}

/* Adding the class form-select to all the select elements in the document. */
const selects = document.getElementsByTagName('select')
for (let l = 0; l < selects.length; l++) {
  selects[l].classList.add('form-select')
}

/* Creating a tooltip for each element that has the attribute data-bs-toggle="tooltip" */
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) { // eslint-disable-line no-unused-vars
  return new bootstrap.Tooltip(tooltipTriggerEl) // eslint-disable-line no-undef
})

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
 * It creates a spinner element
 *
 * Args:
 *   id: the id of the element
 *   type: 'large' or 'small'
 *
 * Returns:
 *   A div element with a spinner inside of it.
 */
function createSpinner (id, type) {
  let div = null
  if (type === 'large') {
    div = createElement('div', null, ['spinner-large-container'], null, id)
    const spinner = createElement('div', null, ['spinner-border', 'text-light', 'spinner-large'], null, null)
    spinner.setAttribute('role', 'status')
    spinner.appendChild(createElement('span', 'Loading...', ['visually-hidden'], null))
    div.appendChild(spinner)
  } else {
    div = createElement('div', null, ['spinner-border', 'text-success', 'spinner-border-sm'], null, id)
    div.setAttribute('role', 'status')
    div.appendChild(createElement('span', 'Loading...', ['visually-hidden'], null))
  }

  return div
}

/**
 * It returns the value of the cookie with the name passed in as a parameter
 *
 * Args:
 *   name: The name of the cookie you want to get.
 *
 * Returns:
 *   The value of the cookie with the name passed in as an argument.
 */
function getCookie (name) {
  const value = `; ${document.cookie}`
  const parts = value.split(`; ${name}=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}

/**
 * It creates a toast element and appends it to the body of the document
 *
 * Args:
 *   message: The message to display in the toast
 *   type: The type of alert you want to show. This can be any of the following:
 *   show: boolean,
 */
function createToast (message, type, show) {
  const outer = document.getElementById('toastPlacement')

  const toastInner = document.createElement('div')
  toastInner.classList.add('toast')

  const toastHeader = document.createElement('div')
  toastHeader.classList.add('toast-header')

  const toastHeaderMessage = document.createElement('strong')
  toastHeaderMessage.classList.add('me-auto')
  toastHeaderMessage.textContent = type

  const toastButton = document.createElement('button')
  toastButton.classList.add('btn-close')
  toastButton.setAttribute('data-bs-dismiss', 'toast')
  toastButton.setAttribute('aria-label', 'Close')
  toastButton.type = 'button'

  toastHeader.appendChild(toastHeaderMessage)
  toastHeader.appendChild(toastButton)

  const toastBody = document.createElement('div')
  toastBody.classList.add('toast-body')
  toastBody.textContent = message

  toastInner.appendChild(toastHeader)
  toastInner.appendChild(toastBody)

  outer.appendChild(toastInner)

  if (show) {
    const toastObj = new bootstrap.Toast(toastInner) // eslint-disable-line no-undef
    toastObj.show()
  }
}

/**
 * It makes an AJAX call to the server, and if the server returns a message, it displays it to the user
 *
 * Args:
 *   url: The url to call
 *   method: The HTTP method to use.
 *   spinnerElementId: The id of the element that will contain the spinner.
 *   spinnerType: The type of spinner to show. This is a string that can be one of the following:
 */
function callModelApi (url, method, spinnerElementId, spinnerType) {
  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef
  let spinnerId
  if (spinnerElementId) {
    const parent = document.getElementById(spinnerElementId)
    spinnerId = spinnerElementId + '_spinner'
    if (parent.children.length > 0) {
      parent.children[0].appendChild(createSpinner(spinnerId, spinnerType))
    } else {
      parent.appendChild(createSpinner(spinnerId, spinnerType))
    }
  }
  xhttp.responseType = 'json'
  xhttp.onload = function () {
    if (spinnerId) {
      const spinner = document.getElementById(spinnerId)
      /* eslint-disable no-undef */
      if (parent && parent.nodeType) {
        parent.removeChild(spinner)
      }
      /* eslint-enable no-undef */
    }

    const data = xhttp.response
    if ((xhttp.status === 200 || xhttp.status === 404) && 'message' in data) {
      createToast(data.message, data.type, true)
    } else {
      const message = HttpStatusEnum.get(xhttp.status)
      createToast(message.desc, message.name, true)
    }
  }

  if (!method) {
    method = 'GET'
  }
  xhttp.open(method, url, true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken'))
  xhttp.send()
}

/**
 * It deletes a model object, and if the element to remove is a table row, it adds a class to it to
 * make it fade out, otherwise it removes the element
 *
 * Args:
 *   url: The url to call
 *   elementToRemoveId: The id of the element to remove from the DOM.
 *   spinnerTargetId: The id of the element that the spinner should be displayed on.
 *   spinnerType: The type of spinner to show. This can be either 'small' or 'large'.
 */
function deleteModelObject (url, elementToRemoveId, spinnerTargetId, spinnerType) { // eslint-disable-line no-unused-vars
  if (confirm('Are you sure you want to delete this?')) { // eslint-disable-line no-undef
    callModelApi(url, 'DELETE', spinnerTargetId, spinnerType)
    const element = document.getElementById(elementToRemoveId)
    if (element.tagName === 'TR') {
      element.classList.add('delete-row')
    } else {
      element.parentNode.removeChild(element)
    }
  }
}

/**
 * It creates an object that can be used to create a row in a table
 *
 * Args:
 *   classList: An array of classes to be added to the row.
 *   id: The id of the row.
 *   content: an array of objects that will be used to create the row's content.
 *   value: The value of the row.
 *   object: The object that will be used to create the row.
 *   attributes: an array of tuples containing any attribute name and value you want to add to the row.
 *
 * Returns:
 *   An object with the properties classList, id, content, value, and object.
 */
function createRowObject (classList, id, content, value, object, attributes) { // eslint-disable-line no-unused-vars
  let cL = []
  let i = ''
  let c = []
  let a = []
  let v = ''
  let o = {}

  if (classList) {
    cL = classList
  }

  if (id) {
    i = id
  }

  if (content) {
    c = content
  }

  if (attributes) {
    a = attributes
  }

  if (value) {
    v = value
  }

  if (object) {
    o = object
  }

  const obj = {
    classList: cL,
    id: i,
    attributes: a
  }

  if (content) {
    obj.content = c
  } else if (value) {
    obj.value = v
  } else if (object) {
    obj.object = o
  }
  return obj
}

/**
 * It takes an array of objects, each object containing an array of objects, and creates a table row
 * for each object in the first array, and a table cell for each object in the second array
 *
 * Args:
 *   data: an array of objects that contain the data for each row.
 *   parent: The parent element to append the row to.
 *   position: The position of the row in the table. If you want to add a row to the top of the table,
 * you would use 1. If you want to add a row to the bottom of the table, you would use the number of
 * rows in the table + 1.
 */
function addRow (data, parent, position) { // eslint-disable-line no-unused-vars
  for (let i = 0; i < data.length; i++) {
    const row = createElement('tr', null, data[i].classList, null, data[i].id)

    if (data[i].attributes) {
      for (let a = 0; a < data[i].attributes.length; a++) {
        row.setAttribute(data[i].attributes[a][0], data[i].attributes[a][1])
      }
    }

    const content = data[i].content

    for (let j = 0; j < content.length; j++) {
      const td = createElement('td', null, content[j].classList, null, content[j].id)

      if ('value' in content[j]) {
        td.textContent = content[j].value
      } else if ('object' in content[j]) {
        td.appendChild(content[j].object)
      }

      if (content[j].attributes) {
        for (let a = 0; a < content[j].attributes.length; a++) {
          td.setAttribute(content[j].attributes[a][0], content[j].attributes[a][1])
        }
      }

      row.appendChild(td)
    }
    if (position && position !== '' && position !== undefined && position !== 'null' && position !== null && position !== 'undefined') {
      parent.insertBefore(row, parent.children[position - 1])
    } else {
      parent.appendChild(row)
    }
  }
}

/**
 * It creates a Bootstrap toast element, appends it to the DOM, and then shows it
 *
 * Args:
 *   message: The message to display in the toast
 *   parentId: The id of the parent element to append the toast to. If not provided, the toast will be
 * appended to the body.
 */
function alertMessage (message, parentId) {
  const wrapper = createElement('div', null, ['toast-container', 'position-absolute', 'p-3', 'top-0', 'start-50', 'translate-middle-x'])
  const toastInner = createElement('div', null, ['toast', 'text-white', 'bg-secondary', 'border-0'])
  const toastBody = createElement('div', message, ['toast-body', 'text-center'])

  toastInner.appendChild(toastBody)
  wrapper.appendChild(toastInner)

  if (parentId) {
    document.getElementById(parentId).appendChild(wrapper)
  } else {
    document.body.appendChild(wrapper)
  }

  const toastObj = new bootstrap.Toast(toastInner) // eslint-disable-line no-undef
  toastObj.show()
}

/**
 * It takes a string and a parent element id, and then copies the string to the clipboard and displays
 * a message to the user
 *
 * Args:
 *   text: The text to copy to the clipboard
 *   parentId: The id of the parent element that the alert message will be appended to.
 */
async function textToClipboard (text, parentId) { // eslint-disable-line no-unused-vars
  await navigator.clipboard.writeText(text)
  alertMessage('Copied to clipboard!', parentId)
}
