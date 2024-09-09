document.addEventListener('DOMContentLoaded', function () {
   const deleteBtn = document.getElementById('deleteBtn');
   const confirmDeleteBtn = document.getElementById('confirmDelete');
   const deleteForm = document.getElementById('deleteForm');
   
   const modalElement = document.getElementById('exampleModal');
   const modal = new bootstrap.Modal(modalElement);
   
   deleteBtn.addEventListener('click', function (event) {
       event.preventDefault();
       modal.show();
   })
    
    confirmDeleteBtn.addEventListener('click', function (event) {
        deleteForm.submit();
    })
});
