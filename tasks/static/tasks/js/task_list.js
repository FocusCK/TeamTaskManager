// task_list.js

function toggleCard(taskId) {
    const cardDetails = document.getElementById(`task-details-${taskId}`);
    if (cardDetails.classList.contains('collapse')) {
        cardDetails.classList.remove('collapse');
    } else {
        cardDetails.classList.add('collapse');
    }
}

function confirmDelete(taskId) {
    const confirmDeletion = confirm("Are you sure you want to delete this task?");
    if (confirmDeletion) {
        return true;
    } else {
        // Prevent default (navigate to the deleted URL)
        return false;
    }
}
