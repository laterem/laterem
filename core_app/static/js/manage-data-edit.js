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
    editing_class = target.className.split(' ')[0];
    editing_inputs = $('input.' + editing_class);

    if ( is_editing ) {
        for ( let i = 0; i < editing_inputs.length; i++ ) {
            editing_inputs[i].value = saved_inputs[i].value;
            editing_inputs[i].disabled = true;
        };
    } else {
        saved_inputs = editing_inputs.clone();
        for ( let i = 0; i < editing_inputs.length; i++ ) {
            editing_inputs[i].disabled = false;
        };
    };
    is_editing = !is_editing;
};
