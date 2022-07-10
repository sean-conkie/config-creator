
  function createElement(type, content, classList, layer, id) {
    let outer = document.createElement(type);
    if (content) {
      outer.textContent = content;
    }
    
    if (classList) {
      for (var i = 0; i < classList.length; i++) {
        outer.classList.add(classList[i]);
      }
    }

    if (layer) {
      outer.style.marginLeft = (layer * 20) + "px";
    }

    if (id) {
      outer.setAttribute("id", id);
    }

    return outer;
  }

  function createColumnElement(object, layer) {
    let row = createElement("tr", null, null, null, null);
    let column_name = createElement("td", object["column_name"], ["tree-table-select"], null, null);
    column_name.setAttribute("onclick", "selectElement(this)");
    column_name.setAttribute("data-column-name", object["column_name"]);
    column_name.setAttribute("data-column-full", object["dataset"] + "." + object["table_name"] + "." + object["column_name"]);
    column_name.setAttribute("data-table-name", object["table_name"]);
    column_name.setAttribute("data-table-full", object["dataset"] + "." + object["table_name"]);
    column_name.setAttribute("data-dataset-name", object["dataset"]);
    let id = "id_connection_" + object["connection_id"] + "_dataset_" + object["dataset"] + "_" + object["table_name"] + "_" + object["column_name"];    
    column_name.setAttribute("id", id);
    let data_Type = createElement("td", object["data_type"], null, null, null);
    let mode;
    if (object["is_nullable"]) {
      mode = createElement("td", "NULLABLE", null, null, null);
    }
    else {
      mode = createElement("td", "REQUIRED", null, null, null);
    }
    
    row.appendChild(column_name);
    row.appendChild(data_Type);
    row.appendChild(mode);
    return row;
  }

  function createTableElement(object, layer) {
    let element;
    if (returnType["selector"] == "table") {
      element = createElement("div", null, ["tree-table-select"], layer * 10, null);
    }
    else {
      element = createElement("details", null, ["tree-table"], layer * 10, null);
    }

    if (object.hasOwnProperty("name")) {
      let id = "id_connection_" + object["connection_id"] + "_dataset_" + object["dataset"] + "_" + object["name"];    
      element.setAttribute("id", id);
      
      if (returnType["selector"] == "table") {
        element.setAttribute("onclick", "selectElement(this)");
        element.insertAdjacentText("beforeend", " " + object["name"]);
        element.setAttribute("data-table-name", object["name"]);
        element.setAttribute("data-table-full", object["dataset"] + "." + object["name"]);
        element.setAttribute("data-dataset-name", object["dataset"]);
        element.setAttribute("data-connection-id", object["connection_id"]);
      }
      else {
        let summary = createElement("summary", null, ["tree-table-summary"], null, null);
        summary.appendChild(createElement("i", null, ["fa-solid", "fa-table"], null, null));
        summary.insertAdjacentText("beforeend", " " + object["name"]);
        element.appendChild(summary);
        let layerInner = layer + 1;
        
        let table = createElement("table", null, ["table","table-striped", "table-hover"], layerInner, null);

        if (object.hasOwnProperty("content")) {
          let child = parseObject(object["content"], layerInner, null);
          if (child) {
            table.appendChild(child);
          }
        }

        element.appendChild(table);
      }
    }
    return element;
  }

  function createDatasetElement(object, layer) {
    let element
    if (returnType["selector"] == "dataset") {
      element = createElement("div", null, ["tree-dataset-select"], layer * 10, null);
    }
    else {
      element = createElement("details", null, ["tree-dataset"], layer * 10, null);
    }
    
    if (object.hasOwnProperty("name")) {
      let id = "id_connection_" + object["connection_id"] + "_dataset_" + object["name"];    
      element.setAttribute("id", id);

      if (returnType["selector"] == "dataset") {
        element.setAttribute("onclick", "selectElement(this)");
        element.insertAdjacentText("beforeend", " " + object["name"]);
        element.setAttribute("data-dataset-name", object["name"]);
        element.setAttribute("data-connection-id", object["connection_id"]);
      }
      else {
        let summary = createElement("summary", null, ["tree-dataset-summary"], null, null);
        summary.appendChild(createElement("i", null, ["fa-solid", "fa-dataset"], null, null));
        summary.insertAdjacentText("beforeend", " " + object["name"]);
        element.appendChild(summary);
        element.setAttribute("onclick", "getData(" + object["connection_id"] + ", '" + object["name"] + "', '" + id + "')");
        
        if (object.hasOwnProperty("content")) {
          let child = parseObject(object["content"], layer + 1, null);
          if (child) {
            element.appendChild(child);
          }
        }
      }
    }
    
    return element;

  }

  function createConnectionElement(object, layer) {
    let detail = createElement("details", null, ["tree-connection"], layer, null);
    detail.setAttribute("id", "id_connection_" + object["id"]);
    detail.setAttribute("onclick", "getData(" + object["id"] + ", null, 'id_connection_" + object["id"] + "')");

    if (object.hasOwnProperty("name")) {
      let summary = createElement("summary", null, ["tree-connection-summary"], null, null);
      summary.appendChild(createElement("i", null, ["fa-solid", "fa-server"], null, null));
      summary.insertAdjacentText("beforeend", " " + object["name"]);
      detail.appendChild(summary);
    }
    
    if (object.hasOwnProperty("content")) {
      let child = parseObject(object["content"], layer + 1, object["id"]);
      if (child) {
        detail.appendChild(child);
      }
    }

    return detail;

  }

  function createConnectionTypeElement(object, layer) {
    let detail = createElement("details", null, null, layer, null);
    if (object.hasOwnProperty("name")) {
      detail.appendChild(createElement("summary", object["name"], ["tree-connection-type"], null, null));
    }

    if (object.hasOwnProperty("content")) {
      let child = parseObject(object["content"], layer + 1, null);
      if (child) {
        detail.appendChild(child);
      }
    }
    
    return detail;

  }

  function parseObject(arr, layer) {
    if (arr.length == 0) {
      return createElement("div", null, ["modal-container"], null, null);
    }
    let element;
    if (arr[0]["type"] == "column") {
      element = createElement("tbody", null, null, null, null);
    }
    else if (arr[0]["type"] == "table") {
      element = createElement("div", null, ["modal-container", "bg-light"], null, null);
    }
    else {
      element = createElement("div", null, ["modal-container"], null, null);
    }
    for (var i = 0; i < arr.length; i++) {
      if (arr[i].hasOwnProperty("type")) {
        let html;
        if (arr[i]["type"] == "connection-type") {
          html = createConnectionTypeElement(arr[i], layer);
          if (i == 0) {
            html.setAttribute("open", "true");
          }
        }
        else if (arr[i]["type"] == "connection") {
          html = createConnectionElement(arr[i], layer);
        }
        else if (arr[i]["type"] == "dataset") {
          html = createDatasetElement(arr[i], layer);
        }
        else if (arr[i]["type"] == "table" && ["column","table"].includes(returnType["selector"])) {
          html = createTableElement(arr[i], layer);
        }
        else if (arr[i]["type"] == "column" && returnType["selector"] == "column") {
          html = createColumnElement(arr[i], layer);
        }

        if (typeof html != "undefined") {
          element.appendChild(html)
        }
      }
    }
    return element;
  }

  function callConnectionApi(url, modal_id) {
    const xhttp = new XMLHttpRequest();
    let parent = document.getElementById(modal_id);
    if (parent.childElementCount > 0) {
      parent.children[0].appendChild(createSpinner(modal_id + "_spinner"));
    }
    else {
      parent.appendChild(createSpinner(modal_id + "_spinner"));
    }
    xhttp.onload = function () {
      let parent = document.getElementById(modal_id);
      if (parent && parent.nodeType) {
        for (var i = 0; i < parent.childNodes.length; i++) {
            if (parent.childNodes[i].tagName != 'SUMMARY') {
                parent.removeChild(parent.childNodes[i]);
            }
        }

        let data = JSON.parse(this.responseText);
        if (data.hasOwnProperty("result")) {
          let html = parseObject(data["result"], 1, null);
          if (html && html.nodeType) {
            parent.appendChild(html);
          }
        }
        let spinner = document.getElementById(modal_id + "_spinner");
        spinner.parentNode.removeChild(spinner);

      }
    }
    xhttp.open("GET", url, true);
    xhttp.send();
  }

  function getData (id, name, element_id) {
    let url = "/api/schema/";
    if (name) {
      url = url + id + "/" + name + "/";
    }
    else {
      url = url + id + "/";
    }
    modal_id = element_id;

    callConnectionApi(url, element_id);  

    document.getElementById(element_id).removeAttribute("onclick");

  }

  function selectElement(element) {
    let selector = returnType["selector"];
    let message;
    if (selector == "column") {
      message = "Would you like to select column '" + element.dataset["columnFull"] + "'?"
    }
    else if (selector == "table") {
      message = "Would you like to select table '" + element.dataset["tableFull"] + "'?"
    }
    else {
      message = "Would you like to select dataset '" + element.dataset["datasetName"] + "'?"
    }

    document.getElementById("id_selection").textContent = message;

    let submitButton = document.getElementById("id_submit_button");
    submitButton.setAttribute("onclick", "submitSelection('" + element.id + "');");
    submitButton.classList.remove("visually-hidden");
    
  }

  function submitSelection(id) {
    let selector = returnType["selector"];
    let element = document.getElementById(id);
    if (selector == "column" && returnType["column"]["target"]) {
      document.getElementById(returnType["column"]["target"]).value = element.dataset[returnType["column"]["type"]];
      document.getElementById(returnType["column"]["target"]).dispatchEvent(new Event('input'));
    }
    if ((selector == "column" || selector == "table") && returnType["table"]["target"]) {
      document.getElementById(returnType["table"]["target"]).value = element.dataset[returnType["table"]["type"]];
      document.getElementById(returnType["table"]["target"]).dispatchEvent(new Event('input'));
    }
    if (returnType["dataset"]["target"]) {
      document.getElementById(returnType["dataset"]["target"]).value = element.dataset[returnType["dataset"]["type"]];
      document.getElementById(returnType["dataset"]["target"]).dispatchEvent(new Event('input'));
    }
    if (returnType["connection"]["target"]) {
      document.getElementById(returnType["connection"]["target"]).value = element.dataset[returnType["connection"]["type"]];
      document.getElementById(returnType["connection"]["target"]).dispatchEvent(new Event('input'));
    }
    bootstrap.Modal.getInstance(document.getElementById('connection-modal')).hide();
  }

  function setReturnType(selector, columnTarget, columnType, tableTarget, tableType, datasetTarget, connectionTarget, reLoadModal) {
    let datasetType = null;
    let connectionType = null;
    if (datasetTarget) {
      datasetType = "datasetName";
    }
    if (connectionTarget) {
      connectionType = "connectionId"
    }
    returnType = {
      "selector": selector,
      "column": {
        "target": columnTarget,
        "type": columnType,
      },
      "table": {
        "target": tableTarget,
        "type": tableType,
      },
      "dataset": {
        "target": datasetTarget,
        "type": datasetType,
      },
      "connection": {
        "target": connectionTarget,
        "type": connectionType,
      }
    };

    if (reLoadModal) {
      let modal_id = "id_modal_content";
      document.getElementById(modal_id).textContent = "";
      callConnectionApi("/api/schema/", modal_id);
    }
    bootstrap.Modal.getOrCreateInstance(document.getElementById('connection-modal')).show();
  }

  let returnType = {
    "selector": "column",
    "column": {
      "target": "id_source_column",
      "type": "columnName",
    },
    "table": {
      "target": "id_source_name",
      "type": "tableFull",
    },
    "dataset": {
      "target": null,
      "type": null,
    },
    "connection": {
      "target": null,
      "type": null,
    }
  };

  callConnectionApi("/api/schema/", "id_modal_content");

  const myModalEl = document.getElementById('connection-modal');
  myModalEl.addEventListener('hidden.bs.modal', function (event) {
    document.getElementById("id_selection").textContent = "";
    document.getElementById("id_submit_button").removeAttribute("onclick");
    document.getElementById("id_submit_button").classList.add("visually-hidden");
    details = document.getElementsByTagName("details");
    for (var i = 0; i < details.length; i ++) {
      details[i].removeAttribute("open");
    }
  })
