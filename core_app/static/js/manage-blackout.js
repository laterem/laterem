var is_blackout = false;

function disp_dialog(target) {
    if ( target.style != undefined ) {
        if ( is_blackout ) {
            target.style.display = 'none';
            $("#blackout")[0].style.display = 'none';
        } else {
            target.style.display = 'block';
            $("#blackout")[0].style.display = 'block';
        };
    } else {
        if ( is_blackout ) {
            for ( let i = 0; i < target.length; i++ ) {
                if ( target[i].style != undefined ) {
                    target[i].style.display = 'none';
                } else {
                    for ( let j = 0; j < target[i].length; j++ ) {
                        target[i][j].style.display = 'none';
                    };
                };
            };
            $("#blackout")[0].style.display = 'none';
        } else {
            for ( let i = 0; i < target.length; i++ ) {
                if ( target[i].style != undefined ) {
                    target[i].style.display = 'block';
                } else {
                    for ( let j = 0; j < target[i].length; j++ ) {
                        target[i][j].style.display = 'block';
                    };
                };
            };
            $("#blackout")[0].style.display = 'block';
        };
    };
    is_blackout = !is_blackout;
};
