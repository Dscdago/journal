window.onload=function(){
    const entryModal = document.getElementById('journalEntry');
        entryModal.addEventListener('show.bs.modal', event => {
            // Button that triggered the modal
            const button = event.relatedTarget;
            // Extract info from data-myentry
            const journalEntry = button.getAttribute('data-myentry');
            var entryData = JSON.parse(journalEntry);
            var entry = entryData["entry"];

            // Update modal's content
            document.getElementById("entryParagraph").innerHTML = entry;
        });
}