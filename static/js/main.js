document.addEventListener("DOMContentLoaded", function () {
    const donateButtons = document.getElementById("donate-buttons");
    const donateFormContainer = document.getElementById("donate-form-container");
    const wrappers = donateButtons.querySelectorAll(".donate-btn-wrapper");

    document.querySelectorAll(".donate-btn").forEach(function (btn) {
        btn.onclick = function () {
            // Reset all buttons before applying new styles
            wrappers.forEach((w) => {
                w.classList.remove("fade-out", "selected", "move-left");
                w.style.display = "";
                w.style.opacity = "1";
                w.style.transform = "";
            });

            // Fade out all except clicked
            wrappers.forEach((w) => {
                if (w.contains(btn)) {
                    w.classList.add("selected");
                } else {
                    w.classList.add("fade-out");
                    w.style.transition = "opacity 0.5s ease";
                    w.style.opacity = "0";
                }
            });

            // Move selected button to the left
            const selectedWrapper = Array.from(wrappers).find(w => w.contains(btn));
            const containerRect = donateButtons.getBoundingClientRect();
            const wrapperRect = selectedWrapper.getBoundingClientRect();
            const moveX = wrapperRect.left - containerRect.left;
            selectedWrapper.style.transition = "transform 0.5s cubic-bezier(0.4,0,0.2,1)";
            selectedWrapper.style.transform = `translateX(-${moveX}px)`;
            selectedWrapper.classList.add("move-left");

            // After fade out, show form
            setTimeout(() => {
                // Hide all except selected
                wrappers.forEach((w) => {
                    if (!w.contains(btn)) w.style.display = "none";
                });

                donateButtons.classList.add("hidden");

                // Build leftHtml
                const imgSrc = btn.querySelector(".beer-img").getAttribute("src");
                const priceText = btn.querySelector(".beer-amount").textContent;
                const labelText = btn.querySelector(".beer-label").textContent;
                const leftHtml = `
                    <div style="position:relative; flex: 0 0 20%; max-width: 20%;">
                        <span class="back-arrow" style="
                            position: absolute;
                            left: -2em;
                            top: 50%;
                            transform: translateY(-50%);
                            cursor:pointer;
                            width: 1.2em;
                            height: 1.2em;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        ">
                            <svg width="18" height="18" viewBox="0 0 18 18" style="display:block">
                                <polyline points="12,3 6,9 12,15" style="fill:none;stroke:#000;stroke-width:2;stroke-linecap:square;stroke-linejoin:miter;" />
                            </svg>
                        </span>
                        <div class="donate-btn btn btn-lg w-100 py-3 d-flex flex-column align-items-center justify-content-center" style="background: none; border: none;">
                            <span class="beer-img-wrapper d-block">
                                <img src="${imgSrc}" alt="Beer" class="beer-img" style="height:160px; width:auto;">
                            </span>
                            <div class="beer-amount" style="font-family: 'Yuji Boku', serif; font-size: 1.2em;">
                                ${priceText}
                            </div>
                            <div class="beer-label" style="font-family: 'Inter', sans-serif; font-size: 0.7em;">
                                ${labelText}
                            </div>
                        </div>
                    </div>
                `;

                // Build formHtml
                const formHtml = `
                    <form class="donation-form">
                        <div style="height: 40px;"></div>
                        <div class="mb-2">
                            <input type="text" id="donor-name" class="form-control" placeholder="Your name (optional)">
                        </div>
                        <div class="mb-2">
                            <textarea id="donor-message" class="form-control" placeholder="Message (optional)"></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary w-100" id="donate-button">Donate</button>
                        <div id="donate-message" style="height: 32px; margin-top:0.5em; color:#333; text-align:center; font-size:1em;"></div>
                    </form>
                `;

                // Insert form and left image
                donateFormContainer.innerHTML = `
                    <div class="d-flex w-100 align-items-top">
                        ${leftHtml}
                        <div style="flex:1; height: 278px;">
                            ${formHtml}
                        </div>
                    </div>
                `;
                donateFormContainer.style.display = "block";

                // Add donate button handler
                const donateButton = document.getElementById("donate-button");
                const donateMessage = document.getElementById("donate-message");
                if (donateButton) {
                    donateButton.onclick = async function (e) {
                        e.preventDefault();

                        // Gather form data
                        let donorName = document.getElementById("donor-name").value.trim();
                        const donorMessage = document.getElementById("donor-message").value;
                        const amount = btn.getAttribute("data-amount");

                        // Set defaults if empty
                        if (!donorName) donorName = "anonymous";

                        // Show redirecting message
                        if (donateMessage) {
                            donateMessage.textContent = "Redirecting to payment...";
                            donateMessage.style.color = "#000";
                            donateMessage.style.fontSize = "0.9em";
                        }

                        try {
                            const response = await fetch("/payments/create-checkout-session/", {
                                method: "POST",
                                headers: {
                                    "Content-Type": "application/json",
                                },
                                body: JSON.stringify({
                                    donor_name: donorName,
                                    message: donorMessage || null,
                                    amount: parseFloat(amount),
                                }),
                            });

                            if (!response.ok) {
                                throw new Error(`Error: ${response.statusText}`);
                            }

                            const data = await response.json();
                            window.location.href = data.url;
                        } catch (error) {
                            console.error("Failed to create donation:", error);
                            alert("Failed to create donation. Please try again.");
                        }
                    };
                }

                // Back arrow logic
                const backArrow = donateFormContainer.querySelector('.back-arrow');
                if (backArrow) {
                    backArrow.onclick = function () {
                        const selectedWrapper = donateButtons.querySelector(".donate-btn-wrapper.selected");

                        if (selectedWrapper) {
                            // Fade out the form and selected button
                            donateFormContainer.style.transition = "opacity 0.5s ease";
                            donateFormContainer.style.opacity = "0";
                            selectedWrapper.style.transition = "opacity 0.5s ease, transform 0.5s ease";
                            selectedWrapper.style.opacity = "0";

                            setTimeout(() => {
                                // Hide the form and reset styles
                                donateFormContainer.style.display = "none";
                                donateFormContainer.style.opacity = "1";
                                selectedWrapper.style.opacity = "1";
                                selectedWrapper.style.transform = "translateX(0)";
                                selectedWrapper.classList.remove("selected");

                                // Reset visibility and fade in all buttons
                                donateButtons.classList.remove("hidden");
                                wrappers.forEach((w) => {
                                    w.style.display = "";
                                    w.style.transition = "opacity 0.5s ease";
                                    w.style.opacity = "1";
                                    w.classList.remove("fade-out");
                                });
                            }, 500);
                        } else {
                            // Fallback if no selected wrapper found
                            donateFormContainer.style.display = "none";
                            donateButtons.classList.remove("hidden");
                            wrappers.forEach((w) => {
                                w.style.display = "";
                                w.style.opacity = "1";
                                w.classList.remove("fade-out");
                            });
                        }
                    };
                }
            }, 500); // fade out duration
        };
    });
});