class MisDatos{
    constructor(unIdViaje, unPrecio){
        this.unosInsumos=new Array();
        this.cantInsumos=new Array();
        this.idViaje=unIdViaje;
        this.precioDeViaje=parseFloat(unPrecio.replace(",","."))
        this.total=0;
        this.totalDeCompra=0;
        this.precios=new Map();
        this.conTarjeta=new Map();
    }
    agregar(){
        var unId=document.getElementById('id_insumos').value;
        var unaCant=document.getElementById('id_cantInsumo').value;
        if (unId.length==0 || unaCant.length===0){    
            alert("debe selecionar un insumo o ingresar la cantidad");
        }else{
            this.unosInsumos.unshift(unId);
            this.cantInsumos.unshift(unaCant);
            this.sumarTotal(unId,unaCant);
            this.cambiarTotal();
        }
    }
    agregarPrecios(unId, unPrecio){
        this.precios.set(unId, unPrecio);
    }
    cambiarTotal(){
        document.getElementById("texto_total").innerHTML = "Compra total de los Insumos: "+this.total+"$";
    }
    sumarTotal(unId, unaCant){
        let valor= this.precios.get(unId);
        let auxCant= parseFloat(unaCant);
        let suma= parseFloat(valor.replace(",", "."))*auxCant;
        this.total=this.total+suma;  
    }
    agregarTarjeta(numero, fecha_day, fecha_month, fecha_year , codigo){
        this.conTarjeta.set("numero", numero);
        this.conTarjeta.set("fecha_day", fecha_day);
        this.conTarjeta.set("fecha_month", fecha_month);
        this.conTarjeta.set("fecha_year", fecha_year)
        this.conTarjeta.set("codigo", codigo);
    }
    formulario() {
        $.ajax(
            {
                data: {'dato': otroCant, 'datos': unInsumo},
                url: $('#form_creacion').attr('action'),
                type:'GET',
                success : function(respuesta) {
                    console.log(respuesta);
                },
                error: function(error){
                    console.log(error);
                }
            }
        );
    }

    ponerTarjetaAlForm(){
        document.getElementById("id_numero").value = this.conTarjeta.get("numero");
        document.getElementById("id_codigo").value = this.conTarjeta.get("codigo");
        document.getElementById("id_fecha_de_vencimiento_day").value = this.conTarjeta.get("fecha_day");
        document.getElementById("id_fecha_de_vencimiento_month").value = this.conTarjeta.get("fecha_month");
        document.getElementById("id_fecha_de_vencimiento_year").value =this.conTarjeta.get("fecha_year");
    }
    confirmar(){
        document.getElementById("confirmacion2").innerHTML = "<h3>monto totol de la compra es: "+this.totalDeCompra+"</h3>";
        document.getElementById("confirmacion").innerHTML = "<button type='button' onclick=datos.prueba()>Confirmar compra </button>";
    }
    prueba(){
        document.getElementById("alerta").innerHTML = "se pudo hacer";
    }
}

