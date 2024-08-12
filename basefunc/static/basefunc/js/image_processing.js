const postForm = document.getElementById('post-form')
const photoPreview = document.getElementById('photo-preview')
const photoUrlPreview = document.getElementById('photo-url-preview')
const confirmBtn = document.getElementById('confirm-btn')
const inputPhoto = document.getElementById('id_photo')
const inputPhotoUrl = document.getElementById('id_photo_url')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

// Добавляем обработчик submit один раз при загрузке страницы
document.getElementById('post-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const $image = $('#image');
    const cropper = $image.data('cropper');

    cropper.getCroppedCanvas().toBlob((blob) => {
        const img = new Image();
        img.src = URL.createObjectURL(blob);

        img.onload = function() {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');

            canvas.width = img.width;
            canvas.height = img.height;

            ctx.drawImage(img, 0, 0);

            const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
            const data = imageData.data;

            for (let i = 0; i < data.length; i += 4) {
                const avg = (data[i] + data[i + 1] + data[i + 2]) / 3;
                data[i] = avg;
                data[i + 1] = avg;
                data[i + 2] = avg;
            }

            ctx.putImageData(imageData, 0, 0);

            canvas.toBlob((filteredBlob) => {
                const formData = new FormData(postForm);
                formData.set('photo', filteredBlob, 'filtered-image.png');

                for (const [key, value] of formData.entries()) {
                    console.log(`${key}: ${value}`);
                }

                fetch(postForm.action, {
                    method: 'POST',
                    body: formData,
                })
                .then(response => response.text())
                .then(html => {
                    console.log('Received HTML:', html);
                    document.open();
                    document.write(html);
                    document.close();
                })
                .catch(error => {
                    console.error('Error:', error);
                });
            });
        };
    });
});

// Добавляем preview и очищаем поля только при изменении input
inputPhoto.addEventListener('change', () => {
    inputPhotoUrl.value = '';
    photoUrlPreview.innerHTML = '';

    const photo_data = inputPhoto.files[0];
    const url = URL.createObjectURL(photo_data);
    photoPreview.innerHTML = `<img src="${url}" id="image" width="300px">`;

    $('#image').cropper({
        aspectRatio: 1 / 1,
        crop(event) {
            console.log(event.detail.x, event.detail.y, event.detail.width, event.detail.height);
        },
    });
});

inputPhotoUrl.addEventListener('change', () => {
    inputPhoto.value = '';
    photoPreview.innerHTML = '';

    const url = inputPhotoUrl.value;
    const proxyUrl = `/proxy-image/?url=${encodeURIComponent(url)}`;

    fetch(proxyUrl)
        .then(response => response.blob())
        .then(blob => {
            const imgURL = URL.createObjectURL(blob);
            photoUrlPreview.innerHTML = `<img src="${imgURL}" id="image" width="300px">`;

            $('#image').cropper({
                aspectRatio: 1 / 1,
                crop(event) {
                    console.log(event.detail.x, event.detail.y, event.detail.width, event.detail.height);
                },
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
