function confirmDelete(taskId) {
    const confirmDeletion = confirm("Are you sure you want to delete this task?");
    if (confirmDeletion) {
        return true;
    } else {
        return false;
    }
    }
