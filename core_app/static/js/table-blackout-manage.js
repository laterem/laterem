tables = $('.dialog-table');

for ( let i = 0; i < tables.length; i++ ) {
    tables[i].addEventListener('click', function (e) {
        if (e.target.localName == 'table') {
            disp_dialog($('#' + this.id));
        };
    });
};
