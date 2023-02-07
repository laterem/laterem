var connection_elements = jQuery.makeArray($(".connection"));
var connections = new Set();
let new_connection = [null, null];
var new_arrow = '';
var i;


function create(htmlStr) {
    var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
    temp.innerHTML = htmlStr;
    while (temp.firstChild) {
        frag.appendChild(temp.firstChild);
    }
    return frag;
}


for (i = 0; i < connection_elements.length; i++) {
    connection_elements[i].addEventListener("click", function() {
        if (new_connection[0] === null) {
            new_connection[0] = this.id;
            console.log(this.id)
        } else {
            if (new_connection[0] != this.id) {
                new_connection[1] = this.id;
                connections.add(new_connection)
                console.log(...connections)

                // Создание стрелки, соединяющей new_connection [0] -> [1]
                // Стрелка:
                // <connection
                // from="#{new_connection[0]}"
                // to="#{new_connection[0]}"
                // color="" Что-то сгенеренное от {i}
                // fromX="1" toX="0" tail onlyVisible></connecton>

                new_arrow = '<connection from="#' + new_connection[0] + '" to="#' + new_connection[1] + '" color="' + 'red' + '" fromX="' + '1' + '" toX="' + '0' + '" tail onlyVisible>' + '</connection>' + $('#task-area')[0].innerHTML;

                $('#task-area')[0].innerHTML = new_arrow;
                new_connection = [null, null];
            };
        };
    });
};
