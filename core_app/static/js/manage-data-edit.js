is_editing = false;
var saved_inputs = $('input');

Object.prototype.clone = Array.prototype.clone = function()
{
    if (Object.prototype.toString.call(this) === '[object Array]')
    {
        var clone = [];
        for (var i=0; i<this.length; i++)
            clone[i] = this[i].clone();

        return clone;
    } 
    else if (typeof(this)=="object")
    {
        var clone = {};
        for (var prop in this)
            if (this.hasOwnProperty(prop))
                clone[prop] = this[prop].clone();

        return clone;
    }
    else
        return this;
}

function data_edit(target) {
    target_class = target.className.split(' ')[0];
    if (target_class.slice(target_class.lastIndexOf('-') + 1) == "confirm") {
        target.closest('form').method = "post";
    } else {
        editing_class = target_class.slice(0,target_class.lastIndexOf('-'));
        editing_inputs = $('input.' + editing_class);
        editing_areas = $('textarea.' + editing_class);
        confirm_button = $('button.' + editing_class + '-confirm')[0];
        undo_button = $('button.' + editing_class + '-undo')[0];
        edit_button = $('button.' + editing_class + '-edit')[0];

        if ( is_editing ) {
            for ( let i = 0; i < editing_inputs.length; i++ ) {
                editing_inputs[i].value = saved_inputs[i].value;
                editing_inputs[i].disabled = true;
            };
            for ( let i = 0; i < editing_areas.length; i++ ) {
                editing_areas[i].value = saved_areas[i].value;
                editing_areas[i].disabled = true;
            };
            confirm_button.style.display = "none";
            undo_button.style.display = "none";
            edit_button.style.display = "inline-flex";
        } else {
            saved_inputs = editing_inputs.clone();
            saved_areas = editing_areas.clone();
            for ( let i = 0; i < editing_inputs.length; i++ ) {
                editing_inputs[i].disabled = false;
            };
            for ( let i = 0; i < editing_areas.length; i++ ) {
                editing_areas[i].disabled = false;
            };
            confirm_button.style.display = "inline-flex";
            undo_button.style.display = "inline-flex";
            edit_button.style.display = "none";
        };
        is_editing = !is_editing;
    };
    
};
