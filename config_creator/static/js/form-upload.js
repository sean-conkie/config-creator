'use strict'

const labels = document.getElementsByTagName('label')
console.log(labels)
for (let i = 0; i < labels.length; i++) {
  console.log(i + ':' + labels.length)
  if (labels[i].htmlFor != '' && labels[i].id != 'file-label') { labels[i].remove() }
  i--
  if (labels.length == 1) { break }
  // labels[i].setAttribute("hidden", true);
}

;
(function (document, window, index) {
  // feature detection for drag&drop upload
  const isAdvancedUpload = (function () {
    const div = document.createElement('div')
    return (('draggable' in div) || ('ondragstart' in div && 'ondrop' in div)) && 'FormData' in window && 'FileReader' in window
  }())

  // applying the effect for every form
  const forms = document.querySelectorAll('.box')
  Array.prototype.forEach.call(forms, function (form) {
    const input = form.querySelector('input[type="file"]')
    const label = form.querySelector('label')
    const errorMsg = form.querySelector('.box__error span')
    const restart = form.querySelectorAll('.box__restart')
    let droppedFiles = false
    const showFiles = function (files) {
      label.textContent = files.length > 1 ? (input.getAttribute('data-multiple-caption') || '').replace('{count}', files.length) : files[0].name
      document.getElementById('id_title').value = files[0].name
    }
    const triggerFormSubmit = function () {
      const event = document.createEvent('HTMLEvents')
      event.initEvent('submit', true, false)
      form.dispatchEvent(event)
    }

    // automatically submit the form on file select
    input.addEventListener('change', function (e) {
      showFiles(e.target.files)
    })

    // drag&drop files if the feature is available
    if (isAdvancedUpload) {
      form.classList.add('has-advanced-upload'); // letting the CSS part to know drag&drop is supported by the browser

      ['drag', 'dragstart', 'dragend', 'dragover', 'dragenter', 'dragleave', 'drop'].forEach(function (event) {
        form.addEventListener(event, function (e) {
          // preventing the unwanted behaviours
          e.preventDefault()
          e.stopPropagation()
        })
      });
      ['dragover', 'dragenter'].forEach(function (event) {
        form.addEventListener(event, function () {
          form.classList.add('is-dragover')
        })
      });
      ['dragleave', 'dragend', 'drop'].forEach(function (event) {
        form.addEventListener(event, function () {
          form.classList.remove('is-dragover')
        })
      })
      form.addEventListener('drop', function (e) {
        droppedFiles = e.dataTransfer.files // the files that were dropped
        showFiles(droppedFiles)
      })
    }

    // if the form was submitted
    form.addEventListener('submit', function (e) {
      // preventing the duplicate submissions if the current one is in progress
      if (form.classList.contains('is-uploading')) return false

      form.classList.add('is-uploading')
      form.classList.remove('is-error')
    })

    // restart the form if has a state of error/success
    Array.prototype.forEach.call(restart, function (entry) {
      entry.addEventListener('click', function (e) {
        e.preventDefault()
        form.classList.remove('is-error', 'is-success')
        input.click()
      })
    })

    // Firefox focus bug fix for file input
    input.addEventListener('focus', function () {
      input.classList.add('has-focus')
    })
    input.addEventListener('blur', function () {
      input.classList.remove('has-focus')
    })
  })
}(document, window, 0))
