document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.alert').forEach(alertBlock => {
        setTimeout(() => {
            alertBlock.style.display = 'none';
        }, 3000);


        const closeButton = alertBlock.querySelectorAll('.alert-close');
        if (closeButton) {
            closeButton.addEventListener('click', function () {
                const targetId = this.getAttribute('data-target');
                const alertToClose = document.getElementById(targetId);
                if (alertToClose) {
                    alertToClose.style.display = 'none';
                }
            })
        }
    });
});
