function createChoiceBox(){
    var ChoiceBox = document.createElement("div");
    var ChoiceTitle = document.createElement("span");
    var ChoiceInput = document.createElement("input");
    ChoiceBox.className =  "input-group";
    ChoiceTitle.className = "input-group-addon";
    ChoiceInput.className = "form-control";
    ChoiceInput.type = "text";
    ChoiceInput.placeholder = "请输入问题内容";
    ChoiceBox.appendChild(ChoiceTitle);
    ChoiceBox.appendChild(ChoiceInput);

    return ChoiceBox
}

function addChoiceBox(){

}