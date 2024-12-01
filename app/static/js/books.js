
(function () {
    const addbtn = document.querySelectorAll('.addbtn');
    const csrf_token = document.querySelector("[name='csrf-token']").value;


    addbtn.forEach((btn) => {
        btn.addEventListener('click', function () {

            isbn = document.getElementById('isbn').value;
            titulo  = document.getElementById('titulo').value;
            autor  = document.getElementById('autor').value;
            fecha_edi = document.getElementById('fecha_edi').value;
            descripcion = document.getElementById('descripcion').value;
            precio = document.getElementById('precio').value;
            // imagen = document.getElementById('imagen').files[0];
            // console.log(imagen);

                confirmarComprar();
        })
    });

    const confirmarComprar = () => {

        Swal.fire({
            title: '¿Desea continuar con el registro?',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Registrar',
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                console.log(window.origin);
                const inputImagen = document.getElementById('imagen');
                const imagen = inputImagen.files[0];
                console.log("Imagen")
                console.log(imagen)
                const formData = new FormData();
                formData.append('isbn', isbn);
                formData.append('titulo', titulo);
                formData.append('autor', autor);
                formData.append('fecha_edi', fecha_edi);
                formData.append('descripcion', descripcion);
                formData.append('precio', precio);
                formData.append('imagen', imagen);
                console.log("FormData")
                console.log(formData[imagen])
                console.log(formData);
                return await fetch(`${window.origin}/agregar`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRF-TOKEN': csrf_token
                    },
                    body:  formData,
                }).then(response => {
                    if (!response.ok) {
                        notificacionSwal('Error', response.statusText, 'error', 'Cerrar');
                    }
                    return response.json();
                }).then(data => {
                    if (data.exito) {
                        Swal.fire({
                            title: "¡Éxito!",
                            text: data.mensaje,
                            icon: "success",
                        });
                    } else {
                        Swal.fire({
                            title: "Error",
                            text: data.mensaje,
                            icon: "warning",
                        });
                    }
                }).catch(error => {
                    Swal.fire({
                        title: "Error",
                        text: error.message,
                        icon: "error",
                    });
                });
            },
            allowOutsideClick: () => false,
            allowEscapeKey: () => false
        });
    };
})();