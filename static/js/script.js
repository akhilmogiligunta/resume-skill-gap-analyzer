document.addEventListener("DOMContentLoaded", function () {

    const form = document.querySelector(".analyzer-form");

    if (!form) {
        return;
    }

    form.addEventListener("submit", function (event) {

        const resumeFile =
            document.getElementById("resume_file");

        const resumeText =
            document.getElementById("resume_text");

        const jobDescription =
            document.getElementById("job_description");

        const hasFile =
            resumeFile.files.length > 0;

        const hasResumeText =
            resumeText.value.trim().length > 0;

        const hasJobDescription =
            jobDescription.value.trim().length > 0;


        // Check job description
        if (!hasJobDescription) {

            event.preventDefault();

            alert(
                "Please enter a job description."
            );

            jobDescription.focus();

            return;
        }


        // Check resume
        if (!hasFile && !hasResumeText) {

            event.preventDefault();

            alert(
                "Please upload a PDF/DOCX resume " +
                "or enter resume text manually."
            );

            resumeText.focus();

            return;
        }


        // Check file extension
        if (hasFile) {

            const filename =
                resumeFile.files[0].name.toLowerCase();

            const validExtension =
                filename.endsWith(".pdf") ||
                filename.endsWith(".docx");

            if (!validExtension) {

                event.preventDefault();

                alert(
                    "Only PDF and DOCX files are supported."
                );

                resumeFile.value = "";

                return;
            }
        }

    });

});