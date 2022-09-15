function dropHandler (ev) {
  // Prevent default behavior (Prevent file from being opened)
  ev.preventDefault()

  if (ev.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    for (let i = 0; i < ev.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (ev.dataTransfer.items[i].kind === 'file') {
        const file = ev.dataTransfer.items[i].getAsFile()
        document.getElementById('id_title').value = file.name
        document.getElementById('id_file-label').textContent = file.name
        const formData = new FormData() // eslint-disable-line no-undef
        formData.append('file', file)
        formData.append('title', file.name)

        const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef
        const spinnerId = 'id_drop_zone_spinner'
        const parent = document.getElementById('id_drop_zone_form')
        parent.appendChild(createSpinner(spinnerId, 'large')) // eslint-disable-line no-undef

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
          if (xhttp.status === 200) {
            location.href = data.result // eslint-disable-line no-undef
          } else {
            const message = HttpStatusEnum.get(xhttp.status) // eslint-disable-line no-undef
            createToast(message.desc, message.name, true) // eslint-disable-line no-undef
          }
        }

        xhttp.open('POST', '/api/file/upload/', true)
        xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
        xhttp.send(formData)
      }
    }
  } else {
    alert('Oops! You\'re still using Internet Explorer?') // eslint-disable-line no-undef
  }
}

function dragStart () {
  document.getElementById('id_drop_zone_form').classList.add('box-hover')
}

function dragEnd (e) {
  document.getElementById('id_drop_zone_form').classList.remove('box-hover')
}

document.getElementById('id_drop_zone_form').addEventListener('dragover', (event) => {
  event.preventDefault()
  dragStart()
})

document.getElementById('id_drop_zone_form').addEventListener('dragleave', (event) => {
  dragEnd()
})

document.getElementById('id_drop_zone_form').addEventListener('drop', (event) => {
  dragEnd()
  dropHandler(event)
})
