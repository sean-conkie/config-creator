var functionObject = {}

/**
 * It prepares the field transformation modal by populating the function type select and setting the
 * field string
 */
function prepareFieldTransformationModal () {
  const field = document.getElementById('id_name').value
  const sourceTable = document.getElementById('id_source_name').value
  const match = sourceTable.match(/([\w\d\-]+)\s*([\w\d]+)$/)
  const transformation = document.getElementById('id_field_transformation').value

  let fieldString

  if (transformation) {
    fieldString = transformation
  } else if (match && field) {
    fieldString = `${match[2]}.${field}`
  } else if (field && sourceTable) {
    fieldString = `${sourceTable}.${field}`
  } else if (field) {
    fieldString = `${field}`
  } else {
    fieldString = ''
  }

  document.getElementById('id_modal_field_transformation').textContent = fieldString
  update(fieldString, 'id_field_transformation_modal_highlighting')
  document.getElementById('id_modal_field_transformation').classList.remove('form-control')

  
  tAreaPosStart = 0
  tAreaPosEnd = 0

  document.getElementById('id_function_type').textContent = ''
  document.getElementById('id_function').textContent = ''
  document.getElementById('id_function_container').textContent = ''
  
  const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef

  xhttp.responseType = 'json'
  xhttp.onload = function () {
    const data = xhttp.response
    if (xhttp.status === 200) {

      const types = data.result
      populateFunctionSelect('id_function_type', types)

    }
  }

  xhttp.open('GET', '/api/function/type/', true)
  xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
  xhttp.send()

  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_field_modal')).hide() // eslint-disable-line no-undef
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_field_transformation_modal')).show() // eslint-disable-line no-undef
}

/**
 * It closes the field transformation modal and shows the field modal
 */
function closeFieldTransformationModal () {
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_field_transformation_modal')).hide() // eslint-disable-line no-undef
  bootstrap.Modal.getOrCreateInstance(document.getElementById('id_field_modal')).show() // eslint-disable-line no-undef
}

/**
 * > When the user selects a function type, the function will populate the function select with the
 * functions of that type
 * 
 * Args:
 *   selectedType: The selected type of function.
 */
function switchFunctionType(selectedType) {
  if (!selectedType) {
    return
  }

  const spinnerId = 'id_function_spinner'

  const parent = document.getElementById('id_function').parentNode
  functionObject["type"] = selectedType

  if ( !{}.propertyIsEnumerable.call(functionObject, selectedType)) {
    parent.style.position = 'relative'
    parent.appendChild(createSpinner(spinnerId, 'large')) // eslint-disable-line no-undef
    parent.setAttribute('disabled', 'true')
        
    const xhttp = new XMLHttpRequest() // eslint-disable-line no-undef
    xhttp.responseType = 'json'
    xhttp.onload = function () {
      const data = xhttp.response
      
    
      if (xhttp.status === 200) {
        const types = data.result
        functionObject[`${functionObject.type}`] = types
        populateFunctionSelect('id_function', types)
      }
      
      if (spinnerId) {
        const spinner = document.getElementById(spinnerId)
        if (parent && parent.nodeType) {
          parent.removeChild(spinner)
          parent.removeAttribute('disabled')
        }
      }
    }

    xhttp.open('GET', `/api/function/type/${selectedType}/`, true)
    xhttp.setRequestHeader('X-CSRFToken', getCookie('csrftoken')) // eslint-disable-line no-undef
    xhttp.send()

  } else {
    populateFunctionSelect('id_function', functionObject[`${selectedType}`])
  }
}

/**
 * It takes a function name and a function type as parameters, and returns the function with the given
 * name and type
 * 
 * Args:
 *   functionName: The name of the function you want to get.
 *   functionType: This is the type of function you want to get.
 * 
 * Returns:
 *   The function object
 */
function getFunction(functionName, functionType) {
  for (i = 0; functionObject[`${functionType}`].length; i++) {
    let func = functionObject[`${functionType}`][i]
    if (func.name === functionName) {
      return func
    }
  }
}

/**
 * It creates a row with a label and an input element
 * 
 * Args:
 *   label: The label for the input
 *   value: the value of the input
 *   inputType: the type of input you want to create.
 *   inputClass: This is the class that will be applied to the input element.
 *   inputId: The id of the input element
 * 
 * Returns:
 *   A row with a label and input
 */
function createFunctionRow(label, value, inputType, inputClass, inputId) {
  const row = createElement('div', null, ['row', 'g-3', 'py-1'])
  const col = createElement('div', null, ['col-12'])
  const group = createElement('div', null, ['form-floating'])
  const labelElement = createElement('label', label, ['form-label'])
  const input = createElement(`${inputType}`, value, ['form-control', `${inputClass}`], 0, inputId)

  input.value = value
  input.setAttribute('disabled', 'true')

  group.appendChild(input)
  group.appendChild(labelElement)

  col.appendChild(group)

  row.appendChild(col)

  return row

}

/**
 * It takes the selected function from the dropdown and displays the details of that function in the
 * form
 * 
 * Args:
 *   selectedFunction: The name of the function that was selected from the dropdown.
 * 
 * Returns:
 *   the function object.
 */
function displayFunction(selectedFunction) {
  
  if (!selectedFunction) {
    return
  }

  const parent = document.getElementById('id_function_container')

  const functionDetail = getFunction(selectedFunction, functionObject.type)

  const btnRow = createElement('div', null, ['row', 'g-3', 'py-1'])
  const btnGroup = createElement('div', null, ['btn-group'])
  btnGroup.setAttribute('role', 'group')
  const copyBtn = createElement('button', null,['alt-btn', 'btn-primary'], null, 'id_button_copy_syntax')
  copyBtn.appendChild(createElement('i', null, ['fa-regular', 'fa-copy']))
  copyBtn.addEventListener('click', function() {
    copySyntax()
  })
  const insertBtn = createElement('button', null,['alt-btn', 'btn-primary'])
  insertBtn.appendChild(createElement('i', null, ['bi', 'bi-input-cursor-text']))
  insertBtn.addEventListener('click', function () {
    insertCode()
  })
  const wrapBtn = createElement('button', null,['alt-btn', 'btn-primary'])
  wrapBtn.appendChild(createElement('i', null, ['bi', 'bi-braces']))
  wrapBtn.addEventListener('click', function() {
    wrapCode()
  })
  btnGroup.appendChild(copyBtn)
  btnGroup.appendChild(insertBtn)
  btnGroup.appendChild(wrapBtn)
  btnRow.appendChild(btnGroup)

  const nameRow = createFunctionRow('Function Name', functionDetail.name, 'input', null, 'id_function_name')
  const syntaxRow = createFunctionRow('Syntax', functionDetail.syntax, 'input', 'code', 'id_function_syntax')
  const returnRow = createFunctionRow('Return Type', functionDetail.return_type, 'input', null, 'id_function_return_type')
  const descRow = createFunctionRow('Description', functionDetail.description, 'textarea', null, 'id_function_description')

  document.getElementById('id_function_container').textContent = ''

  parent.appendChild(btnRow)
  parent.appendChild(nameRow)
  parent.appendChild(syntaxRow)
  parent.appendChild(returnRow)
  parent.appendChild(descRow)
  
  document.getElementById('id_function_description').setAttribute("style", "height:" + (document.getElementById('id_function_description').scrollHeight) + "px;overflow-y:hidden;")

}

/**
 * It takes an array of objects, and creates an HTML option element for each object, and appends it to
 * the target element
 * 
 * Args:
 *   targetId: The id of the select element you want to populate
 *   content: an array of objects, each object has a name and an id
 */
function populateFunctionSelect(targetId, content) {
  const targetElement = document.getElementById(targetId)
  targetElement.textContent = ''

  for (i = 0; i < content.length; i++) {
    let opt = createElement('option', content[i].name)
    opt.setAttribute('value', content[i].id)
    targetElement.appendChild(opt)
  }
}


/**
 * The functionDescriptionReSize() function is used to resize the textarea element to fit the content.
 */
function functionDescriptionReSize() {
  this.style.height = 0;
  this.style.height = (this.scrollHeight) + "px";
}

/**
 * It returns the value of the textarea with the id "id_function_syntax" in lowercase
 * 
 * Returns:
 *   The value of the element with the id of id_function_syntax.
 */
function getSyntax() {
  return document.getElementById('id_function_syntax').value.toLowerCase()
}

/**
 * * The function `copySyntax()` is called when the user clicks on the button with the id
 * `id_button_copy_syntax`.
 * * The function `copySyntax()` calls the function `textToClipboard()` with the following parameters:
 *   * The value of the textarea with the id `id_function_syntax`
 *   * The id of the textarea where the user will be notified that the syntax has been copied to the
 * clipboard.
 * * The function `textToClipboard()` copies the text to the clipboard and notifies the user
 */
function copySyntax() {
  textToClipboard(getSyntax(), 'id_field_transformation_modal')
}

/**
 * It takes the string in the textarea, finds the first word in the syntax, and replaces it with the
 * string in the textarea
 */
function wrapCode() {
  const string = document.getElementById('id_modal_field_transformation').value
  const match = getSyntax().match(/\w+\((\b\w+)\b/)
  let newString

  if (match) {
    newString = getSyntax().replace(match[1], string)
  } else {
    newString = `${getSyntax()}${string}`
  }
  document.getElementById('id_modal_field_transformation').textContent = newString
  update(newString, 'id_field_transformation_modal_highlighting')

}

let tAreaPosStart = 0
let tAreaPosEnd = 0

const tArea = document.getElementById('id_modal_field_transformation')
tArea.addEventListener('click', function() {
  tAreaPosStart = tArea.selectionStart
  tAreaPosEnd = tArea.selectionEnd
  console.log(`click: ${tAreaPosStart}-${tAreaPosEnd}`)
})
tArea.addEventListener('change', function() {
  tAreaPosStart = tArea.selectionStart
  tAreaPosEnd = tArea.selectionEnd
  console.log(`change: ${tAreaPosStart}-${tAreaPosEnd}`)
})

/**
 * It takes the text from the textarea, finds the selected text, and inserts it into the syntax
 */
function insertCode() {
  const string = document.getElementById('id_modal_field_transformation').value
  const match = getSyntax().match(/\w+\((\b\w+)\b/)
  let newString

  if (tAreaPosStart === tAreaPosEnd) {
    tAreaPosEnd = string.length
  }

  const codeStringLength = tAreaPosEnd - tAreaPosStart

  const codeString = string.substr(tAreaPosStart, codeStringLength)

  if (match) {
    newString = getSyntax().replace(match[1], codeString)
  } else {
    newString = `${getSyntax()}${codeString}`
  }

  const finalString = string.replace(codeString, newString)

  document.getElementById('id_modal_field_transformation').textContent = finalString
  update(finalString, 'id_field_transformation_modal_highlighting')

}

/**
 * It takes the string from the modal, splits it into an array, and then loops through the array to
 * lowercase all the words except for the ones in single quotes
 */
function saveTransformation() {
  const splitString = document.getElementById('id_modal_field_transformation').value.split(' ')
  let transformationString = ''

  for (i = 0; i < splitString.length; i++) {
    let match = splitString[i].match(/\'.*\'|\".*\"/)
    if (match) {
      transformationString += `${splitString[i]} `
    } else {
      transformationString += `${splitString[i].toLowerCase()} `
    }
  }
  
  document.getElementById('id_field_transformation').textContent = transformationString
  update(transformationString, 'id_field_transformation_highlighting')

  closeFieldTransformationModal()
}