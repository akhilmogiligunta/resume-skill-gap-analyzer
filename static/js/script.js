document.addEventListener("DOMContentLoaded", () => {

        /* =====================================================
       PAGE TRANSITION
       ===================================================== */

    const pageTransition =
        document.getElementById("pageTransition");

    if (pageTransition) {

        // Hide transition after page has loaded.
        requestAnimationFrame(() => {
            pageTransition.classList.add("hidden");
        });


        // Show transition when navigating away.
        document.querySelectorAll('a[href="/"]').forEach(link => {

            link.addEventListener("click", () => {

                pageTransition.classList.remove("hidden");

                const transitionText =
                    pageTransition.querySelector(
                        ".page-transition-text"
                    );

                if (transitionText) {
                    transitionText.textContent =
                        "Opening analyzer...";
                }
            });
        });


        // Show transition when submitting analyzer form.
        const transitionForm =
            document.getElementById("analyzerForm");

        if (transitionForm) {

            transitionForm.addEventListener("submit", () => {

                pageTransition.classList.remove("hidden");

                const transitionText =
                    pageTransition.querySelector(
                        ".page-transition-text"
                    );

                if (transitionText) {
                    transitionText.textContent =
                        "Analyzing your resume...";
                }
            });
        }
    }

    /* =====================================================
       DARK / LIGHT MODE
       ===================================================== */

    const themeToggle = document.getElementById("themeToggle");
    const themeIcon = document.getElementById("themeIcon");

    function applyTheme(theme) {

        if (theme === "dark") {

            document.body.classList.add("dark-mode");

            if (themeIcon) {
                themeIcon.textContent = "☀️";
            }

        } else {

            document.body.classList.remove("dark-mode");

            if (themeIcon) {
                themeIcon.textContent = "🌙";
            }
        }
    }

    const savedTheme =
        localStorage.getItem("resumeAnalyzerTheme");

    if (savedTheme) {
        applyTheme(savedTheme);
    } else {
        applyTheme("light");
    }

    if (themeToggle) {

        themeToggle.addEventListener("click", () => {

            const isDark =
                document.body.classList.contains("dark-mode");

            const newTheme =
                isDark ? "light" : "dark";

            applyTheme(newTheme);

            localStorage.setItem(
                "resumeAnalyzerTheme",
                newTheme
            );
        });
    }


    /* =====================================================
       RESUME FILE UPLOAD
       ===================================================== */

    const resumeFile =
        document.getElementById("resumeFile");

    const selectedFile =
        document.getElementById("selectedFile");

    const uploadArea =
        document.getElementById("uploadArea");


    /* Normal file selection */

    if (resumeFile && selectedFile) {

        resumeFile.addEventListener("change", () => {

            if (resumeFile.files.length > 0) {

                const file =
                    resumeFile.files[0];

                selectedFile.textContent =
                    `✓ ${file.name}`;

                selectedFile.style.display =
                    "block";

            } else {

                selectedFile.textContent = "";
                selectedFile.style.display = "none";
            }
        });
    }


    /* =====================================================
       DRAG AND DROP
       ===================================================== */

    if (uploadArea && resumeFile) {

        ["dragenter", "dragover"].forEach(
            eventName => {

                uploadArea.addEventListener(
                    eventName,
                    (event) => {

                        event.preventDefault();
                        event.stopPropagation();

                        uploadArea.classList.add(
                            "dragover"
                        );
                    }
                );
            }
        );


        ["dragleave", "drop"].forEach(
            eventName => {

                uploadArea.addEventListener(
                    eventName,
                    (event) => {

                        event.preventDefault();
                        event.stopPropagation();

                        uploadArea.classList.remove(
                            "dragover"
                        );
                    }
                );
            }
        );


        uploadArea.addEventListener(
            "drop",
            (event) => {

                const files =
                    event.dataTransfer.files;

                if (files.length === 0) {
                    return;
                }

                const file = files[0];

                const fileName =
                    file.name.toLowerCase();

                const isPDF =
                    fileName.endsWith(".pdf");

                const isDOCX =
                    fileName.endsWith(".docx");

                if (!isPDF && !isDOCX) {

                    alert(
                        "Unsupported file type. " +
                        "Please upload a PDF or DOCX file."
                    );

                    return;
                }

                resumeFile.files = files;

                selectedFile.textContent =
                    `✓ ${file.name}`;

                selectedFile.style.display =
                    "block";
            }
        );
    }


    /* =====================================================
       FORM SUBMISSION
       ===================================================== */

    const analyzerForm =
        document.getElementById("analyzerForm");

    const analyzeButton =
        document.getElementById("analyzeButton");

    if (analyzerForm && analyzeButton) {

        analyzerForm.addEventListener(
            "submit",
            () => {

                analyzeButton.disabled = true;

                analyzeButton.innerHTML =
                    `<span class="button-icon">⏳</span>
                     Analyzing Resume...`;

                analyzeButton.style.opacity =
                    "0.8";

                analyzeButton.style.cursor =
                    "wait";
            }
        );
    }


    /* =====================================================
       SKILL GAP DOUGHNUT CHART
       ===================================================== */

    const skillGapChart =
        document.getElementById("skillGapChart");

    /*
       skillGapData is created inside results.html.

       We DO NOT put Jinja code here because this is
       a static JavaScript file.
    */

    if (
        skillGapChart &&
        typeof Chart !== "undefined" &&
        typeof skillGapData !== "undefined"
    ) {

        new Chart(
            skillGapChart,
            {
                type: "doughnut",

                data: {

                    labels: [
                        "Matched Skills",
                        "Missing Skills",
                        "Additional Skills"
                    ],

                    datasets: [
                        {
                            data: [
                                skillGapData.matched,
                                skillGapData.missing,
                                skillGapData.additional
                            ],

                            borderWidth: 0
                        }
                    ]
                },

                options: {

                    responsive: true,

                    maintainAspectRatio: false,

                    cutout: "68%",

                    plugins: {

                        legend: {
                            display: false
                        }
                    }
                }
            }
        );
    }

});