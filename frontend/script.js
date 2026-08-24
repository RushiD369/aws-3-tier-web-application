const API_URL = "http://127.0.0.1:5000";

const form = document.getElementById("submissionForm");
const result = document.getElementById("result");

form.addEventListener("submit", async function (event) {

    event.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const message = document.getElementById("message").value;

    const data = {
        name: name,
        email: email,
        message: message
    };

    result.textContent = "Submitting...";

    try {

        const response = await fetch(
            `${API_URL}/submit-data`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );

        const resultData = await response.json();

        if (response.ok) {

            result.textContent =
                "Data submitted successfully!";

            form.reset();

        } else {

            result.textContent =
                resultData.message || "Submission failed.";
        }

    } catch (error) {

        console.error(error);

        result.textContent =
            "Unable to connect to backend.";
    }

});