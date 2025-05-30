let draggedTaskId = null;

function handleDragStart(event) {
    draggedTaskId = event.target.getAttribute("data-task-id");
    event.dataTransfer.setData("text/plain", draggedTaskId);
}

function handleDrop(event, newStatus) {
    event.preventDefault();
    const taskId = event.dataTransfer.getData("text/plain");

    fetch(`/update_task_status/${taskId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ status: newStatus })
    }).then(response => {
        if (response.ok) {
            window.location.reload();
        }
    });
}
