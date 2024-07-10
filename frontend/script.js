const SERVER_URL = `http://localhost:8000`;

// ================================================================================
// API
// ================================================================================

class API {
  async get_photos() {
    console.log("get_photos");
    const r = await fetch(`${SERVER_URL}/photos`);
    return await r.json();
  }

  async upload_photo(name, email, file) {
    console.log("upload_photo");

    const formData = new FormData();
    formData.append('name', name);
    formData.append('email', email);
    formData.append('file', file);

    fetch(`${SERVER_URL}/photos`, {
      method: 'POST',
      body: formData
    });
  }
}

const api = new API()

// ================================================================================
// Helpers
// ================================================================================

// Upload Image
function handleUpload() {
  const fileInput = document.getElementById("imageUpload");
  const file = fileInput.files[0];

  // This shouldn't happen because HTML prevents submit button from being pressed when file not selected
  if (!file) {
    console.error("No file selected.");
    return;
  }

  api.upload_photo("name", "example@example.com", file);
}


// ================================================================================
// Event handlers
// ================================================================================

// Tutorial Modal
document.addEventListener("DOMContentLoaded", function () {
  if (localStorage.getItem("visited") === "true") {
    return;
  }

  var modal = document.getElementById("tutorialModal");
  modal.style.display = "block";

  var closeBtn = modal.querySelector(".close");
  closeBtn.addEventListener("click", function () {
    modal.style.display = "none";
    localStorage.setItem("visited", "true");
  });

  var nextBtn = modal.querySelector(".nextBtn");
  var tutorialText = [
    "Upload an image by either drag & drop or click on 'Upload Image'.",
    "Click 'Submit' to upload.",
    "The image will be sent to analyse and you will be able to view the final results.",
  ];
  var step = 0;

  function updateTutorialText() {
    document.getElementById("tutorialStep").textContent =
      "Step " + (step + 1);
    document.getElementById("tutorialText").textContent = tutorialText[step];
  }

  updateTutorialText();

  nextBtn.addEventListener("click", function () {
    step++;
    if (step < tutorialText.length) {
      updateTutorialText();
    } else {
      modal.style.display = "none";
      localStorage.setItem("visited", "true");
    }
  });
});

document.addEventListener("DOMContentLoaded", async () => {
  const r = await fetch(`${SERVER_URL}/photos`);
  const data = await r.json();
  document.getElementById("placeholder").innerHTML = `Number of elements: ${data.length}`;
});


document.getElementById('uploadForm').onsubmit = function(event) {
  // Stop page from reloading
  event.preventDefault();

  handleUpload();
};

