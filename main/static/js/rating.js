document.addEventListener("DOMContentLoaded", function () {
    const ratingDiv = document.getElementById("user-rating");
    if (!ratingDiv) return;

    const stars = ratingDiv.querySelectorAll(".star");
    const type = ratingDiv.dataset.type;
    const id = ratingDiv.dataset.id;
    const rateUrl = ratingDiv.dataset.rateUrl;
    const csrfToken = ratingDiv.dataset.csrf;

    stars.forEach(star => {
        star.addEventListener("click", function () {
            const score = this.dataset.score;

            fetch(rateUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrfToken
                },
                body: `type=${type}&id=${id}&score=${score}`
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    alert(`You rated this ${score} stars!`);
                    location.reload();
                } else {
                    alert("Error: " + data.errors);
                }
            })
            .catch(err => console.error("Rating error:", err));
        });
    });
});
