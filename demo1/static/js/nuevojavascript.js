class MisDatos{
    constructor(unIdViaje, unPrecio, cantAsientos, esGold){
        this.unosInsumos=new Array();
        this.cantInsumos=new Array();
        this.idViaje=unIdViaje;
        this.precioDeViaje=parseFloat(unPrecio.replace(",","."))
        this.total=0;
        this.totalDeCompra=0;
        this.precios=new Map();
        this.nombre=new Map();
        this.conTarjeta=new Map();
        this.cantAsientosDis=parseInt(cantAsientos);
        this.esGold=esGold;
    }
    agregar(){
        
        var unId=document.getElementById('id_insumos').value;
        var unaCant=document.getElementById('id_cantInsumo').value;
        if (unId.length==0 || unaCant.length===0){    
            alert("debe selecionar un insumo o ingresar la cantidad");
        }else{
            let tiene= this.verficarExistenciaDeInsumo(unId, unaCant);
            if (tiene){
                this.unosInsumos.unshift(unId);
                this.cantInsumos.unshift(unaCant);
            }
            var element = document.getElementsByTagName("table"), index;
            for (index = element.length - 1; index >= 0; index--) {
                element[index].parentNode.removeChild(element[index]);  
                }
            
            this.generar_tabla();
            document.getElementById("Detalle").innerHTML = "<h4>El precio de cada pasaje es: $"+this.precioDeViaje+"</h4>";
            this.sumarTotal(unId,unaCant);
            this.cambiarTotal();
        }
    }
    generar_fila(lista_texto){
        var fila=document.createElement("tr");
        for (let i = 0; i < lista_texto.length; i++) {
            const element = document.createElement("td");
            var textoCelda = document.createTextNode(lista_texto[i]);
            element.appendChild(textoCelda);
            fila.appendChild(element);  
        }
        document.getElementById("cuerpo_tabla").appendChild(fila);
    }
    generar_tabla(){
        document.getElementById("Tabla").innerHTML= "<table border='1' style='width:90%;'><tbody id='cuerpo_tabla'></tbody></table>";
        var nombre_cabecera=["Producto", "Cantidad", "Costo unitario" ];
        var fila=document.createElement("tr");
        var colum=document.createElement("td");
        colum.colSpan='3';
        colum.align="center";
        colum.appendChild(document.createTextNode("Carrito de Productos"));
        fila.appendChild(colum);
        document.getElementById("cuerpo_tabla").appendChild(fila);
        this.generar_fila(nombre_cabecera);
        for (var i = 0; i < this.unosInsumos.length; i++) {
            var lista_texto = [this.nombre.get(this.unosInsumos[i]), this.cantInsumos[i],this.precios.get(this.unosInsumos[i])];
            this.generar_fila(lista_texto);
        }   
    }
    
     
    verficarExistenciaDeInsumo(unId, unaCant){
        let tiene=true;
        for (let index = 0; index < this.unosInsumos.length; index++) {
            let id = this.unosInsumos[index];
            if (id==unId){
                this.cantInsumos[index]=parseInt(this.cantInsumos[index])+parseInt(unaCant);
                tiene=false;
            }
        }
        return tiene;
    }
    agregarPrecios(unId, unPrecio,unNombre){
        this.precios.set(unId, unPrecio);
        this.nombre.set(unId, unNombre);
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
        
        function resumenDecompra(respuesta) {
            
            let o=respuesta[0]["origen"];
            let d=respuesta[0]["destino"];
            let n=respuesta[0]["nombre"];
            let t=respuesta[0]["total"];
            let cant= respuesta[0]["cant"];
            let f=respuesta[0]["fecha"];
            let h=respuesta[0]["hora"];
            document.getElementById("esGold").innerHTML="";
            document.getElementById("mi_total").innerHTML="";
            document.getElementById("form").innerHTML="";
            document.getElementById("form").style="";
            document.getElementById("Tabla").style="";
            document.getElementById("Tabla").innerHTML="";
            document.getElementById("confirmacion2").innerHTML="<h3>La compra se realizo con exito. Resumen de compra:</h3>";
            document.getElementById("confirmacion").innerHTML="<p>Pasajero: "+n+"</p><p>Costo: $"+t+"</p><p>Origen: "+o+"</p><p>Destino: "+d+"</p><p>Fecha: "+f+"</p><p>Hora: "+h+"</p><p>Cantidad de asientos: "+cant+"</p><p></p>";
            document.getElementById("botones").innerHTML="";
            
        }
        let cantAsientos= document.getElementById("id_cantidad").value;
        $.ajax(
            {
                data: {'dato': this.unosInsumos, 
                        'datos': this.cantInsumos,
                        "total": this.totalDeCompra,
                        "cant": cantAsientos},
                url: $('#form_creacion').attr('action'),
                type:'GET',
                dataType: "json",
                success : function(respuesta) {
                    console.log(respuesta);
                    resumenDecompra(respuesta);
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
        let cantidad=document.getElementById("id_cantidad").value;
        let valido=this.verificarCantidad(cantidad);
        let validarTarjeta=this.validarTarjeta();
        if (valido && validarTarjeta){
            setTimeout(() => {
                this.cambiarHtml(cantidad)
            }, 5000);
            document.getElementById("confirmacion2").innerHTML= "<h4>Validando tarjeta....</h4>";
        }
    }

    cambiarHtml(cantidad){
        let descuento=this.calcularTotalDeCompra(parseInt(cantidad));
        document.getElementById("confirmacion2").innerHTML = "<h4>Tarjeta Valida.</h4><h3>Monto totol de la compra es: "+this.totalDeCompra+"$</h3>";
        if(this.esGold=="True"){
            this.totalDeCompra=this.totalDeCompra-descuento;
            document.getElementById("esGold").innerHTML = "<h3>Por ser usuario gold obtubo un descuento del 15%. Precio total es: " +this.totalDeCompra+"$</h3";
        }
        document.getElementById("confirmacion").innerHTML = "<p>Esta seguro de realizar la compra?</p><button type='button' onclick=datos.formulario()>Confirmar </button><button type='button' onclick=datos.cancelado()>Cancelar</button>";
    }

    verificarCantidad(cant){
        if (parseInt(cant)<=this.cantAsientosDis && parseInt(cant)>0){
            return true;
        }else{
            alert("La cantidad de pasajes ingresados debe ser menor a las disponibles (Disp: "+this.cantAsientosDis+") y mayor a 0. Vuelva a ingresar la cantidad");
            return false;
        }
    }
    cancelado(){
        document.getElementById("confirmacion2").innerHTML ="";
        document.getElementById("esGold").innerHTML ="";
        document.getElementById("confirmacion").innerHTML ="";
        document.getElementById("Tabla").innerHTML="";
        this.unosInsumos=new Array();
        this.cantInsumos=new Array();
        this.totalDeCompra=0;
        this.total=0;
        this.cambiarTotal();
    }
    
    calcularTotalDeCompra(cant){
        let dato=this.precioDeViaje*cant;
        this.totalDeCompra=this.total+dato;
        let descuento=0;
        if (this.esGold=="True"){
            descuento=(this.totalDeCompra*15)/100;
        }
        return descuento;
    }
    validarTarjeta(){
        let today= new Date();
        let dias=today.getDate();
        let mes=today.getMonth(); //este cuenta de 0 a 11
        let year=today.getFullYear();
        let numero=document.getElementById("id_numero").value;
        let codigo= document.getElementById("id_codigo").value;
        let diasHtml=document.getElementById("id_fecha_de_vencimiento_day").value;
        let mesHtml=document.getElementById("id_fecha_de_vencimiento_month").value;
        let a??oHtml=document.getElementById("id_fecha_de_vencimiento_year").value;
        if (numero.length==0 || codigo.length==0){
            alert("Debe ingresar los datos de la tarjeta");
            return false;
        }else{
            if (numero.length==18 && codigo.length==3){
                let fecha= new Date(a??oHtml, parseInt(mesHtml)-1, diasHtml);
                if (fecha<today){
                    if (dias==parseInt(diasHtml) && mes==parseInt(mesHtml)-1 && year==parseInt(a??oHtml)){
                        return true;
                    }else{
                        alert("La fecha ingresada no debe ser pasada");
                        return false;
                    }
                }else{
                    return true;
                }
            }else{
                alert("Ingrese dos datos correctamente. El codigo es de 3 dig. y el numero de tarjeta de 18 digitos");
                return false;
            }
        }
    }
}

function confirmarEliminacion(unUrl, mensaje) {
    let valor=confirm(mensaje);
    if (valor){
        $.ajax({
            url: unUrl,
            type:'GET',
            dataType: "json",
            success : function(respuesta) {
                console.log(respuesta);
                if (respuesta[0]["seElimino"]){
                    document.getElementById("mensaje").innerHTML= "<h3>"+respuesta[0]["mensaje"]+"</h3>";
                    setTimeout(() => {
                        document.getElementById("mensaje").innerHTML="";
                    }, 5000);
                }else{
                    location.reload();
                }
                },
            error: function(error){
                console.log(error);
            }
        });
    }
}

function confirmEliminacion(unUrl,mensaje){
    let valor=confirm(mensaje)
    if(valor){
        $.ajax({
            url:unUrl,
            type:'GET',
            success: function(respuesta){
                console.log(respuesta);
                location.reload();
            },
            error: function(error){
                console.log(error);
            }
        })
    }
}
function confirmEliminacion1(unUrl,mensaje){
    let valor=confirm(mensaje)
    if(valor){
        $.ajax({
            url:unUrl,
            type:'GET',
            success: function(respuesta){
                console.log(respuesta);
                //location.reload();
            },
            error: function(error){
                console.log(error);
            }
        })
    }
}
