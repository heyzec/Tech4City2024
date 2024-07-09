// Upload Image
function handleUpload() {
    const fileInput = document.getElementById("imageUpload");
    const file = fileInput.files[0];
    if (file) console.log("File selected:", file);
    else console.error("No file selected.");
}
// Tutorial Modal
document.addEventListener("DOMContentLoaded", function() {
    if (localStorage.getItem("visited") !== "true") {
        var modal = document.getElementById("tutorialModal");
        modal.style.display = "block";
        var closeBtn = modal.querySelector(".close");
        closeBtn.addEventListener("click", function() {
            modal.style.display = "none";
            localStorage.setItem("visited", "true");
        });
        var nextBtn = modal.querySelector(".nextBtn");
        var tutorialText = [
            "Upload an image by either drag & drop or click on 'Upload Image'.",
            "Click 'Submit' to upload.",
            "The image will be sent to analyse and you will be able to view the final results."
        ];
        var step = 0;
        function updateTutorialText() {
            document.getElementById("tutorialStep").textContent = "Step " + (step + 1);
            document.getElementById("tutorialText").textContent = tutorialText[step];
        }
        updateTutorialText();
        nextBtn.addEventListener("click", function() {
            step++;
            if (step < tutorialText.length) updateTutorialText();
            else {
                modal.style.display = "none";
                localStorage.setItem("visited", "true");
            }
        });
    }
});

//# sourceMappingURL=index.672d4772.js.map
