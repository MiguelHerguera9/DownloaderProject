function addField() {
    const container = document.getElementById('urlContainer');
    const inputGroup = document.createElement('div');
    inputGroup.className = 'input-group mb-3 w-75';

    inputGroup.innerHTML = `
        <input type="text" class="form-control" name="urls" placeholder="Ingresa una URL de YouTube" oninput="validateYouTubeURL(this)">
        <button type="button" class="btn btn-outline-danger" onclick="removeField(this)">Eliminar</button>
    `;
    container.appendChild(inputGroup);
}

function removeField(button) {
    button.parentElement.remove();
}

function validateYouTubeURL(input) {
    const youtubeRegex = /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]{11}(&.*)?$/;

    if (youtubeRegex.test(input.value.trim())) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    } else {
        input.classList.remove('is-valid');
        input.classList.add('is-invalid');
    }
}

async function sendData() {
    const resultDownloadAlert = document.getElementById('result-download');
    if(resultDownloadAlert) resultDownloadAlert.remove();

    const inputs = document.querySelectorAll('[name="urls"]');
    const urls = Array.from(inputs).map(input => input.value.trim()).filter(url => url);

    if (urls.length === 0) {
        alert("Por favor, ingresa al menos una URL.");
        return;
    }

    const invalidInputs = Array.from(inputs).filter(input => !/^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[\w-]{11}(&.*)?$/.test(input.value.trim()));
    if (invalidInputs.length > 0) {
        alert("Una o más URLs no son válidas. Corrige los errores antes de continuar.");
        return;
    }

    try {
        const loadingToast = `
            <div id="alert-downloading" class="alert alert-warning" role="alert">
                <div>
                    <h2>Descargando músicas...</h2>
                </div>
                <div class="spinner-border text-warning" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `

        const form = document.getElementById('urlForm');
        form.insertAdjacentHTML('beforebegin', loadingToast);



        const response = await fetch('/process-urls/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ urls }),
        });
        document.getElementById('alert-downloading').remove();
        responseJson = await response.json();

        if (response.ok) {
            const successDownloadAlert = `
                <div id="result-download" class="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>Descarga exitosa</strong> ${responseJson.message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `
            form.insertAdjacentHTML('beforebegin', successDownloadAlert);
        } else {
            const errorDownloadAlert = `
                <div id="result-download" class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>Error</strong> ${responseJson.message}.
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>
            `
            form.insertAdjacentHTML('beforebegin', errorDownloadAlert);
        }
    } catch (error) {
        console.error('Error al enviar las URLs:', error);
        alert('Ocurrió un error inesperado.');
    }
}