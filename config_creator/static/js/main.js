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
    desc: 'The request is OK (this is the standard response for successful HTTP requests)'
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
    desc: 'A generic error message'
  })
  .set(501, {
    name: 'Not Implemented',
    desc: 'The server either does not recognize the request method'
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
for (var i = 0; i < inputs.length; i++) {
  if (inputs[i].type == 'checkbox') {
    inputs[i].classList.add('form-check-input')
  } else {
    inputs[i].classList.add('form-control')
  }
}

/* Adding the class "form-control" to all the labels in the form. */
const textarea = document.getElementsByTagName('textarea')
for (var i = 0; i < textarea.length; i++) {
  textarea[i].classList.add('form-control')
}

/* Adding the class form-label to all the label elements in the document. */
const labels = document.getElementsByTagName('label')
for (var i = 0; i < labels.length; i++) {
  labels[i].classList.add('form-label')
}

/* Adding the class form-select to all the select elements in the document. */
const selects = document.getElementsByTagName('select')
for (var i = 0; i < selects.length; i++) {
  selects[i].classList.add('form-select')
}

/* Creating a tooltip for each element that has the attribute data-bs-toggle="tooltip" */
const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})

/**
 * It creates a div element with the id of the parameter passed in, adds the classes "spinner-border",
 * "text-success", and "spinner-border-sm" to the div, and then adds a span element with the text
 * "Loading..." and the class "visually-hidden" to the div
 *
 * Args:
 *   id: The id of the element
 *
 * Returns:
 *   A div element with a spinner-border class, text-success class, spinner-border-sm class, and a role
 * attribute of status.
 */
function createSpinner (id) {
  const div = createElement('div', null, ['spinner-border', 'text-success', 'spinner-border-sm'], null, id)
  div.setAttribute('role', 'status')
  div.appendChild(createElement('span', 'Loading...', ['visually-hidden'], null))
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
 * It creates an element of the type specified, with the content specified, with the classes specified,
 * with the layer specified, and with the id specified
 *
 * Args:
 *   type: the type of element to create (e.g. "div", "p", "span", etc.)
 *   content: The text content of the element.
 *   classList: an array of class names to add to the element
 *   layer: the layer of the element. This is used to indent the element.
 *   id: The id of the element.
 *
 * Returns:
 *   A DOM element.
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
 * It creates a toast element and appends it to the body of the document
 *
 * Args:
 *   message: The message to display in the toast
 *   type: The type of alert you want to show. This can be any of the following:
 *   show: boolean,
 */
function createToast (message, type, show) {
  const doc = document.getElementsByTagName('body')[0]

  const outer = document.getElementById('toastPlacement')

  const toastInner = document.createElement('div')
  toastInner.classList.add('toast')
  toastInner.classList.add('alert-' + type)

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
    const toastObj = new bootstrap.Toast(toastInner)
    toastObj.show()
  }
}

/**
 * It makes an AJAX request to the server, and if the request is successful, it calls the callback
 * function
 *
 * Args:
 *   url: The url to call
 *   method: The HTTP method to use.
 *   spinnerElementId: The id of the element that will contain the spinner.
 */
function callModelApi (url, method, spinnerElementId) {
  const xhttp = new XMLHttpRequest()
  let spinnerId
  if (spinnerElementId) {
    const parent = document.getElementById(modal_id)
    spinnerId = spinnerElementId + '_spinner'
    if (parent.children.length > 0) {
      parent.children[0].appendChild(createSpinner(spinnerId))
    } else {
      parent.appendChild(createSpinner(spinnerId))
    }
  }
  xhttp.responseType = 'json'
  xhttp.onload = function () {
    if (spinnerId) {
      const spinner = document.getElementById(spinnerId)
      if (parent && parent.nodeType) {
        parent.removeChild(spinner)
      }
    }

    data = xhttp.response
    if ((xhttp.status == 200 || xhttp.status == 404) && 'message' in data) {
      createToast(data.message, data.type, true)
    } else {
      message = HttpStatusEnum.get(xhttp.status)
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
 * make it fade out
 *
 * Args:
 *   url: The url to call.
 *   elementToRemoveId: The id of the element to remove from the DOM.
 *   spinnerTargetId: The id of the element that will be the target of the spinner.
 */
function deleteModelObject (url, elementToRemoveId, spinnerTargetId) {
  if (confirm('Are you sure you want to delete this?')) {
    callModelApi(url, 'DELETE', spinnerTargetId)
    const element = document.getElementById(elementToRemoveId)
    if (element.tagName == 'TR') {
      element.classList.add('delete-row')
    } else {
      element.parentNode.removeChild(element)
    }
  }
}

/**
 * It takes in a classList, id, content, and value, and returns an object with the classList and id,
 * and either the content or value
 *
 * Args:
 *   classList: an array of classes to be added to the row
 *   id: the id of the row
 *   content: an array of objects that will be used to create the row's cells.
 *   value: The value of the input.
 *
 * Returns:
 *   An object with the properties classList, id, content, and value.
 */
function createRowObject (classList, id, content, value, object) {
  let cL = []
  let i = ''
  let c = []
  let v = ''

  if (classList) {
    cL = classList
  }

  if (id) {
    i = id
  }

  if (content) {
    c = content
  }

  if (value) {
    v = value
  }

  if (object) {
    o = object
  }

  const obj = {
    classList: cL,
    id: i
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
 * It takes an array of objects, each object representing a row, and each object containing an array of
 * objects, each object representing a cell, and each object containing a classList, id, and value, and
 * it adds the rows and cells to the parent element
 *
 * Args:
 *   data: an array of objects, each object representing a row in the table.
 *   parent: the parent element to append the row to
 */
function addRow (data, parent) {
  for (let i = 0; i < data.length; i++) {
    const row = createElement('tr', null, data[i].classList, null, data[i].id)

    const content = data[i].content

    for (let j = 0; j < content.length; j++) {
      const td = createElement('td', null, content[j].classList, null, content[j].id)

      if ('value' in content[j]) {
        td.textContent = content[j].value
      } else if ('object' in content[j]) {
        td.appendChild(content[j].object)
      }

      row.appendChild(td)
    }

    parent.appendChild(row)
  }
}
