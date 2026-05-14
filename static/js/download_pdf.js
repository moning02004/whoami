document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('submit', function (e) {
        const target = e.target.closest('.download-pdf');
        if (target) {
            e.preventDefault();

            const button = target.querySelector('button');
            const icon = target.querySelector('i');
            const originalIcon = icon.className;

            button.disabled = true;
            button.classList.add('opacity-50', 'cursor-not-allowed');
            icon.className = 'fa-solid fa-spinner fa-spin';

            fetch(target.action, {method: 'POST', body: new FormData(target)})
                .then(res => {
                    const disposition = res.headers.get('Content-Disposition');
                    const encoded = disposition?.match(/filename\*=UTF-8''(.+)/)?.[1] || 'output.pdf';
                    const filename = decodeURIComponent(encoded);
                    return res.blob().then(blob => ({blob, filename}));
                })
                .then(({blob, filename}) => {
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = filename; // 👈 뷰에서 지정한 파일명 사용
                    a.click();
                    URL.revokeObjectURL(url);
                })
                .finally(() => {
                    button.disabled = false;
                    button.classList.remove('opacity-50', 'cursor-not-allowed');
                    icon.className = originalIcon;
                });
        }
    })
})