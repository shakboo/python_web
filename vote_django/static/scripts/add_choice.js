function addLoadEvent(func){
    var oldonload=window.onload;
    if(typeof window.onload != 'function') {
        window.onload = func;
    }else{
        window.onload=function(){
            oldonload();
            func();
        }
    }
}


function createChoiceBox(){


    var ChoiceBox = document.createElement("div");
    var ChoiceTitle = document.createElement("span");
    var ChoiceInput = document.createElement("input");
    var ChoiceNum = document.getElementsByClassName("input-group");
    ChoiceBox.className =  "input-group";
    ChoiceTitle.className = "input-group-addon";
    ChoiceTitle.innerHTML = "问题";
    ChoiceInput.className = "form-control";
    ChoiceInput.type = "text";
    ChoiceInput.placeholder = "请输入问题内容";
    ChoiceInput.name = String(ChoiceNum.length+1);
    ChoiceBox.appendChild(ChoiceTitle);
    ChoiceBox.appendChild(ChoiceInput);

    ChoiceTitle.onclick = function(){
        ChoiceBox.parentNode.removeChild(ChoiceBox);
    }

    return ChoiceBox;
}


function addChoiceBox(){
    var addChoiceBtn = document.getElementById("addChoice");
    addChoiceBtn.onclick = function(){
        var targetElement = document.getElementById("addTarget");
        var parent = targetElement.parentNode;
        parent.insertBefore(createChoiceBox(),targetElement);
    }
}

addLoadEvent(addChoiceBox)