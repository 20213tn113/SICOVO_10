document.addEventListener("DOMContentLoaded", () => {
    cargarAutores();
});

function cargarAutores() {
    // Llamada al backend para obtener los autores
    fetch("/get_autores")
        .then(response => {
            if (!response.ok) {
                throw new Error("Error al obtener los autores");
            }
            return response.json();
        })
        .then(data => {
            const autorSelect = document.getElementById("autor_existente");
            const autorIdSeleccionado = document.getElementById("autor_id").value;

            // Limpia cualquier dato previo en el dropdown
            autorSelect.innerHTML = '<option value="">Seleccione un autor...</option>';

            // Itera sobre los autores y los agrega como opciones
            data.forEach(autor => {
                const option = document.createElement("option");
                option.value = autor[0]; // ID del autor
                option.textContent = autor[1]; // Nombre concatenado del autor

                // Compara el ID del autor con el valor del campo hidden

                if (autor[0] == autorIdSeleccionado) {
                    option.selected = true; // Marca la opción si coincide el ID
                }

                autorSelect.appendChild(option);
            });
        })
        .catch(error => {
            console.error("Error cargando autores:", error);
        });
}


(function () {

    const radioExistente = document.getElementById("radio_existente");
    const radioNuevo = document.getElementById("radio_nuevo");
    const autorExistente = document.getElementById("autor_existente");
    const nombreAutor = document.getElementById("nombre_autor");
    const apellidoAutor = document.getElementById("apellido_autor");
    const fecha_nacimiento = document.getElementById("fecha_nacimiento");

    // Controla los campos según el botón radio seleccionado
    radioExistente.addEventListener("change", () => {
        if (radioExistente.checked) {
            autorExistente.disabled = false;
            nombreAutor.disabled = true;
            apellidoAutor.disabled = true;
            fecha_nacimiento.disabled = true;
            nombreAutor.value = "";
            apellidoAutor.value = "";
            fecha_nacimiento.value = "";
            cargarAutores();
        }
    });

    radioNuevo.addEventListener("change", () => {
        if (radioNuevo.checked) {
            autorExistente.disabled = true;
            nombreAutor.disabled = false;
            apellidoAutor.disabled = false;
            fecha_nacimiento.disabled = false;
            autorExistente.value = "";
        }
    });

})();









(function () {
    const editbtn = document.querySelectorAll('.editbtn');
    const csrf_token = document.querySelector("[name='csrf-token']").value;


    editbtn.forEach((btn) => {
        btn.addEventListener('click', function () {

            isbn = document.getElementById('isbn').value;
            titulo = document.getElementById('titulo').value;
            fecha_edi = document.getElementById('fecha_edi').value;
            descripcion = document.getElementById('descripcion').value;
            precio = document.getElementById('precio').value;
            isbn_org = document.getElementById('isbn_org').value;

            const inputImagen = document.getElementById('imagen');
            const imagen = inputImagen.files[0];


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

                const formData = new FormData();
                formData.append('isbn', isbn);
                formData.append('isbn_org', isbn_org);
                formData.append('titulo', titulo);
                formData.append('fecha_edi', fecha_edi);
                formData.append('descripcion', descripcion);
                formData.append('precio', precio);
                formData.append('imagen', imagen);
                console.log('isbn ORG: ', isbn_org);
                const radioExistente = document.getElementById('radio_existente').checked;
                const radioNuevo = document.getElementById('radio_nuevo').checked;

                if (radioExistente) {
                    const autorExistente = document.getElementById('autor_existente').value;
                    console.log('autor id: ', autorExistente)
                    if (!autorExistente) {
                        Swal.fire({
                            title: "Error",
                            text: "Debe seleccionar un autor existente.",
                            icon: "warning",
                        });
                        return false;
                    }
                    formData.append('autor', autorExistente); // ID del autor existente
                    formData.append('autor_nuevo', false); // Indica que es un autor nuevo

                } else if (radioNuevo) {
                    const nombreAutor = document.getElementById('nombre_autor').value.trim();
                    const apellidoAutor = document.getElementById('apellido_autor').value.trim();
                    const fechaNacimiento = document.getElementById('fecha_nacimiento').value;

                    if (!nombreAutor || !apellidoAutor || !fechaNacimiento) {
                        Swal.fire({
                            title: "Error",
                            text: "Debe completar los datos del nuevo autor.",
                            icon: "warning",
                        });
                        return false;
                    }

                    // Si es un autor nuevo, agrega sus datos al FormData
                    formData.append('autor_nuevo', true); // Indica que es un autor nuevo
                    formData.append('nombre_autor', nombreAutor);
                    formData.append('apellido_autor', apellidoAutor);
                    formData.append('fecha_nacimiento', fechaNacimiento);
                } else {
                    Swal.fire({
                        title: "Error",
                        text: "Debe seleccionar un tipo de autor (existente o nuevo).",
                        icon: "warning",
                    });
                    return false;
                }


                return await fetch(`${window.origin}/editar`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRF-TOKEN': csrf_token
                    },
                    body: formData,
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
                            title: "Libro registrado exitosamente",
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
