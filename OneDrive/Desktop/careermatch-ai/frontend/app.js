// CareerMatch AI — Frontend JavaScript

const API = "http://localhost:8000";

const $ = selector => document.querySelector(selector);

const file = $("#resume");
const drop = $("#drop");
const job = $("#job");
const form = $("#form");


// Job description character counter

job.addEventListener("input", () => {

    $("#count").textContent =
        job.value.length.toLocaleString() + " characters";

});


// Display selected resume

file.addEventListener("change", () => {

    if (file.files[0]) {

        $("#file-name").textContent =
            file.files[0].name;

    }

});


// Drag and drop functionality

["dragover", "dragenter"].forEach(eventName => {

    drop.addEventListener(eventName, event => {

        event.preventDefault();

        drop.style.borderColor = "#167653";

    });

});


["drop", "dragleave"].forEach(eventName => {

    drop.addEventListener(eventName, event => {

        event.preventDefault();

        drop.style.borderColor = "";

    });

});


drop.addEventListener("drop", event => {

    const selectedFile = event.dataTransfer.files[0];

    if (!selectedFile) return;

    if (!/\.(pdf|txt)$/i.test(selectedFile.name)) {

        return showError(
            "Please select a PDF or TXT file."
        );

    }

    const dataTransfer = new DataTransfer();

    dataTransfer.items.add(selectedFile);

    file.files = dataTransfer.files;

    $("#file-name").textContent =
        selectedFile.name;

});


// Display errors

function showError(message) {

    $("#error").textContent = message;

    $("#error").classList.remove("hidden");

}


// Render skill tags

function fillTags(id, items, missing = false) {

    const element = $(id);

    element.replaceChildren();

    if (!items.length) {

        element.textContent = "No skills detected.";

        return;

    }

    items.forEach(skill => {

        const tag = document.createElement("span");

        tag.className =
            "tag" + (missing ? " missing" : "");

        tag.textContent = skill;

        element.append(tag);

    });

}


// Render lists

function fillList(id, items) {

    const element = $(id);

    element.replaceChildren();

    const values = items.length
        ? items
        : ["No items identified."];

    values.forEach(item => {

        const li = document.createElement("li");

        li.textContent = item;

        element.append(li);

    });

}


// Submit resume for analysis

form.addEventListener("submit", async event => {

    event.preventDefault();

    $("#error").classList.add("hidden");

    $("#results").classList.add("hidden");


    const selectedFile = file.files[0];

    if (!selectedFile) {

        return showError(
            "Please upload your resume."
        );

    }


    if (selectedFile.size > 5 * 1024 * 1024) {

        return showError(
            "Resume must be 5 MB or smaller."
        );

    }


    if (job.value.trim().length < 50) {

        return showError(
            "Please paste a job description of at least 50 characters."
        );

    }


    // Prepare multipart request

    const data = new FormData();

    data.append("resume", selectedFile);

    data.append("job_description", job.value);


    // Show loading state

    $("#loading").classList.remove("hidden");

    $("#submit").disabled = true;


    try {

        const response = await fetch(
            API + "/api/analyze",
            {
                method: "POST",
                body: data
            }
        );


        const result = await response.json();


        if (!response.ok) {

            throw new Error(
                result.detail || "Analysis failed."
            );

        }


        // Render results

        render(result);

        $("#results").classList.remove("hidden");

        $("#results").scrollIntoView({
            behavior: "smooth"
        });


    } catch (error) {

        showError(
            error.message +
            " — Check that the FastAPI server is running on port 8000."
        );

    } finally {

        $("#loading").classList.add("hidden");

        $("#submit").disabled = false;

    }

});


// Render complete analysis

function render(data) {

    // Match score

    $("#score").textContent =
        data.match_score + "%";

    $("#label").textContent =
        data.score_label;

    $("#bar").style.width =
        data.match_score + "%";


    // Summary

    $("#summary").textContent =
        data.summary;


    // Statistics

    $("#matched-count").textContent =
        data.matched_skills.length;

    $("#missing-count").textContent =
        data.missing_skills.length;


    // Skills

    fillTags(
        "#matched",
        data.matched_skills
    );

    fillTags(
        "#missing",
        data.missing_skills,
        true
    );


    // Strengths

    fillList(
        "#strengths",
        data.strengths
    );


    // Recommendations

    fillList(
        "#recommendations",
        data.recommendations
    );


    // Requirements breakdown

    const requirements = $("#requirements");

    requirements.replaceChildren();


    data.required_skills.forEach(skill => {

        const row = document.createElement("div");

        row.className = "req";


        const left = document.createElement("div");

        const title = document.createElement("b");

        title.textContent = skill.name;


        const evidence = document.createElement("small");

        evidence.textContent = skill.matched
            ? (
                skill.evidence ||
                "Keyword found in resume."
            )
            : "No matching keyword detected in resume.";


        left.append(title, evidence);


        const status = document.createElement("em");

        status.className = skill.matched ? "" : "no";

        status.textContent = skill.matched
            ? "Matched"
            : "Not detected";


        row.append(left, status);

        requirements.append(row);

    });


    // Resume bullet suggestions

    const bullets = $("#bullets");

    bullets.replaceChildren();


    data.bullet_suggestions.forEach(item => {

        const block = document.createElement("div");

        block.className = "bullet";


        const original = document.createElement("p");

        original.textContent =
            "Original context: " +
            item.original_context;


        const rewrite = document.createElement("p");

        rewrite.className = "rewrite";

        rewrite.textContent =
            item.suggested_bullet;


        const reason = document.createElement("p");

        reason.textContent =
            "Why: " + item.reason;


        block.append(
            original,
            rewrite,
            reason
        );

        bullets.append(block);

    });


    // Disclaimer

    $("#disclaimer").textContent =
        data.disclaimer;

}
