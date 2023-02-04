var connection_elements = $(".connection");
let connections = Set([]);
var new_connection = [null, null];
var i;

for (i = 0; i < connection_elements.length; i++) {
    connection_elements[i].addEventListener("click", function() {
        if (new_connection[0] == null) {
            new_connection[0] = connection_elements[i].id;
        } else {
            new_connection[1] = connection_elements[i].id;
            connections.add(new_connection)
            var new_connection = [null, null];
        };
    });
};
