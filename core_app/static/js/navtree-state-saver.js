$(document).on('submit', 'form', function(e){
    var new_data = $(this).serializeArray();
    var active_ids = $('.active').map(function(_, x) { return x.id; }).get();
    new_data.push({name: 'active_ids', value: active_ids});

    if ( typeof connections != "undefined" ) {
        new_data.push({name: 'connections', value: Array.from(connections)})
    };

    $.ajax({
        type: 'POST',
        data: new_data,
        async: false
    });
});
$(document).on('beforeunload', function(e){
    e.preventDefault();
    var new_data = [];
    new_data.push({name: 'before-redirect', value: ['']});
    var active_ids = $('.active').map(function(_, x) { return x.id; }).get();
    new_data.push({name: 'active_ids', value: active_ids});
    $.ajax({
        type: 'POST',
        data: new_data,
        async: false
    });
});