
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
            imagen = document.getElementById('imagen').files[0];

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





                return await fetch(`${window.origin}/agregar`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': csrf_token
                    },
                    body: JSON.stringify({
                        'isbn' : isbn,
                        'titulo' : titulo,
                        'autor' : autor,
                        'fecha_edi' : fecha_edi,
                        'descripcion' : descripcion,
                        'precio' : precio,
                        'imagen' : imagen
                    }), formData
                }).then(response => {
                    if (!response.ok) {
                        notificacionSwal('Error', response.statusText, 'error', 'Cerrar');
                    }
                    return response.json();

                }).then(data => {
                    if (data.exito) {
                        Swal.fire({
                            position: "Center",
                            titleText: '¡Éxito!',
                            icon: "success",
                            title: "Usuario registrado exitosamente",
                            showConfirmButton: '¡Ok!',
                            timer: 1500

                        }).then((result) => {
                            if (result.dismiss === Swal.DismissReason.timer) {
                                window.location.href = '/login';
                            } else if (result.isConfirmed) {
                                window.location.href = '/login';
                            }
                        });

                    } else {
                        notificacionSwal('¡Alerta!', data.mensaje, 'warning', 'Ok');
                    }
                }).catch(error => {
                    notificacionSwal('Error', error, 'error', 'Cerrar');
                });
            },
            allowOutsideClick: () => false,
            allowEscapeKey: () => false
        });
    };
})();