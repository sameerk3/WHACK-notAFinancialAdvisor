function analyzeCrypto() {
    const hashtag = document.getElementById("hashtag").value;
    const executeTransaction = document.getElementById("executeTransaction").checked;
    const resultsDiv = document.getElementById("results");

    // Clear previous results
    resultsDiv.innerHTML = "";

    if (!hashtag) {
        resultsDiv.innerHTML = "Please enter a cryptocurrency hashtag!";
        return;
    }

    // Display the analysis loading message (simulate analysis process)
    resultsDiv.innerHTML = "Analyzing data for " + hashtag + "...";

    // Simulated response after analysis
    setTimeout(() => {
        const analysisResult = "Positive sentiment detected! Recommendation: Buy";
        resultsDiv.innerHTML = `<p>Analysis Result for ${hashtag}: ${analysisResult}</p>`;

        if (executeTransaction) {
            resultsDiv.innerHTML += "<p>Transaction execution enabled. Proceeding with buy order...</p>";
        } else {
            resultsDiv.innerHTML += "<p>Transaction execution is disabled.</p>";
        }
    }, 2000);
}

function runScript() {
    const button = document.getElementById("runScriptButton");
        button.style.display = "none";
}
