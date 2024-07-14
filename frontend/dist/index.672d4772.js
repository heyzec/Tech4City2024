const SERVER_URL = `http://localhost:8000`;
// ================================================================================
// API
// ================================================================================
class API {
    async get_photos() {
        try {
            const response = await fetch(`${SERVER_URL}/results`);
            if (!response.ok) throw new Error("Failed to fetch photos");
            return await response.json();
        } catch (error) {
            console.error("Error fetching photos:", error.message);
            throw error;
        }
    }
    async upload_photo(file) {
        try {
            const formData = new FormData();
            formData.append("file", file);
            const response = await fetch(`${SERVER_URL}/analyze`, {
                method: "POST",
                body: formData
            });
            if (!response.ok) throw new Error("Failed to upload photo");
            return await response.json();
        } catch (error) {
            console.error("Error uploading photo:", error.message);
            throw error;
        }
    }
}
const api = new API();
// ================================================================================
// Helpers
// ================================================================================
// ================================================================================
// Event handlers
// ================================================================================
// // Tutorial Modal
// document.addEventListener("DOMContentLoaded", function () {
//   if (localStorage.getItem("visited") === "true") {
//     return;
//   }
//   var modal = document.getElementById("tutorialModal");
//   modal.style.display = "block";
//   var closeBtn = modal.querySelector(".close");
//   closeBtn.addEventListener("click", function () {
//     modal.style.display = "none";
//     localStorage.setItem("visited", "true");
//   });
//   var nextBtn = modal.querySelector(".nextBtn");
//   var tutorialText = [
//     "Upload an image by either drag & drop or click on 'Upload Image'.",
//     "Click 'Submit' to upload.",
//     "The image will be sent to analyse and you will be able to view the final results.",
//   ];
//   var step = 0;
//   function updateTutorialText() {
//     document.getElementById("tutorialStep").textContent = "Step " + (step + 1);
//     document.getElementById("tutorialText").textContent = tutorialText[step];
//   }
//   updateTutorialText();
//   nextBtn.addEventListener("click", function () {
//     step++;
//     if (step < tutorialText.length) {
//       updateTutorialText();
//     } else {
//       modal.style.display = "none";
//       localStorage.setItem("visited", "true");
//     }
//   });
// });
// document.addEventListener("DOMContentLoaded", async () => {
//   const r = await fetch(`${SERVER_URL}/results`);
//   const data = await r.json();
//   document.getElementById(
//     "placeholder"
//   ).innerHTML = `Number of elements: ${data.length}`;
// });
// document.getElementById("uploadForm").onsubmit = function (event) {
//   // Stop page from reloading
//   console.log("onsubmit");
//   event.preventDefault();
//   handleUpload();
// };
document.addEventListener("DOMContentLoaded", function() {
    const uploadForm = document.getElementById("uploadForm");
    uploadForm.addEventListener("submit", function(event) {
        event.preventDefault();
        const fileInput = document.getElementById("imageUpload");
        const file = fileInput.files[0];
        api.upload_photo(file).then((response)=>{
            console.log("Updated photo: ", `data:image/png;base64,${response.base64_data}`);
            document.getElementById("resultImage").src = `data:image/png;base64,${response.base64_data}`;
        }).catch((error)=>{
            console.error("Failed to upload photo:", error);
        });
    });
});

//# sourceMappingURL=index.672d4772.js.map
