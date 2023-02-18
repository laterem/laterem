var is_blackout = false;

function disp_dialog(target) {
    if ( target.style != undefined ) {
        if ( is_blackout ) {
            if (target != undefined) {
                target.style.display = 'none';
            };
            $("#blackout")[0].style.display = 'none';
        } else {
            if (target != undefined) {
                target.style.display = 'block';
            };
            $("#blackout")[0].style.display = 'block';
        };
    } else {
        if ( is_blackout ) {
            for ( let i = 0; i < target.length; i++ ) {
                target[i].style.display = 'none';
            };
            $("#blackout")[0].style.display = 'none';
        } else {
            for ( let i = 0; i < target.length; i++ ) {
                target[i].style.display = 'block';
            };
            $("#blackout")[0].style.display = 'block';
        };
    };
    is_blackout = !is_blackout;
}
