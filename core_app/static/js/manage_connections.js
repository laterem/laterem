var connection_elements = jQuery.makeArray($(".connection"));
var connections = new Set();
let new_connection = [null, null];
var i;

for (i = 0; i < connection_elements.length; i++) {
    connection_elements[i].addEventListener("click", function() {
        if (new_connection[0] === null) {
            new_connection[0] = this.id;
        } else {
            new_connection[1] = this.id;
            connections.add(new_connection)
            console.log(...connections)
            new_connection = [null, null];
        };
    });
};
