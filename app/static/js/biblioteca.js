(function () {
    const btnEliminar = document.querySelectorAll('.btnEliminar');
    const csrf_token = document.querySelector("[name='csrf-token']").value;


    btnEliminar.forEach((btn) => {
        btn.addEventListener('click', function () {

            const isbn = btn.getAttribute('data-isbn');
            console.log(isbn)


            confirmarEliminar(isbn);
        })
    });

    const confirmarEliminar = (isbn) => {

        Swal.fire({
           title: "¿Estás seguro?",
            text: "Esta acción no se puede deshacer",
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Borrar",
            cancelButtonText: "Cancelar",
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                console.log(window.origin);

                return await fetch(`${window.origin}/borrarlibro`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': csrf_token
                    },
                    body: JSON.stringify({
                        'isbn' : isbn
                    })
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
                            title: "Libro eliminado exitosamente",
                            showConfirmButton: '¡Ok!',
                            timer: 1500
                        }).then((result) => {
                            if (result.dismiss === Swal.DismissReason.timer) {
                                window.location.href = '/biblioteca';
                            } else if (result.isConfirmed) {
                                window.location.href = '/biblioteca';
                            }
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

(function () {
    const btnEditar = document.querySelectorAll('.btnEditar');

    btnEditar.forEach((btn) => {
        btn.addEventListener('click', function () {
            const isbn = btn.getAttribute('data-isbn'); // Obtener el ISBN del atributo data-isbn
            window.location.href = `/editarlibro/${isbn}`; // Redirigir a la ruta con el ISBN
        });
    });
})();

