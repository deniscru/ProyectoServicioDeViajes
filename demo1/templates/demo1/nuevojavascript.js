function formulario() {
    $.ajax(
        {
            data: $('#form_creacion').serialize(),
            url: $('#form_creacion').attr('action'),
            type:$('#form_creacion').attr('method'),
            success : function(respuesta) {
                console.log(respuesta);
            },
            error: function(error){
                console.log(error);
            }
        }
    );
}
